import oci
import os
import config
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

os.makedirs(os.path.dirname(config.log_file), exist_ok=True)
file_handler = logging.FileHandler(config.log_file, mode='a')
file_handler.setFormatter(formatter)


logger.addHandler(file_handler)


def config_oci_client():
    return oci.config.from_file()


def config_ocs_client():
    config = config_oci_client()
    return oci.object_storage.ObjectStorageClient(config)


def get_object_namespace():
    object_storage_client = config_ocs_client()
    return object_storage_client.get_namespace().data


def get_object_list(bucket_name: str):
    objects, directories = [], []
    object_storage_client = config_ocs_client()
    namespace = get_object_namespace()
    for object in object_storage_client.list_objects(namespace, bucket_name=bucket_name).data.objects:

        if object.name[-1] != '/':
            objects.append(object.name)
        else:
            directories.append(object.name)
    return [directories, objects]


def make_directory(directory_list, src_directory):
    for directory in directory_list:
        destination_dir = src_directory.format(directory.split('/')[-1])
        isExist = os.path.exists(os.path.dirname(
            destination_dir+chr(92)+directory.replace('/', chr(92))))
        if not isExist:
            os.makedirs(os.path.dirname(destination_dir +
                        chr(92)+directory.replace('/', chr(92))))


def download_from_oci_bucket(src_bucket_name: str, directory_path: str):

    object_storage_client = config_ocs_client()
    namespace = get_object_namespace()
    object_list = get_object_list(src_bucket_name)
    make_directory(object_list[0], directory_path)

    for object_name in object_list[1]:
        destination_dir = (directory_path).format(object_name.split('/')[-1])
        get_obj = object_storage_client.get_object(
            namespace, src_bucket_name, object_name)

        with open(os.path.join(destination_dir, object_name.replace('/', chr(92))), 'wb') as file:
            logger.info('STARTED DOWNLOADING {}'.format(object_name))
            for chunk in get_obj.data.raw.stream(2048 ** 2, decode_content=False):
                file.write(chunk)
                logger.info('FINISHED DOWNLOADING {}'.format(object_name))
