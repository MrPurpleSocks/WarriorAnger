'''
main file to be executed to run the program

THIS IS BROKEN RIGHT NOW, IT WILL BE FIXED
'''

import os
import time
import signal
import sys

import obsws_python as obs
from dotenv import load_dotenv

import get_matches
import file_upload
import stream_manager

if __name__ == "__main__":

    # THIS FILE IS DEPRECATED, DO NOT USE
    # IT IS OUT OF DATE AND WILL NOT WORK
    # WILL PROBABLY BE REMOVED IN THE FUTURE

    # Warning message
    print("********************************")
    print("*           WARNING!           *")
    print("*       FILE DEPRECATED        *")
    print("*          DO NOT USE          *")
    print("********************************")

    load_dotenv()

    MATCH_DISPLAYED = False

    # connects to local OBS instance on port 4454
    cl = obs.ReqClient(host=os.getenv("OBSWS_HOST"), port=os.getenv("OBSWS_PORT"),
                       password=os.getenv("OBSWS_PASSWORD"), timeout=3)

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
    def signal_handler():
        '''
        Handles the Ctrl+C signal
        returns: nothing
        '''
        print("Ctrl+C Pressed!")
        print("Exiting gracefully")
        cl.set_current_program_scene("brb")
        time.sleep(1)
        resp = cl.get_record_status()
        if resp.output_active:
            cl.stop_record()
            print("Stopped Recording")
        else:
            print("OBS Wasn't recording")
        sys.exit(0)
    def error_handler():
        '''
        Handles the error signal
        returns: nothing
        '''
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
    matches = get_matches.all(os.getenv("EVENT_KEY"), os.getenv("TBA_TOKEN"))

    for i in matches:
        print("Match: ", i)
        print(" ")
        teams = get_matches.getTeams(i)
        fileMatch = i[10:]
        file = f"{fileMatch}-{teams[0]}_{teams[1]}_{teams[2]}-{teams[3]}_{teams[4]}_{teams[5]}"
        cl.set_profile_parameter("Output", "FilenameFormatting", file)
        stream_manager.updateMatch(cl, i, teams)
        print("Stream Ready!")
        print("Waiting for field to clear")

        while True:
            cur_time = time.perf_counter()
            if round(cur_time == 165) and not MATCH_DISPLAYED:
                print("Match End!")
                cl.stop_record()
                print(f"File saved as {file}.mp4")
                time.sleep(5)
                file_upload.videoUpload(i, teams)
                MATCH_DISPLAYED = True
                print("Delay to catch errors")
                time.sleep(180)
                print("Advancing to next match")
                print(" ")
                print(" ")
                break
        MATCH_DISPLAYED = False
