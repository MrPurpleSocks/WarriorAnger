import requests
from dotenv import load_dotenv
import os
from discord_webhook import DiscordWebhook, DiscordEmbed
import json

load_dotenv()


def videoUpload(match: str, teams):
    match = "qm" + match[12:]
    file = (os.getenv("ROOT_FOLDER") + os.getenv("EVENT_KEY") + "/{}-{}_{}_{}-{}_{}_{}.mp4".format(match, teams[0],
                                                                                                   teams[1], teams[2],
                                                                                                   teams[3],
                                                                                                   teams[4], teams[5]))
    multipart_form_data = {
        'file': (file, open(file, 'rb'), 'video/mp4')
    }
    headers = {
        "Authorization": os.getenv("ZIPLINE_TOKEN"),
        "Embed": "true",
        "Format": "NAME"
    }

    response = requests.post('http://anger.warriorb.org/api/upload', files=multipart_form_data, headers=headers)

    headers2 = {
        "Authorization": os.getenv("ZIPLINE_TOKEN"),
    }
    getID = requests.get("http://anger.warriorb.org/api/user/recent", data={"take": "1"}, headers=headers2)
    fileID = getID.json()[0]["id"]
    print(fileID)

    folderThing = requests.post("http://anger.warriorb.org/api/user/folders/" + os.getenv("ZIPLINE_FOLDER"),
                                data={"file": str(fileID)}, headers=headers2)

    json = response.json()
    json2 = folderThing.json()

    notif = DiscordWebhook(url=os.getenv("DISCORD_WEBHOOK"))
    embed = DiscordEmbed(title="New Match Available!",
                         description="Match {} is available on WarriorAnger! you can view it at {} . View other matches at http://anger.warriorb.org/folder/5".format(
                             match, json["files"][0]), color="014F8F")
    embed.set_footer(text="Video may take up to 30 secs to process")
    embed.set_timestamp()
    embed.add_embed_field(name="Red Alliance", value="{}, {}, {}".format(teams[0], teams[1], teams[2]))
    embed.add_embed_field(name="Blue Alliance", value="{}, {}, {}".format(teams[3], teams[4], teams[5]))

    notif.add_embed(embed)
    DiscordResponse = notif.execute()

    return json["files"][0]

def createFolders():
    url = "https://www.thebluealliance.com/api/v3/event/" + os.getenv("EVENT_KEY") + "/teams/simple"
    teams = requests.get(url, headers={"X-TBA-Auth-Key": os.getenv("TBA_TOKEN")})
    folders = {}
    print(teams.json())
    for i in teams.json():
        zipline = "http://anger.warriorb.org/api/user/folders"
        headers = {"Authorization": os.getenv("ZIPLINE_TOKEN")}
        body = {
            "name": os.getenv("EVENT_KEY") + "-" + str(i["team_number"]),
        }
        resp = requests.post(zipline, headers=headers, json=body)
        folders[i["team_number"]] = resp.json()["id"]

        newResp = requests.patch("http://anger.warriorb.org/api/user/folders/" + str(resp.json()["id"]), headers=headers, json={"public": True})

    json_object = json.dumps(folders, indent=4)
    with open(os.getenv("ROOT_FOLDER") + "/ziplineFolders.json", "w") as outfile:
        outfile.write(json_object)

    return folders

def delete():
    folders = {114: 188, 1160: 189, 1458: 190, 1678: 191, 1700: 192, 199: 193, 2204: 194, 2288: 195, 254: 196, 2637: 197, 2854: 198, 3045: 199, 3256: 200, 3482: 201, 4159: 202, 4186: 203, 4255: 204, 4669: 205, 4698: 206, 4904: 207, 4973: 208, 4990: 209, 5274: 210, 5419: 211, 5430: 212, 5507: 213, 581: 214, 5940: 215, 5985: 216, 6059: 217, 6238: 218, 6418: 219, 649: 220, 6619: 221, 6814: 222, 6884: 223, 7137: 224, 7245: 225, 7401: 226, 7419: 227, 751: 228, 766: 229, 7667: 230, 7729: 231, 7840: 232, 8045: 233, 8159: 234, 841: 235, 8793: 236, 8852: 237, 9038: 238, 9111: 239, 9202: 240, 9470: 241, 9519: 242, 9545: 243, 9609: 244, 9634: 245, 972: 246, 9781: 247}
    headers = {"Authorization": os.getenv("ZIPLINE_TOKEN")}
    for i in folders:
        print("http://anger.warriorb.org/api/user/folders/" + str(folders[i]))
        resp = requests.delete("http://anger.warriorb.org/api/user/folders/" + str(folders[i]), headers=headers, json={"deleteFolder": "false"})
        print(resp.json())

print(createFolders())
#delete()
