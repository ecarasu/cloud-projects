import requests
import config
import os
from urllib.parse import quote

# Set the pre-authenticated URL and file path
file_path = r'D:\Career\Learning\Python\Projects\OCI_GCP\WiFi-22.180.0-Driver64-Win10-Win11.exe'
print(file_path.replace(config.upload_dir, ""))
pre_auth_url = config.ocs_pre_auth_url + \
    quote(file_path.replace(config.upload_dir, ""), safe='')

print(pre_auth_url)
# Set the chunk size (in bytes) for each part
chunk_size = 1024 * 1024 * 10  # 10 MB

# Open the file and get its total size
with open(file_path, 'rb') as f:
    file_size = os.path.getsize(file_path)

# Calculate the number of parts required
num_parts = file_size // chunk_size
if file_size % chunk_size != 0:
    num_parts += 1

print(num_parts)

# Set the headers for the initial POST request
headers = {'Content-Type': 'application/octet-stream'}
data = {'parts': []}

# Send the initial POST request to create the upload session and get the upload ID
response = requests.post(pre_auth_url, headers=headers, json=data)
if response.status_code != requests.codes.ok:
    print(
        f"Error creating upload session. Status code: {response.status_code}")
    print(response.json())


# Get the upload ID from the response
upload_id = response.json()['uploadId']

# Upload each part of the file
with open(file_path, 'rb') as f:
    for i in range(num_parts):
        # Read the chunk of data from the file
        chunk = f.read(chunk_size)

        # Set the headers for the PUT request for this part
        headers = {'Content-Type': 'application/octet-stream',
                   'Content-Length': str(len(chunk))}
        url = f"{pre_auth_url}&partNumber={i+1}&uploadId={upload_id}"

        # Send the PUT request to upload the part
        response = requests.put(url, data=chunk, headers=headers)

        # Add the part number and ETag to the data for the final POST request
        data['parts'].append(
            {'partNumber': i+1, 'ETag': response.headers['ETag']})

# Set the headers for the final POST request
headers = {'Content-Type': 'application/json'}
url = f"{pre_auth_url}&uploadId={upload_id}"

# Send the final POST request to complete the multipart upload
response = requests.post(url, headers=headers, json=data)

# Check the response status code
if response.status_code == requests.codes.ok:
    print(f"File uploaded successfully to {pre_auth_url}")
else:
    print(
        f"Error uploading file to {pre_auth_url}. Status code: {response.status_code}")
