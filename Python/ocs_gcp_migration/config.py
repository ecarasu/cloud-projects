oci_bucket_name = 'gcp_migration'
gcp_bucket_name = 'oci-migration-2022'
download_dir = r"D:\Career\Learning\Python\Projects\OCI_GCP"
download_dir += f'{chr(92)}{oci_bucket_name}'
upload_dir = r"D:\Career\Learning\Python\Projects\OCI_GCP"+chr(92)

gcs_service_account_credentials = r'D:\Career\Playground\GCP\triple-shift-350411-72c624b2f9b9.json'
log_file = r'D:\Career\Learning\Python\Projects\OCI_GCP\Logs\Migration.log'
chunk_size = 2048 ** 2
inp_audit_header = ['OCS_FILE_NAME',
                    'MD5',
                    'SIZE']

out_audit_header = ['OCS_FILE_NAME',
                    'MD5',
                    'SIZE',
                    'DOWNLOAD_START_DATE',
                    'DOWNLOAD_END_DATE',
                    'DOWNLOAD_SIZE']
inp_audit_file = r'D:\Career\Learning\Python\Projects\OCI_GCP\Audit\inp_Audit.csv'
out_audit_file = r'D:\Career\Learning\Python\Projects\OCI_GCP\Audit\out_Audit.csv'
ocs_pre_auth_url = 'https://objectstorage.us-ashburn-1.oraclecloud.com/p/bxYwzoZGS8qeabN90MERwPHkXt8orfz2OqDsFR7jXL0VxPe_6ot4YbMFepmvoPpY/n/idt88w6rh4ji/b/gcp_migration/o/'
ocs_url_fields = r'?fields=name,md5,size'
