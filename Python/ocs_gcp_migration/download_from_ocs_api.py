import os
import csv
import mmap
import base64
import config
import hashlib
import requests
import urllib.parse
from datetime import datetime
from urllib.parse import quote


def createAuditFile(ocs_pre_auth_url: str, ocs_url_fields: str, audit_file_name: str, inp_audit_header: list):
    directories = []
    session = requests.Session()

    with open(audit_file_name, 'w', newline='', encoding='utf-8') as audit_file:
        fieldnames = inp_audit_header

        writer = csv.DictWriter(audit_file, fieldnames=fieldnames)
        writer.writeheader()

        response = session.get(f"{ocs_pre_auth_url}{ocs_url_fields}")
        response_data = response.json()

        for obj in response_data['objects']:
            if obj['name'][-1] != '/':
                row = {"OCS_FILE_NAME": obj['name'],
                       "MD5": obj['md5'], "SIZE": obj['size']}
                row.update({field: '-' for field in fieldnames[3:]})
                writer.writerow(row)
            else:
                directories.append(obj['name'])

    return directories


def writeToAuditFile(filename: str, content: dict, header: list, isHeader: bool):
    mode = 'w' if isHeader else 'a'
    with open(filename, mode, newline='', encoding='utf-8') as auditFile:
        csv_writer = csv.DictWriter(auditFile, fieldnames=header)
        if isHeader:
            csv_writer.writeheader()
        else:
            csv_writer.writerow(content)


def makeDirectory(directory_list: list, src_directory: str):
    if not os.path.exists(src_directory):
        os.makedirs(src_directory)
    for directory in directory_list:
        destination_dir = os.path.join(
            src_directory, os.path.basename(directory))
        directory_path = os.path.join(
            destination_dir, directory.replace('/', os.sep))
        os.makedirs(directory_path, exist_ok=True)


def getMd5(filename: str):
    try:
        file_size = os.path.getsize(filename)
        if file_size == 0:
            return "dummy-value"
        with open(filename, 'rb') as file_to_check:
            with mmap.mmap(file_to_check.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
                md5_hash = hashlib.md5(mmapped_file).digest()
                md5_base64 = base64.b64encode(md5_hash).decode()
                return md5_base64
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except Exception as e:
        print(f"Error: {str(e)}")


def download_from_oci_bucket(ocs_pre_auth_url, directory_path, inp_audit_file, out_audit_file, out_audit_header, chunk_size):

    out_audit_dict = {key: None for key in out_audit_header}
    writeToAuditFile(out_audit_file, {}, out_audit_header, True)

    with open(inp_audit_file, 'r') as audit_file:
        files = csv.DictReader(audit_file)
        for object_name in files:
            destination_dir = directory_path.format(
                object_name['OCS_FILE_NAME'].split('/')[-1])

            out_audit_dict.update({'OCS_FILE_NAME': object_name['OCS_FILE_NAME'],
                                   'MD5': object_name['MD5'],
                                   'SIZE': object_name['SIZE'],
                                   'DOWNLOAD_SIZE': 0,
                                   'DOWNLOAD_START_DATE': datetime.now()})

            get_file = requests.get(
                ocs_pre_auth_url + quote(object_name['OCS_FILE_NAME'], safe=''), stream=True)

            with open(os.path.join(destination_dir, object_name['OCS_FILE_NAME'].replace('/', chr(92))), 'wb') as file:
                for chunk in get_file.iter_content(chunk_size=chunk_size):
                    if chunk:
                        file.write(chunk)
                        out_audit_dict.update({'DOWNLOAD_END_DATE': datetime.now(),
                                               'DOWNLOAD_SIZE': out_audit_dict['DOWNLOAD_SIZE'] + len(chunk)})
                        writeToAuditFile(
                            out_audit_file, out_audit_dict, out_audit_header, False)


def splitFile(input_file: str, multi_part_size: int):
    with open(input_file, 'rb') as file:
        part_number = 1
        while True:
            part = file.read(multi_part_size)
            if not part:
                break
            output_file = '{}.{}'.format(input_file, part_number)
            with open(output_file, 'wb') as out:
                out.write(part)
            part_number += 1
    return part_number


def createUploadAuditFile(directory_path: str, audit_file_name: str, audit_header: str):
    
    writeToAuditFile(filename=audit_file_name, content={},
                     header=audit_header, isHeader=True)
    out_audit_dict = dict.fromkeys(audit_header, None)
    for root, directories, files in os.walk(directory_path):
        for file in files:
            out_audit_dict['FILE'] = os.path.join(root, file)
            out_audit_dict['SIZE'] = os.stat(out_audit_dict['FILE']).st_size
            out_audit_dict['MD5'] = getMd5(out_audit_dict['FILE'])

            writeToAuditFile(audit_file_name, out_audit_dict,
                             audit_header, isHeader=False)


def multiPartUpload(ocs_pre_auth_url, upload_dir, inp_audit_file,
                    out_audit_file, out_audit_header, part_size, base_url):

    out_audit_dict = {key: None for key in out_audit_header}
    writeToAuditFile(out_audit_file, {}, out_audit_header, True)

    with open(inp_audit_file, 'r') as audit_file:
        files = csv.DictReader(audit_file)
        for object_name in files:
            url = ocs_pre_auth_url + \
                quote(object_name['FILE'].replace(
                    upload_dir, "").replace(chr(92), '/'), safe='')

            headers = {'opc-multipart': 'true'}
            response = requests.put(url, headers=headers)

            multi_part_url = base_url
            multi_part_url += response.json()['accessUri']
            start_time = datetime.now()
            out_audit_dict.update({'FILE': object_name['FILE'],
                                   'SIZE': object_name['SIZE'],
                                   'MD5': object_name['MD5'],
                                   'UPLOAD_START_TIME': start_time})

            parts = splitFile(
                input_file=object_name['FILE'], multi_part_size=part_size)

            for part in range(1, parts):
                data = open(object_name['FILE']+f'.{part}', 'rb').read()
                headers = {'Content-Type': 'application/octet-stream'}
                response = requests.put(
                    f'{multi_part_url}{part}', headers=headers, data=data)
                if response.status_code == 200:
                    # Delete the file if the response code is 200 (OK)
                    os.remove(object_name['FILE']+f'.{part}')

            post_headers = {'Content-Type': 'application/json'}
            post_response = requests.post(multi_part_url, headers=post_headers)

            end_time = datetime.now()
            out_audit_dict.update({'UPLOAD_END_TIME': end_time,
                                   'DURATION': round((end_time - start_time).total_seconds()),
                                   'RESPONSE': post_response})
            writeToAuditFile(
                out_audit_file, out_audit_dict, out_audit_header, False)
