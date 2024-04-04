import requests
from dotenv import load_dotenv
import os

load_dotenv()
def videoUpload(match: str):
    file = os.getenv("ROOT_FOLDER") + "/" + match + ".mp4"
    multipart_form_data = {
        'file': ('3256.png', open('C:/Users/wooll/Downloads/CdrUZC.mp4', 'rb'), 'video/mp4')
    }
    headers = {
        "Authorization": os.getenv("ZIPLINE_TOKEN"),
        "Embed": "true"
    }

    response = requests.post('http://anger.warriorb.org/api/upload', files=multipart_form_data, headers=headers)

    json = response.json()
    return json["files"][0]
videoUpload()
