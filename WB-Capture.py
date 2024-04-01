import os
import time

import obsws_python as obs
from dotenv import load_dotenv

import GetMatches
import matchStatus

load_dotenv()

# counts number of recordings made
numFiles = 0

# Gets match keys in order from TBA
matches = GetMatches.all(os.getenv("EVENT_KEY"), os.getenv("TBA_TOKEN"))

# connects to local OBS instance on port 4454
cl = obs.ReqClient(host=os.getenv("OBSWS_HOST"), port=os.getenv("OBSWS_PORT"), password=os.getenv("OBSWS_PASSWORD"), timeout=3)

for i in matches:
    print("Match Queuing")
    if matchStatus.waitForStart():
        print("Match Started!")
        start = time.perf_counter()
        print("Started timer")
    while True:
        cur_time = time.perf_counter()
        print(cur_time-start)
        if cur_time-start == 15:
            print("End of Auto")
        if cur_time-start == 150:
            print("Match End!")
