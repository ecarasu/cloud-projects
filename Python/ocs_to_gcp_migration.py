import oci
import os
import glob
from google.cloud import storage
from datetime import datetime


oci_bucket_name = 'gcp_migration'
gcp_bucket_name = 'oci-migration-2022'
download_dir = r'D:\Test'
gcs_service_account_credentials = r''


def upload_to_gcp_from_directory(directory_path: str, dest_bucket_name: str):
    GCS_CLIENT = storage.Client.from_service_account_json(
        gcs_service_account_credentials)
    rel_paths = glob.glob(directory_path + '/**', recursive=True)

    gcp_bucket = GCS_CLIENT.get_bucket(dest_bucket_name)
    for local_file in rel_paths[1:]:
        remote_path = "/".join(local_file.split(os.sep)[2:])

        if os.path.isfile(local_file):
            blob = gcp_bucket.blob(remote_path)
            print('Started upoading '+local_file+' at: '+str(datetime.now()))
            blob.upload_from_filename(local_file)
            print('Finished upoading '+local_file + ' at: '+str(datetime.now()))


def download_from_oci_bucket(src_bucket_name: str, directory_path: str):
    objects = []
    config = oci.config.from_file()
    object_storage_client = oci.object_storage.ObjectStorageClient(config)
    namespace = object_storage_client.get_namespace().data

    object_list = object_storage_client.list_objects(
        namespace, bucket_name=src_bucket_name)

    for object in object_list.data.objects:
        objects.append(object.name)

    for object_name in objects:
        if object_name[-1] != '/':
            destination_dir = (directory_path).format(
                object_name.split('/')[-1])
            get_obj = object_storage_client.get_object(
                namespace, src_bucket_name, object_name)

            isExist = os.path.exists(os.path.dirname(
                destination_dir+chr(92)+object_name.replace('/', chr(92))))

            if isExist:
                with open(os.path.join(destination_dir, object_name.replace('/', chr(92))), 'wb') as file:
                    print('Started downloading '+object_name +
                          ' from OCI at: '+str(datetime.now()))
                    for chunk in get_obj.data.raw.stream(2048 ** 2, decode_content=False):
                        file.write(chunk)
                    print('Finished downloading '+object_name +
                          ' from OCI at: '+str(datetime.now()))

            if not isExist:
                os.makedirs(os.path.dirname(destination_dir +
                            chr(92)+object_name.replace('/', chr(92))))
                with open(os.path.join(destination_dir, object_name.replace('/', chr(92))), 'wb') as file:
                    print('Started downloading '+object_name +
                          ' from OCI at: '+str(datetime.now()))
                    for chunk in get_obj.data.raw.stream(2048 ** 2, decode_content=False):
                        file.write(chunk)
                    print('Finished downloading '+object_name +
                          ' from OCI at: '+str(datetime.now()))


download_from_oci_bucket(oci_bucket_name, download_dir)
print('---------------------------------------------------')
upload_to_gcp_from_directory(download_dir, gcp_bucket_name)
