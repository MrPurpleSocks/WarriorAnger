import os
import time
import signal
import sys

import obsws_python as obs
from dotenv import load_dotenv

import GetMatches
import matchStatus
import testStuff

load_dotenv()

# counts number of recordings made
numFiles = 0
AutoDisplayed = False
MatchDisplayed = False

# connects to local OBS instance on port 4454
cl = obs.ReqClient(host=os.getenv("OBSWS_HOST"), port=os.getenv("OBSWS_PORT"), password=os.getenv("OBSWS_PASSWORD"), timeout=3)

path = os.getenv("ROOT_FOLDER") + "\\" + os.getenv("EVENT_KEY")
if not os.path.isdir(path):
    print(path + " Does Not Exist, Creating It")
    os.mkdir(path)
else:
    response = input(path + " Exists, do you want to use it? ")
    if response == "N" or response == "n":
        newFolder = input("Please enter a dir name")
        path = os.getenv("ROOT_FOLDER") + "\\" + newFolder
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

try:
    # Gets match keys in order from TBA
    # matches = GetMatches.all(os.getenv("EVENT_KEY"), os.getenv("TBA_TOKEN"))
    matches = testStuff.getTestMatches()

    for i in matches:
        cl.set_profile_parameter("Output", "FilenameFormatting", i)
        print("Match: ", i)
        print(" ")
        time.sleep(120)
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
            if round(cur_time-start) == 155 and not MatchDisplayed:
                print("Match End!")
                cl.stop_record()
                MatchDisplayed = True
                print("Delay to catch errors")
                time.sleep(30)
                print(" ")
                print(" ")
                break

        #reset
        MatchDisplayed = False
        AutoDisplayed = False
except:
    error_handler()
