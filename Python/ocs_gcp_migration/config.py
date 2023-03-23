oci_bucket_name = 'gcp_migration'
ocs_pre_auth_url = 'https://objectstorage.us-ashburn-1.oraclecloud.com/p/OH0pThZmn1i6GNS5VvTflorDz28LprIRmpWpJT2jWbdv3ey69MnhPl1cYFFVjdnC/n/idt88w6rh4ji/b/gcp_migration/o/'
ocs_url_fields = r'?fields=name,md5,size'

# Downloads
download_dir = r"D:\Career\Learning\Python\Projects\OCI_GCP"
download_dir += f'{chr(92)}{oci_bucket_name}'
log_file = r'D:\Career\Learning\Python\Projects\OCI_GCP\Logs\Migration.log'
inp_audit_file = r'D:\Career\Learning\Python\Projects\OCI_GCP\Audit\inp_Audit.csv'
out_audit_file = r'D:\Career\Learning\Python\Projects\OCI_GCP\Audit\out_Audit.csv'
inp_audit_header = ['OCS_FILE_NAME',
                    'MD5',
                    'SIZE']
out_audit_header = ['OCS_FILE_NAME',
                    'MD5',
                    'SIZE',
                    'DOWNLOAD_START_DATE',
                    'DOWNLOAD_END_DATE',
                    'DOWNLOAD_SIZE']
chunk_size = 2048 ** 2

# Uploads
upload_dir = r"D:\Series" + \
    chr(92)
multi_part_size = 200 * 1024 * 1024  # 3 MB
upload_audit = r'D:\Career\Learning\Python\Projects\OCI_GCP\Audit\upload_audit.csv'
out_upload_audit = r'D:\Career\Learning\Python\Projects\OCI_GCP\Audit\out_upload_audit.csv'
upload_audit_fields = ['FILE', 'SIZE', 'MD5']
base_url = 'https://objectstorage.us-ashburn-1.oraclecloud.com'
out_upload_audit_header = ['FILE', 'SIZE', 'MD5',
                           'UPLOAD_START_TIME', 'UPLOAD_END_TIME', 'DURATION', 'RESPONSE']
