import requests

url = 'https://objectstorage.us-ashburn-1.oraclecloud.com'
url += '/p/OH0pThZmn1i6GNS5VvTflorDz28LprIRmpWpJT2jWbdv3ey69MnhPl1cYFFVjdnC/n/idt88w6rh4ji/b/gcp_migration/u/Age%20of%20Empires%20III%20The%20Warchiefs%20Soundtrack%20-%20The%20Warchiefs%20Theme.mp4/id/1c4aaf32-d361-576c-f38d-09eb593b64c2/'


input_file = r'D:\Age of Empires III The Warchiefs Soundtrack - The Warchiefs Theme.mp4'


for i in range(1, 5):

    data = open(input_file+f'.{i}', 'rb').read()
    headers = {'Content-Type': 'application/octet-stream'}
    print(f'{url}{i}')
    response = requests.put(f'{url}{i}', headers=headers, data=data)
    print(response)


post_headers = {'Content-Type': 'application/json'}
post_response = requests.post(url, headers=post_headers)
print(post_response)
