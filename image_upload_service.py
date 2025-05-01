import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

def encode_string_to_base64(input_string: str) -> str:
    encoded_bytes = base64.b64encode(input_string.encode('utf-8'))
    return encoded_bytes.decode('utf-8')


def image_upload(file_obj, filename):
    url = 'https://upload.imagekit.io/api/v1/files/upload'
    
    api_key = os.getenv('IMAGEKIT_API_KEY')
        
    auth_string = api_key + ':'
    base64_auth = encode_string_to_base64(auth_string)
    
    headers = {
        'Authorization': f'Basic {base64_auth}',
    }
    
    data = {
        'fileName': filename,
        'folder':'/lost-found-images',
    }

    files = {
        'file': file_obj
    }

    response = requests.post(
        url,
        headers=headers,
        files=files,
        data=data,
    )

    if response.status_code == 200:
        return response.json()
    else:
        return None


