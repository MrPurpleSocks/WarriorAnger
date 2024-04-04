import requests
from dotenv import load_dotenv
import os

load_dotenv()

def all(eventKey, token):
    matchKeysUrl = "https://www.thebluealliance.com/api/v3/event/" + eventKey + "/matches/keys"
    matchKeys = requests.get(matchKeysUrl, headers={"X-TBA-Auth-Key": token})
    keys = matchKeys.json()
    firstTen = [eventKey + "_qm1", eventKey + "_qm2", eventKey + "_qm3", eventKey + "_qm4", eventKey + "_qm5",
                eventKey + "_qm6", eventKey + "_qm7", eventKey + "_qm8", eventKey + "_qm9", eventKey + "_qm10", ]
    if keys[0] == eventKey + "_f1m1":
        keys.pop(0)
        keys.pop(0)
        keys.pop(0)
    for i in range(10):
        keys.remove(firstTen[i])
    keys = firstTen + keys
    previous = os.getenv("LAST_MATCH")
    if previous:
        indice = keys.index(previous)
        del keys[:indice + 1]
    return keys

def getTeams(match):
    url = "https://www.thebluealliance.com/api/v3/match/{}/simple".format(match)
    teamsRequest = requests.get(url, headers={"X-TBA-Auth-Key": os.getenv("TBA_TOKEN")})
    teams = teamsRequest.json()
    justTheTeams = []
    justTheTeams += teams["alliances"]["red"]["team_keys"]
    justTheTeams += teams["alliances"]["blue"]["team_keys"]

    for i in range(len(justTheTeams)):
        team = justTheTeams[i]
        team = team[3:]
        justTheTeams[i] = team

    return justTheTeams
