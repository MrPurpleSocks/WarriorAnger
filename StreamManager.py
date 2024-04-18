import os
import obsws_python as obs
from dotenv import load_dotenv
import time
import base64
import requests
import shutil

load_dotenv()

def countDown(client: obs.ReqClient, t):
    #client.set_current_program_scene("PreMatch")
    while t:
        if t == 300:
            print("5 Min Warning!")
        if t == 60:
            print("1 Min Warning")
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        client.set_input_settings("CountDown", {"text": timer}, True)
        time.sleep(1)
        t -= 1
    client.set_current_program_scene("Primary")

def teamIcon(team):
    file = os.getenv("ICON_FOLDER") + "FRC_ICONS/" + team + ".png"
    folder = os.getenv("ICON_FOLDER") + "FRC_ICONS/"
    url = "https://www.thebluealliance.com/api/v3/team/frc" + team + "/media/2024"
    token = os.getenv("TBA_TOKEN")
    media = requests.get(url, headers={"X-TBA-Auth-Key": token})
    media = media.json()
    try:
        base64Icon = media[0]["details"]["base64Image"]
        base64Icon = bytes(base64Icon, 'utf-8')
        if not os.path.exists(file):
            if not os.path.exists(folder):
                print("FRC_ICONS folder does not exist, creating it")
                os.mkdir(folder)
                with open(file, 'wb') as icon:
                    icon.write(base64.decodebytes(base64Icon))
                return file
            else:
                print("Missing team icon, adding to folder")
                with open(file, 'wb') as icon:
                    icon.write(base64.decodebytes(base64Icon))
                return file
        else:
            return file
    except:
        if not os.path.exists(os.getenv("ICON_FOLDER") + "/FRC_ICONS/DEFAULT.png"):
            if not os.path.exists(os.getenv("ICON_FOLDER") + "/FRC_ICONS/"):
                print("FRC_ICONS folder does not exist, creating it")
                os.mkdir(folder)
                shutil.copy("C:/Users/wooll/Downloads/default_icon.png", folder + "DEFAULT.png")
                return folder + "DEFAULT.png"
            else:
                shutil.copy("C:/Users/wooll/Downloads/default_icon.png", folder + "DEFAULT.png")
                return folder + "DEFAULT.png"


def updateMatch(client: obs.ReqClient, match, teamList):
    match = match[10:]
    if len(match) == 1:
        match = "Qual-0" + match
    else:
        match = "Qual-" + match
    matchResp = client.set_input_settings("MatchNum", {"text": match}, True)
    r1Resp = client.set_input_settings("Red1", {"text": teamList[0]}, True)
    r1aResp = client.set_input_settings("Red1Icon", {"file": teamIcon(teamList[0])}, True)
    r2Resp = client.set_input_settings("Red2", {"text": teamList[1]}, True)
    r1aResp = client.set_input_settings("Red2Icon", {"file": teamIcon(teamList[1])}, True)
    r3Resp = client.set_input_settings("Red3", {"text": teamList[2]}, True)
    r1aResp = client.set_input_settings("Red3Icon", {"file": teamIcon(teamList[2])}, True)
    b1Resp = client.set_input_settings("Blue1", {"text": teamList[3]}, True)
    r1aResp = client.set_input_settings("Blue1Icon", {"file": teamIcon(teamList[3])}, True)
    b2Resp = client.set_input_settings("Blue2", {"text": teamList[4]}, True)
    r1aResp = client.set_input_settings("Blue2Icon", {"file": teamIcon(teamList[4])}, True)
    b3Resp = client.set_input_settings("Blue3", {"text": teamList[5]}, True)
    r1aResp = client.set_input_settings("Blue3Icon", {"file": teamIcon(teamList[5])}, True)