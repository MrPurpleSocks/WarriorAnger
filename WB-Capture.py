import os
import time
import signal
import sys

import obsws_python as obs
from dotenv import load_dotenv

import GetMatches
import matchStatus

load_dotenv()

# counts number of recordings made
numFiles = 0
AutoDisplayed = False
MatchDisplayed = False

# connects to local OBS instance on port 4454
cl = obs.ReqClient(host=os.getenv("OBSWS_HOST"), port=os.getenv("OBSWS_PORT"), password=os.getenv("OBSWS_PASSWORD"), timeout=3)

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
    matches = GetMatches.all(os.getenv("EVENT_KEY"), os.getenv("TBA_TOKEN"))

    for i in matches:
        print("Queuing ", i)
        if matchStatus.waitForStart():
            print("Match Started!")
            start = time.perf_counter()
            print("Started Recording")
            cl.toggle_record()

        while True:
            cur_time = time.perf_counter()
            if round(cur_time-start) == 15 and not AutoDisplayed:
                print("End of Auto")
                AutoDisplayed = True
            if round(cur_time-start) == 155 and not MatchDisplayed:
                print("Match End!")
                cl.toggle_record()
                MatchDisplayed = True
                break

        #reset
        MatchDisplayed = False
        AutoDisplayed = False
except:
    error_handler()
