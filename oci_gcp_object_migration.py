import oci
import glob
import os
from google.cloud import storage

config = oci.config.from_file()
objects = []
upload_objects = []
bucket_name='gcp_migration'
download_dir='D:\Test'


def upload_to_gcp_from_directory(dest_blob_name: str, directory_path: str, dest_bucket_name: str):
    GCS_CLIENT = storage.Client.from_service_account_json(r'D:\Career\Playground\GCP\gcp-poc-349906-3ab8a3cf6b02.json')
    rel_paths = glob.glob(directory_path + '/**', recursive=True)
    print(rel_paths)
    bucket = GCS_CLIENT.get_bucket(dest_bucket_name)
    for local_file in rel_paths:
        remote_path = f'{dest_blob_name}/{"/".join(local_file.split(os.sep)[1:])}'
        if os.path.isfile(local_file):
            blob = bucket.blob(remote_path)
            blob.upload_from_filename(local_file)


# Initialize service client with default config file
object_storage_client = oci.object_storage.ObjectStorageClient(config)
namespace = object_storage_client.get_namespace().data


bucket = object_storage_client.get_bucket(namespace, bucket_name=bucket_name)
object_list = object_storage_client.list_objects(namespace, bucket_name=bucket_name)

for o in object_list.data.objects:
    objects.append(o.name)
    

for object_name in objects:
    print(object_name)
    if object_name[-1] != '/':
        destination_dir = (download_dir).format(object_name.split('/')[-1])
        upload_objects.append(destination_dir+chr(92)+object_name.split('/')[-1])
        get_obj = object_storage_client.get_object(namespace, bucket_name, object_name)
        with open(os.path.join(destination_dir,object_name.split('/')[-1]), 'wb') as f:
            for chunk in get_obj.data.raw.stream(16384 ** 2, decode_content=False):
                f.write(chunk)
    else:
        print('Not a file')
        

upload_to_gcp_from_directory('Test',download_dir,'arasu-bucket')
