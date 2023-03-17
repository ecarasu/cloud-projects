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
    with open(filename, 'rb') as file_to_check:
        with mmap.mmap(file_to_check.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
            md5_hash = hashlib.md5(mmapped_file).digest()
            md5_base64 = base64.b64decode(md5_hash).decode()
            return md5_base64


def download_from_oci_bucket(ocs_pre_auth_url, directory_path, inp_audit_file, out_audit_file, out_audit_header, chunk_size):

    out_audit_dict = {key: None for key in out_audit_header}
    writeToAuditFile(out_audit_file, {}, out_audit_header, True)

    with open(inp_audit_file, 'r') as audit_file:
        files = csv.DictReader(audit_file)
        for object_name in files:
            destination_dir = (directory_path).format(
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
