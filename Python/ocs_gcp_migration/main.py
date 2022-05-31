import upload_to_gcs
import download_from_ocs_api
import config
import datetime
import csv

download_from_ocs_api.download_from_oci_bucket(config.ocs_pre_auth_url, config.ocs_url_fields,
                                               config.download_dir, config.inp_audit_file, config.out_audit_file, config.out_audit_header, config.chunk_size)


# upload_to_gcs.upload_to_gcp_from_directory(
#     config.download_dir, config.gcp_bucket_name)
