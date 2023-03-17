import upload_to_gcs
import download_from_ocs_api
import config
import datetime
import csv


folders = download_from_ocs_api.createAuditFile(
    config.ocs_pre_auth_url, config.ocs_url_fields, config.inp_audit_file, config.inp_audit_header)

download_from_ocs_api.makeDirectory(folders, config.download_dir)
download_from_ocs_api.download_from_oci_bucket(config.ocs_pre_auth_url, config.download_dir,
                                               config.inp_audit_file, config.out_audit_file, config.out_audit_header, config.chunk_size)
