import os
import time
import signal
import sys

import obsws_python as obs
from dotenv import load_dotenv

import GetMatches
import matchStatus
import testStuff
import FileUpload
import StreamManager

load_dotenv()

# counts number of recordings made
numFiles = 0
AutoDisplayed = False
MatchDisplayed = False

# connects to local OBS instance on port 4454
cl = obs.ReqClient(host=os.getenv("OBSWS_HOST"), port=os.getenv("OBSWS_PORT"), password=os.getenv("OBSWS_PASSWORD"), timeout=3)

path = os.getenv("ROOT_FOLDER") + os.getenv("EVENT_KEY")
if not os.path.isdir(path):
    print(path + " Does Not Exist, Creating It")
    os.mkdir(path)
else:
    response = input(path + " Exists, do you want to use it? ")
    if response == "N" or response == "n":
        newFolder = input("Please enter a dir name")
        path = os.getenv("ROOT_FOLDER") + newFolder
        path = path.replace("/", "\\")
        os.mkdir(path)
    cl.send("SetRecordDirectory", {"recordDirectory": path})
def signal_handler(sig, frame):
    print("Ctrl+C Pressed!")
    print("Exiting gracefully")
    cl.set_current_program_scene("brb")
    time.sleep(1)
    if resp.output_active:
        cl.stop_record()
        print("Stopped Recording")
    else:
        print("OBS Wasn't recording")
    sys.exit(0)
def error_handler():
    print("Code Exited Code 1!")
    print("Exiting gracefully")
    cl.set_current_program_scene("brb 2")
    time.sleep(1)
    resp = cl.get_record_status()
    if resp.output_active:
        cl.stop_record()
        print("Stopped Recording")
    else:
        print("OBS Wasn't recording")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

#try:
matches = GetMatches.all(os.getenv("EVENT_KEY"), os.getenv("TBA_TOKEN"))

for i in matches:
    print("Match: ", i)
    print(" ")
    teams = GetMatches.getTeams(i)
    fileMatch = i[10:]
    file = "{}-{}_{}_{}-{}_{}_{}".format(fileMatch, teams[0], teams[1], teams[2], teams[3], teams[4], teams[5])
    cl.set_profile_parameter("Output", "FilenameFormatting", file)
    StreamManager.updateMatch(cl, i, teams)
    print("Stream Ready!")
    print("Waiting for field to clear")
    if matchStatus.waitForClear():
        print("Waiting for match to start")
        if matchStatus.waitForStart():
            print("Match Started!")
            start = time.perf_counter()
            cl.toggle_record()
            print("Started Recording")

    while True:
        cur_time = time.perf_counter()
        if round(cur_time-start) == 10 and not MatchDisplayed:  # Set to 165
            print("Match End!")
            cl.stop_record()
            print("File saved as {}.mp4".format(file))
            time.sleep(5)
            FileUpload.videoUpload(i, teams)
            MatchDisplayed = True
            print("Delay to catch errors")
            time.sleep(120)
            print("Advancing to next match")
            print(" ")
            print(" ")
            break

    #reset
    MatchDisplayed = False
#except:
   # error_handler()
