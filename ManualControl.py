# Allows for manual control of recording

from dotenv import load_dotenv
import os
import GetMatches
import FileUpload
import obsws_python as obs
import StreamManager

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

matches = GetMatches.all(os.getenv("EVENT_KEY"), os.getenv("TBA_TOKEN"))

print("Connecting to OBS")
cl = obs.ReqClient(host=os.getenv("OBSWS_HOST"), port=os.getenv("OBSWS_PORT"), password=os.getenv("OBSWS_PASSWORD"), timeout=3)

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
    print("Match {} Queued".format(i))
    print("Fetching Match Data")
    teams = GetMatches.getTeams(i)
    print("Posting to OBS Scene")
    cl.set_current_program_scene("Trans")
    StreamManager.updateMatch(cl, i, teams)
    cl.set_current_program_scene("Primary")
    print("Updating File Name")
    file = "{}-{}_{}_{}-{}_{}_{}".format(i, teams[0], teams[1], teams[2], teams[3], teams[4], teams[5])
    cl.set_profile_parameter("Output", "FilenameFormatting", file)
    print("Stream Is Ready!")
    print("Red Alliance: {} {} {}, Blue Alliance: {} {} {}". format(teams[0], teams[1], teams[2], teams[3], teams[4], teams[5]))
    input("Press Return On Match Start ")
    cl.start_record()
    input("Press Return On Match End ")
    cl.stop_record()
    FileUpload.videoUpload(i, teams)
