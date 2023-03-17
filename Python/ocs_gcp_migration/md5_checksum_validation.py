import hashlib
import base64
import mmap


def getMd5(filename: str):
    with open(filename, 'rb') as file_to_check:
        with mmap.mmap(file_to_check.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
            md5_hash = hashlib.md5(mmapped_file).digest()
            md5_base64 = base64.b64decode(md5_hash).decode()
            return md5_base64
