'''
Allows for a manual control of the match recording system.
Mainly for use with debugging or if the automatic system fails.
'''

import os

import obsws_python as obs
from dotenv import load_dotenv

import get_matches
import stream_manager

# ascii escape codes
LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'

# Loads Constants from the .env file
load_dotenv()

print("WarriorBorgs Match Record System")
print("Current Mode: Manual")
print("Event: " + os.getenv("EVENT_KEY"))
print("Last Match Played: " + os.getenv("LAST_MATCH"))
print("OBS Host: " + os.getenv("OBSWS_HOST"))
print("OBS Port: " + os.getenv("OBSWS_PORT"))
print("OBS Password: " + os.getenv("OBSWS_PASSWORD"))
input("Press return to continue")
print("Fetching Matches")

matches = get_matches.get_all(os.getenv("EVENT_KEY"), os.getenv("TBA_TOKEN"))

print("Connecting to OBS")
cl = obs.ReqClient(host=os.getenv("OBSWS_HOST"), port=os.getenv("OBSWS_PORT"),
                   password=os.getenv("OBSWS_PASSWORD"), timeout=3)

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
    input("Press Return On Match Start ")
    cl.start_record()
    input("Press Return On Match End ")
    cl.stop_record()
    #FileUpload.videoUpload(i, teams)
