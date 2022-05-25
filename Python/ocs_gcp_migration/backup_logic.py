

# def download_from_oci_bucket(src_bucket_name: str, directory_path: str):

#     object_storage_client = config_ocs_client()
#     namespace = get_object_namespace()
#     object_list = get_object_list(src_bucket_name)
#     make_directory(object_list[0], directory_path)

#     for object_name in object_list[1]:
#         destination_dir = (directory_path).format(object_name.split('/')[-1])
#         get_obj = object_storage_client.get_object(
#             namespace, src_bucket_name, object_name)

#         ocs_logger = migration_logger.craete_migration_log(
#             config.log_file, __name__)

#         with open(os.path.join(destination_dir, object_name.replace('/', chr(92))), 'wb') as file:
#             ocs_logger.info('STARTED DOWNLOADING {}'.format(object_name))
#             for chunk in get_obj.data.raw.stream(config.chunk_size, decode_content=False):
#                 file.write(chunk)
#                 ocs_logger.info('FINISHED DOWNLOADING {}'.format(object_name))


# def get_object_list(bucket_name: str):
#     objects, directories = [], []
#     object_storage_client = config_ocs_client()
#     namespace = get_object_namespace()
#     for object in object_storage_client.list_objects(namespace, bucket_name=bucket_name, fields=['size']).data.objects:

#         if object.name[-1] != '/':
#             objects.append(object.name)
#         else:
#             directories.append(object.name)
#     return [directories, objects]

# def get_audit_header(seed_audit_file: str):
#     header = None
#     with open(seed_audit_file, 'r') as header_file:
#         header_csv_file = csv.reader(header_file)
#         header = next(header_csv_file)
#     return header
