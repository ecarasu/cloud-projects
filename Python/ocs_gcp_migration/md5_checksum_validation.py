import hashlib
import base64


def md5_checksum_validation(filename: str, md5_value: str, chunk_size: int):
    hash_file = hashlib.md5()
    with open(filename, 'rb') as file_to_check:
        for chunk in iter(lambda: file_to_check.read(chunk_size), b''):
            hash_file.update(chunk)
        return (base64.b64encode(hash_file.digest()).decode() == md5_value)
