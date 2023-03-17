import os
import requests
import config
from urllib.parse import quote


def split_file(input_file, chunk_size):
    with open(input_file, 'rb') as f:
        i = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            output_file = '{}.{}'.format(input_file, i)
            with open(output_file, 'wb') as out:
                out.write(chunk)
            i += 1


chunk_size = 250 * 1024 * 1024  # 250MB in bytes

input_file = r"D:\Rowdy_First_Birthday.mp4"

split_file(input_file, chunk_size)


url = config.ocs_pre_auth_url + \
    quote(input_file.replace(config.upload_dir, ""), safe='')

headers = {'opc-multipart': 'true'}

response = requests.put(url, headers=headers)

print(response.json())
