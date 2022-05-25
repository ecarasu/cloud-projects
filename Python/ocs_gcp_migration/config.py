oci_bucket_name = 'gcp_migration'
gcp_bucket_name = 'oci-migration-2022'
download_dir = f'D:{chr(92)}{oci_bucket_name}'
gcs_service_account_credentials = r''
log_file = r''
chunk_size = 2048 ** 2
audit_header = ['OCS_FILE_NAME',
                'SIZE',
                'DOWNLOAD_START_DATE',
                'DOWNLOAD_START_TIME',
                'DOWNLOAD_END_DATE',
                'DOWNLOAD_END_TIME',
                'DOWNLOAD_PERCENTAGE']
audit_file = r''
