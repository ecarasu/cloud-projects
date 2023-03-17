import requests
import config
from urllib.parse import quote

# Set the pre-authenticated URL and file path

file_path = r'D:\Career\Learning\Python\Projects\OCI_GCP\WiFi-22.180.0-Driver64-Win10-Win11.exe'
print(file_path.replace(config.upload_dir, ""))
pre_auth_url = config.ocs_pre_auth_url + \
    quote(file_path.replace(config.upload_dir, ""), safe='')


# Read the file contents
with open(file_path, 'rb') as f:
    file_content = f.read()

# Set the headers
headers = {'Content-Type': 'application/octet-stream',
           'Content-Length': str(len(file_content))}

# Send the PUT request to upload the file
response = requests.put(pre_auth_url, data=file_content, headers=headers)

# Check the response status codemu
if response.status_code == requests.codes.ok:
    print(f"File uploaded successfully to {pre_auth_url}")
else:
    print(
        f"Error uploading file to {pre_auth_url}. Status code: {response.status_code}")
