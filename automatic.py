

import os

from websocket import create_connection
from json import loads
import obsws_python as obs
from dotenv import load_dotenv

# Loads Constants from the .env file
load_dotenv()

ws = create_connection("wss://api.mrpurplesocks.hackclub.app/anger/client")
for i in range(2): # NOTE: Temporary, will be replaced with a while loop
    print("Waiting to recieve")
    result =  loads(ws.recv()) # Waits for json payload from server
    print("Recieved Payload")
    if not result["disregard"]:
        matchHappening = ""
        for match in result["matches"]: # Finds the match that is currently happening
            if match["status"] == "On field":
                matchHappening = match["label"]
    else: # Certain actions are recieved 2-4 times, and the server marks them to be disregarded
        print("Disregarded")
        break
    print(f'Match on field: {matchHappening}')
ws.close()
print("closed")