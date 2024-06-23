'''
Uploads files to zipline instance
'''

import json
import os

import requests
from discord_webhook import DiscordEmbed, DiscordWebhook
from dotenv import load_dotenv

load_dotenv()


def video_upload(match: str, teams):
    '''
    Uploads a video to the zipline instance
    '''
    event = match[:7]
    file = f"C:\\Users\\wooll\\Downloads\\{event}\\"
    file += f"{match}-{teams[0]}_{teams[1]}_{teams[2]}-{teams[3]}_{teams[4]}_{teams[5]}.mp4"
    with open(file, 'rb') as f:
        multipart_form_data = {
        'file': (file, f, 'video/mp4')
        }
    headers = {
        "Authorization": os.getenv("ZIPLINE_TOKEN"),
        "Embed": "true",
        "Format": "NAME"
    }

    response = requests.post('http://anger.warriorb.org/api/upload', files=multipart_form_data,
                             headers=headers, timeout=5)

    response_json = response.json()

    description = f"Match {match} is available on WarriorAnger! "
    description += "you can view it at " + response_json['files'][0]

    notif = DiscordWebhook(url=os.getenv("DISCORD_WEBHOOK"))
    embed = DiscordEmbed(title="New Match Available!", description=description, color="014F8F")
    embed.set_footer(text="Operated By Patrick Woollvin")
    embed.set_timestamp()
    embed.add_embed_field(name="Red Alliance", value=f"{teams[0]}, {teams[1]}, {teams[2]}")
    embed.add_embed_field(name="Blue Alliance", value=f"{teams[3]}, {teams[4]}, {teams[5]}")

    notif.add_embed(embed)
    notif.execute()

    return response_json["files"][0]

def create_folders():
    '''
    Creates folders for each team in the zipline instance
    Isn't currently used, may be used in the future
    '''
    url = "https://www.thebluealliance.com/api/v3/event/" + os.getenv("EVENT_KEY") + "/teams/simple"
    teams = requests.get(url, headers={"X-TBA-Auth-Key": os.getenv("TBA_TOKEN")}, timeout=5)
    folders = {}
    print(teams.json())
    for i in teams.json():
        zipline = "http://anger.warriorb.org/api/user/folders"
        headers = {"Authorization": os.getenv("ZIPLINE_TOKEN")}
        body = {
            "name": os.getenv("EVENT_KEY") + "-" + str(i["team_number"]),
        }
        resp = requests.post(zipline, headers=headers, json=body, timeout=5)
        folders[i["team_number"]] = resp.json()["id"]

        requests.patch("http://anger.warriorb.org/api/user/folders/" + str(resp.json()["id"]),
                       headers=headers, json={"public": True}, timeout=5)

    json_object = json.dumps(folders, indent=4)
    with open(os.getenv("ROOT_FOLDER") + "/ziplineFolders.json", "w", encoding="utf-8") as outfile:
        outfile.write(json_object)

    return folders
