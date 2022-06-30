import requests


with open(r'D:\Career\AWS.pdf', 'rb') as f:
    data = f.read()

base_url = 'https://objectstorage.us-ashburn-1.oraclecloud.com'

# pre auth url
url = 'https://objectstorage.us-ashburn-1.oraclecloud.com/p/a-kmzCF7mlE6FW73SJmOFE2MaN4CCv4CTfafrrBJZMm5BeOZihQqbB6iuGsqubar/n/idt88w6rh4ji/b/gcp_migration/o/Career/AWS.pdf'
headers = {'opc-multipart': 'true'}

get_multipart_url = requests.put(url, headers=headers)
response = get_multipart_url.json()

# putting object in multipart URL
# logic for multipart should be added
requests.put(url=base_url+response['accessUri']+'1', data=data)

# commiting multi part upload
result = requests.post(url=base_url+response['accessUri'])

print(result.status_code)
