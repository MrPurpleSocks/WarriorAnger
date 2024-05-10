'''
Gets all matches for an event from The Blue Alliance API
'''

import os

import requests
from dotenv import load_dotenv

load_dotenv()

def get_all(event_key, token):
    '''
    Used to get all Qualification matches in an event
    returns: a list of the matches
    '''
    match_keys_url = "https://www.thebluealliance.com/api/v3/event/" + event_key + "/matches/keys"
    match_keys = requests.get(match_keys_url, headers={"X-TBA-Auth-Key": token}, timeout=5)
    keys = match_keys.json()
    first_ten = [event_key + "_qm1", event_key + "_qm2", event_key + "_qm3", event_key + "_qm4",
                event_key + "_qm5", event_key + "_qm6", event_key + "_qm7", event_key + "_qm8",
                event_key + "_qm9", event_key + "_qm10", ]
    if keys[0] == event_key + "_f1m1":
        keys.pop(0)
        keys.pop(0)
        keys.pop(0)
    for i in range(10):
        keys.remove(first_ten[i])
    keys = first_ten + keys
    previous = os.getenv("LAST_MATCH")
    if previous:
        indice = keys.index(previous)
        del keys[:indice + 1]
    return keys

def get_teams(match):
    '''
    Used to get the teams in a match
    returns: a list of the teams in the match
    '''
    url = f"https://www.thebluealliance.com/api/v3/match/{match}/simple"
    teams_request = requests.get(url, headers={"X-TBA-Auth-Key": os.getenv("TBA_TOKEN")}, timeout=5)
    teams = teams_request.json()
    just_the_teams = []
    just_the_teams += teams["alliances"]["red"]["team_keys"]
    just_the_teams += teams["alliances"]["blue"]["team_keys"]

    for i, thing in enumerate(just_the_teams):
        thing=thing[0:] # it complains about it not being used, so i "used" it
        team = just_the_teams[i]
        team = team[3:]
        just_the_teams[i] = team

    return just_the_teams
