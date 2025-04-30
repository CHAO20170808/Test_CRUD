import requests
import mohawk
import time

hawk_id = '8577961'
hawk_key = '3r45e4b8-9f3c-4a2d-8f1d-2f5b7c9a6e0d'
hawk_algorithm = 'sha256'
user_id_to_read = 1
api_url = f'http://localhost:5000/api/users/{user_id_to_read}'
method = 'GET'
content = b''  # GET 請求通常沒有內容
content_type = ''
url_path = f'/api/users/{user_id_to_read}'

credentials = {'id': hawk_id, 'key': hawk_key, 'algorithm': hawk_algorithm}

hawk = mohawk.Sender(credentials, api_url, method, content=content, content_type=content_type)
headers = {'Authorization': hawk.request_header}

response = requests.get(api_url, headers=headers)

print(response.status_code)
print(response.json())