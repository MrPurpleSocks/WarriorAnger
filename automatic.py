import os

from websocket import create_connection
from json import loads
import obsws_python as obs
from dotenv import load_dotenv

import time
import get_matches
import stream_manager

# Loads Constants from the .env file
load_dotenv()

print("Connecting to OBS")
cl = obs.ReqClient(host=os.getenv("OBSWS_HOST"), port=os.getenv("OBSWS_PORT"),
                   password=os.getenv("OBSWS_PASSWORD"), timeout=3)

print("Getting Matches")
matches = get_matches.get_all(os.getenv("EVENT_KEY"), os.getenv("TBA_TOKEN"))

print("Connecting to Server")
ws = create_connection("wss://api.mrpurplesocks.hackclub.app/anger/client")

path = os.getenv("ROOT_FOLDER") + os.getenv("EVENT_KEY")
print("Checking for path")
if not os.path.isdir(path):
    print(path + " Does Not Exist, Creating It")
    os.mkdir(path)
    cl.set_record_directory(path)
else:
    print(path + " Exists")
    print("Note: double check that LAST_MATCH is set")
    cl.send("SetRecordDirectory", {"recordDirectory": path})

for i in matches:
    print()
    print(f"Match {i} Queued")
    print("Fetching Match Data")
    teams = get_matches.get_teams(i)
    print("Posting to OBS Scene")
    cl.set_current_program_scene("Trans")
    stream_manager.update_match(cl, i, teams)
    cl.set_current_program_scene("Primary")
    print("Updating File Name")
    file = f"{i}-{teams[0]}_{teams[1]}_{teams[2]}-{teams[3]}_{teams[4]}_{teams[5]}"
    cl.set_profile_parameter("Output", "FilenameFormatting", file)
    print("Stream Is Ready!")
    print(f"Red Alliance: {teams[0]} {teams[1]} {teams[2]}")
    print(f"Blue Alliance: {teams[3]} {teams[4]} {teams[5]}")

    # Wait for the server
    print("Waiting to recieve")
    result =  loads(ws.recv()) # Waits for json payload from server
    print("Recieved Payload")
    if not result["disregard"]:
        #tells us to record
        cl.start_record()
        time.sleep(210) # Waits for 3.5 minutes
        cl.stop_record()
        
    #FileUpload.videoUpload(i, teams)
        
ws.close()
print("closed")
