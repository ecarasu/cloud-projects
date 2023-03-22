import os
import requests
import config
from urllib.parse import quote


def splitFile(input_file: str, multi_part_size: int):
    with open(input_file, 'rb') as f:
        i = 1
        while True:
            part = f.read(multi_part_size)
            if not part:
                break
            output_file = '{}.{}'.format(input_file, i)
            with open(output_file, 'wb') as out:
                out.write(part)
            i += 1
    return(i)


chunk_size = 3 * 1024 * 1024

input_file = r"D:\Age of Empires III The Warchiefs Soundtrack - The Warchiefs Theme.mp4"

split_file(input_file, chunk_size)


url = config.ocs_pre_auth_url + \
    quote('Age of Empires III The Warchiefs Soundtrack - The Warchiefs Theme.mp4', safe='')

headers = {'opc-multipart': 'true'}

response = requests.put(url, headers=headers)

print(response.json()['accessUri'])

# url = 'https://objectstorage.us-ashburn-1.oraclecloud.com/p/OxZ47fcsRhQRxNqhPJzCpqvw23zqZQGV1L9nnLY-g3FzNgO223qo9mR77K2U1gpE/n/idmldytingzx/b/DWH-Load/u/large_random_data.csv/id/7f878479-00e1-4630-23b6-683deac88a78/1'
# data = open('x00', 'rb').read()
# headers = {
#     'Content-Type': 'application/octet-stream',
# }
# response = requests.put(url, headers=headers, data=data)
# print(response.text)
