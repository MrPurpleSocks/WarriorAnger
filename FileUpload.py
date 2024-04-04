import requests
from dotenv import load_dotenv
import os
from discord_webhook import DiscordWebhook, DiscordEmbed

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
    # DiscordResponse = notif.execute()

    return json["files"][0]
