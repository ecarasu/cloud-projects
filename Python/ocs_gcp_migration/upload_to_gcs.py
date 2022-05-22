import os
import glob
from google.cloud import storage
import config
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

os.makedirs(os.path.dirname(config.log_file), exist_ok=True)
file_handler = logging.FileHandler(config.log_file, mode='a')
file_handler.setFormatter(formatter)


logger.addHandler(file_handler)


def get_relative_paths(directory_path: str):
    return glob.glob(directory_path + '/**', recursive=True)


def config_gcs_client(service_account_credentials: str):
    return storage.Client.from_service_account_json(config.gcs_service_account_credentials)


def upload_to_gcp_from_directory(directory_path: str, dest_bucket_name: str):

    gcs_client = config_gcs_client(config.gcs_service_account_credentials)
    rel_paths = get_relative_paths(directory_path)
    gcp_bucket = gcs_client.get_bucket(dest_bucket_name)

    for local_file in rel_paths[1:]:
        remote_path = "/".join(local_file.split(os.sep)[2:])

        if os.path.isfile(local_file):
            blob = gcp_bucket.blob(remote_path)
            logger.info('STARTED UPLOADING {}'.format(local_file))

            blob.upload_from_filename(local_file)
            logger.info('FINISHED UPLOADING {}'.format(local_file))
