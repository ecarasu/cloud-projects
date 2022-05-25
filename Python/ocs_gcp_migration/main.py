import upload_to_gcs
import download_from_ocs
import config


download_from_ocs.download_from_oci_bucket(
    config.oci_bucket_name, config.download_dir, audit_file=config.audit_file)


# upload_to_gcs.upload_to_gcp_from_directory(
#     config.download_dir, config.gcp_bucket_name)
