import obsws_python as obs
import time
import os
import requests
import ffmpeg
import GetMatches
import OAuth
from dotenv import load_dotenv

load_dotenv()

main = OAuth.Client()
main.connect()

# counts number of recordings made
numFiles = 0

#Gets match keys in order from TBA
matches = GetMatches.all(os.getenv("EVENT_KEY"), os.getenv("TBA_TOKEN"))

# connects to local OBS instance on port 4454
cl = obs.ReqClient(host=os.getenv("OBSWS_HOST"), port=os.getenv("OBSWS_PORT"), password=os.getenv("OBSWS_PASSWORD"), timeout=3)

# testing filename change and start/stop
while numFiles != len(matches):
    currentTime = time.perf_counter()
    if currentTime - main.created() >= main.expires():
        main.refresh()

    #print(numFiles) # debug
    cl.set_profile_parameter("Output", "FilenameFormatting", matches[numFiles]) # changes file formatting
    cl.start_record()
    time.sleep(10)
    cl.stop_record()
    time.sleep(1)
    numFiles += 1