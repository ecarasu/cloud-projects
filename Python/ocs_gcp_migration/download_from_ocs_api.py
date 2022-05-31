import os
import config
import requests
import csv
import urllib.parse
from datetime import datetime


def writeToAuditFile(fileName: str, content: dict, header: list, isHeader: bool):
    if isHeader:
        with open(fileName, 'w', newline='', encoding='utf-8') as auditFile:
            csv_writer = csv.writer(auditFile)
            csv_writer.writerow(header)
    else:
        with open(fileName, 'a', newline='', encoding='utf-8') as auditFile:
            csv_writer = csv.DictWriter(auditFile, fieldnames=header)
            csv_writer.writerow(content)


def make_directory(directory_list, src_directory):
    for directory in directory_list:
        destination_dir = src_directory.format(directory.split('/')[-1])
        isExist = os.path.exists(os.path.dirname(
            destination_dir+chr(92)+directory.replace('/', chr(92))))
        if not isExist:
            os.makedirs(os.path.dirname(destination_dir +
                        chr(92)+directory.replace('/', chr(92))))


def create_audit_file(ocs_pre_auth_url: str, audit_file_name: str):

    directories = []

    with open(audit_file_name, 'w', newline='', encoding='utf-8') as audit_file:
        fieldnames = config.inp_audit_header
        field_count = len(fieldnames) - 3

        csvwriter = csv.writer(audit_file)
        csvwriter.writerow(fieldnames)
        response = requests.get(ocs_pre_auth_url)
        response_data = response.json()

        for object in response_data['objects']:
            if object['name'][-1] != '/':
                csvwriter.writerow(
                    [object['name'], object['md5'], object['size']] + (['-'] * field_count))
            else:
                directories.append(object['name'])
    return directories


def download_from_oci_bucket(ocs_pre_auth_url: str, ocs_url_fields: str, directory_path: str, inp_audit_file: str, out_audit_file: str, out_audit_header: str, chunk_size: int):

    object_list = create_audit_file(
        ocs_pre_auth_url=ocs_pre_auth_url+ocs_url_fields, audit_file_name=inp_audit_file)
    make_directory(object_list, directory_path)
    out_audit_dict = dict.fromkeys(out_audit_header, None)
    writeToAuditFile(fileName=out_audit_file, content={},
                     header=out_audit_header, isHeader=True)

    with open(inp_audit_file, 'r') as audit_file:
        files = csv.DictReader(audit_file)
        for object_name in files:

            destination_dir = (directory_path).format(
                object_name['OCS_FILE_NAME'].split('/')[-1])

            out_audit_dict['OCS_FILE_NAME'] = object_name['OCS_FILE_NAME']
            out_audit_dict['MD5'] = object_name['MD5']
            out_audit_dict['SIZE'] = object_name['SIZE']
            out_audit_dict['DOWNLOAD_SIZE'] = 0

            get_file = requests.get(
                ocs_pre_auth_url+urllib.parse.quote(object_name['OCS_FILE_NAME'], safe=''), stream=True)

            with open(os.path.join(destination_dir, object_name['OCS_FILE_NAME'].replace('/', chr(92))), 'wb') as file:
                out_audit_dict['DOWNLOAD_START_DATE'] = datetime.now()
                for chunk in get_file.iter_content(chunk_size=chunk_size):
                    if chunk:
                        file.write(chunk)
                        out_audit_dict['DOWNLOAD_END_DATE'] = datetime.now()
                        out_audit_dict['DOWNLOAD_SIZE'] = (
                            out_audit_dict['DOWNLOAD_SIZE'] + len(chunk))
            writeToAuditFile(fileName=out_audit_file, content=out_audit_dict,
                             header=out_audit_header, isHeader=False)
