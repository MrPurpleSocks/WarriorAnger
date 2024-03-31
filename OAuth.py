import requests
from dotenv import load_dotenv
import os
import time

# Load .env vars
load_dotenv()

class Client:
    def __init__(self):
        self.id = os.getenv("G_CLIENT_ID")
        self.secret = os.getenv("G_CLIENT_SECRET")
    def connect(self):
        data = "client_id=" + self.id + "&scope=email&20profile"
        url = "https://oauth2.googleapis.com/device/code"
        initResponse = requests.post(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        initResponse = initResponse.json()

        deviceCode = initResponse["device_code"]
        user_code = initResponse["user_code"]
        expires = initResponse["expires_in"]
        interval = initResponse["interval"]
        user_url = initResponse["verification_url"]

        print(" ")
        print("Connected to Google OAuth 2.0!")
        print("Visit " + user_url + " on a device and enter the following code:")
        print(user_code)
        print(" ")
        print("Code expires in " + str(int(expires)/60) + " mins")

        # poll google if user signed in every {interval} seconds
        startTime = time.perf_counter()
        while True:
            currentTime = time.perf_counter()
            if currentTime - startTime >= int(expires):
                raise RuntimeError("Google OAuth Timeout")
                return False
            time.sleep(int(interval))
            data = "client_id=" + self.id + "&client_secret=" + self.secret + "&device_code=" + deviceCode + "&grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Adevice_code"
            url = "https://oauth2.googleapis.com/token"
            pollResponse = requests.post(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
            pollData = pollResponse.json()
            if int(pollResponse.status_code) == 200:
                self.created = time.perf_counter()
                self.expires = int(pollData["expires_in"])
                self.access = pollData['access_token']
                self.refresh = pollData['refresh_token']
                break
    def refresh(self):
        url = "https://oauth2.googleapis.com/token"
        data = "client_id=" + self.id + "&client_secret=" + self.secret + "&refresh_token=" + self.refresh + "&grant_type=refresh_token"
        refreshResponse = requests.post(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        refreshData = refreshResponse.json()
        if refreshResponse.status_code == 200:
            self.access = refreshData["access_token"]
            return 0
        else:
            return 1

    def revoke(self):
        url = "https://oauth2.googleapis.com/revoke?token=" + self.access
        revokeResponse = requests.post(url, headers={"Content-Type": "application/x-www-form-urlencoded"})
        if revokeResponse.status_code == 200:
            return 0
        else:
            return 1

    def access_token(self):
        return self.access

    def token_created(self):
        return self.created

    def expires(self):
        return self.expires