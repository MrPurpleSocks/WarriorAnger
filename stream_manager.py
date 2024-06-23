'''
Handles all the OBS interactions for the stream
'''

import base64
import os
import shutil
import time

import obsws_python as obs
import requests
from dotenv import load_dotenv

load_dotenv()

def count_down(obs_client: obs.ReqClient, t):
    '''
    Starts a countdown timer in OBS
    and switches to it. returns 1 if successful
    '''

    #obs_client.set_current_program_scene("PreMatch")
    while t:
        if t == 300:
            print("5 Min Warning!")
        if t == 60:
            print("1 Min Warning")
        mins, secs = divmod(t, 60)
        timer = f'{mins}:{secs}'
        obs_client.set_input_settings("CountDown", {"text": timer}, True)
        time.sleep(1)
        t -= 1
    obs_client.set_current_program_scene("Primary")

    return 1

def team_icon(team):
    '''
    Get the icon for a team and adds it to a folder and returns it
    '''
    file = os.getenv("ICON_FOLDER") + "FRC_ICONS/" + team + ".png"
    folder = os.getenv("ICON_FOLDER") + "FRC_ICONS/"
    url = "https://www.thebluealliance.com/api/v3/team/frc" + team + "/media/2024"
    token = os.getenv("TBA_TOKEN")
    media = requests.get(url, headers={"X-TBA-Auth-Key": token}, timeout=9)
    media = media.json()
    try:
        base_64_icon = media[0]["details"]["base64Image"]
        base_64_icon = bytes(base_64_icon, 'utf-8')
        if not os.path.exists(file):
            if not os.path.exists(folder):
                print("FRC_ICONS folder does not exist, creating it")
                os.mkdir(folder)
                with open(file, 'wb') as icon:
                    icon.write(base64.decodebytes(base_64_icon))
                return file
            print("Missing team icon, adding to folder")
            with open(file, 'wb') as icon:
                icon.write(base64.decodebytes(base_64_icon))
            return file
        return file
    except IndexError:  # Add exception type IndexError
        if not os.path.exists(os.getenv("ICON_FOLDER") + "/FRC_ICONS/DEFAULT.png"):
            if not os.path.exists(os.getenv("ICON_FOLDER") + "/FRC_ICONS/"):
                print("FRC_ICONS folder does not exist, creating it")
                os.mkdir(folder)
                shutil.copy("C:/Users/wooll/Downloads/default_icon.png", folder + "DEFAULT.png")
                return folder + "DEFAULT.png"
            shutil.copy("C:/Users/wooll/Downloads/default_icon.png", folder + "DEFAULT.png")
            return folder + "DEFAULT.png"

    return 1


def update_match(obs_client: obs.ReqClient, match, team_list):
    '''
    Updates OBS settings for a match, returns 1 if successful
    '''

    match = match[10:]
    if len(match) == 1:
        match = "Qual-0" + match
    else:
        match = "Qual-" + match
    obs_client.set_input_settings("MatchNum", {"text": match}, True)
    obs_client.set_input_settings("Red1", {"text": team_list[0]}, True)
    obs_client.set_input_settings("Red1Icon", {"file": team_icon(team_list[0])}, True)
    obs_client.set_input_settings("Red2", {"text": team_list[1]}, True)
    obs_client.set_input_settings("Red2Icon", {"file": team_icon(team_list[1])}, True)
    obs_client.set_input_settings("Red3", {"text": team_list[2]}, True)
    obs_client.set_input_settings("Red3Icon", {"file": team_icon(team_list[2])}, True)
    obs_client.set_input_settings("Blue1", {"text": team_list[3]}, True)
    obs_client.set_input_settings("Blue1Icon", {"file": team_icon(team_list[3])}, True)
    obs_client.set_input_settings("Blue2", {"text": team_list[4]}, True)
    obs_client.set_input_settings("Blue2Icon", {"file": team_icon(team_list[4])}, True)
    obs_client.set_input_settings("Blue3", {"text": team_list[5]}, True)
    obs_client.set_input_settings("Blue3Icon", {"file": team_icon(team_list[5])}, True)
    return 1
