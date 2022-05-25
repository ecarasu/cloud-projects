import oci
import os
import config
import csv
import migration_logger


def config_oci_client():
    return oci.config.from_file()


def config_ocs_client():
    config = config_oci_client()
    return oci.object_storage.ObjectStorageClient(config)


def get_object_namespace():
    object_storage_client = config_ocs_client()
    return object_storage_client.get_namespace().data


def make_directory(directory_list, src_directory):
    for directory in directory_list:
        destination_dir = src_directory.format(directory.split('/')[-1])
        isExist = os.path.exists(os.path.dirname(
            destination_dir+chr(92)+directory.replace('/', chr(92))))
        if not isExist:
            os.makedirs(os.path.dirname(destination_dir +
                        chr(92)+directory.replace('/', chr(92))))


def create_audit_file(bucket_name: str, audit_file_name: str):
    object_storage_client = config_ocs_client()
    namespace = get_object_namespace()
    directories = []

    with open(audit_file_name, 'w', newline='', encoding='utf-8') as audit_file:
        fieldnames = config.audit_header
        field_count = len(fieldnames) - 2

        csvwriter = csv.writer(audit_file)
        csvwriter.writerow(fieldnames)

        for object in object_storage_client.list_objects(namespace, bucket_name=bucket_name, fields=['size']).data.objects:
            if object.name[-1] != '/':
                csvwriter.writerow(
                    [object.name, object.size] + ([''] * field_count))
            else:
                directories.append(object.name)
    return directories


def download_from_oci_bucket(src_bucket_name: str, directory_path: str, audit_file: str):

    object_storage_client = config_ocs_client()
    namespace = get_object_namespace()
    object_list = create_audit_file(
        bucket_name=src_bucket_name, audit_file_name=audit_file)
    make_directory(object_list, directory_path)

    with open(audit_file, 'r') as audit_file:
        files = csv.DictReader(audit_file)
        for object_name in files:

            destination_dir = (directory_path).format(
                object_name['OCS_FILE_NAME'].split('/')[-1])
            get_obj = object_storage_client.get_object(
                namespace, src_bucket_name, object_name['OCS_FILE_NAME'])
            ocs_logger = migration_logger.craete_migration_log(
                config.log_file, __name__)
            ocs_logger.info('STARTED DOWNLOADING {}'.format(
                object_name['OCS_FILE_NAME']))

            with open(os.path.join(destination_dir, object_name['OCS_FILE_NAME'].replace('/', chr(92))), 'wb') as file:
                size = 0
                for chunk in get_obj.data.raw.stream(config.chunk_size, decode_content=False):

                    file.write(chunk)
            ocs_logger.info('FINISHED DOWNLOADING {}'.format(
                object_name['OCS_FILE_NAME']))
