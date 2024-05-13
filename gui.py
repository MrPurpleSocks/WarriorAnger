
from tkinter import *
import time

# GUI: RUN; OBS: READY; Stream: READY; Nexus: RUN; Manual: READY; Status: READY

status = "READY"
services_in_error = ["OBS", "Stream", "ZipLine", "Nexus", "Manual"]
services_running = []
services_ready = []

is_init = False
is_started = False

warnings = 0

def init():
    '''
    Initializes the GUI
    '''
    global is_init
    if not is_init:
        is_init = True
        set_status("OBS", "READY")
        set_status("Stream", "READY")
        set_status("ZipLine", "READY")
        set_status("Nexus", "READY")
        set_status("Manual", "READY")

def start_event():
    '''
    Starts the event
    '''
    global warnings, is_started
    if len(services_in_error) > 0:
        warnings += 1
        listbox.insert(warnings,"Warning: Not all services are ready")
    elif not is_init:
        warnings += 1
        listbox.insert(warnings,"Warning: Event not initialized")
    else:
        is_started = True
        listbox.insert(warnings,"Event Started")
        set_status("OBS", "RUN")
        set_status("Stream", "RUN")
        set_status("Nexus", "RUN")

def end_event():
    '''
    Ends the event
    '''
    global warnings, is_started
    if not is_started:
        warnings += 1
        listbox.insert(warnings,"Warning: Event not started")
    else:
        is_started = False
        listbox.insert(warnings,"Event Ended")
        set_status("OBS", "READY")
        set_status("Stream", "READY")
        set_status("Nexus", "READY")

def set_status(service: str, status: str):
    '''
    Sets the status of a service
    '''

    match service:
        case "OBS":
            match status:
                case "RUN":
                    print("OBS RUN")
                    if "OBS" not in services_running:
                        services_running.append("OBS")
                    if "OBS" in services_ready:
                        services_ready.remove("OBS")
                    if "OBS" in services_in_error:
                        services_in_error.remove("OBS")
                case "READY":
                    print("OBS READY")
                    if "OBS" in services_running:
                        services_running.remove("OBS")
                    if "OBS" not in services_ready:
                        services_ready.append("OBS")
                    if "OBS" in services_in_error:
                        services_in_error.remove("OBS")
                case "ERROR":
                    print("OBS ERROR")
                    if "OBS" in services_running:
                        services_running.remove("OBS")
                    if "OBS" in services_ready:
                        services_ready.remove("OBS")
                    if "OBS" not in services_in_error:
                        services_in_error.append("OBS")
                         
                case _:
                    print("Invalid Status")
        case "Stream":
            match status:
                case "RUN":
                    print("Stream RUN")
                    if "Stream" not in services_running:
                        services_running.append("Stream")
                    if "Stream" in services_ready:
                        services_ready.remove("Stream")
                    if "Stream" in services_in_error:
                        services_in_error.remove("Stream")
                case "READY":
                    print("Stream READY")
                    if "Stream" in services_running:
                        services_running.remove("Stream")
                    if "Stream" not in services_ready:
                        services_ready.append("Stream")
                    if "Stream" in services_in_error:
                        services_in_error.remove("Stream")
                case "ERROR":
                    print("Stream ERROR")
                    if "Stream" in services_running:
                        services_running.remove("Stream")
                    if "Stream" in services_ready:
                        services_ready.remove("Stream")
                    if "Stream" not in services_in_error:
                        services_in_error.append("Stream")
                         
                case _:
                    print("Invalid Status")
        case "ZipLine":
            match status:
                case "RUN":
                    print("ZipLine RUN")
                    if "ZipLine" not in services_running:
                        services_running.append("ZipLine")
                    if "ZipLine" in services_ready:
                        services_ready.remove("ZipLine")
                    if "ZipLine" in services_in_error:
                        services_in_error.remove("ZipLine")
                case "READY":
                    print("ZipLine READY")
                    if "ZipLine" in services_running:
                        services_running.remove("ZipLine")
                    if "ZipLine" not in services_ready:
                        services_ready.append("ZipLine")
                    if "ZipLine" in services_in_error:
                        services_in_error.remove("ZipLine")
                case "ERROR":
                    print("ZipLine ERROR")
                    if "ZipLine" in services_running:
                        services_running.remove("ZipLine")
                    if "ZipLine" in services_ready:
                        services_ready.remove("ZipLine")
                    if "ZipLine" not in services_in_error:
                        services_in_error.append("ZipLine")
                         
                case _:
                    print("Invalid Status")
        case "Nexus":
            match status:
                case "RUN":
                    print("Nexus RUN")
                    if "Nexus" not in services_running:
                        services_running.append("Nexus")
                    if "Nexus" in services_ready:
                        services_ready.remove("Nexus")
                    if "Nexus" in services_in_error:
                        services_in_error.remove("Nexus")
                case "READY":
                    print("Nexus READY")
                    if "Nexus" in services_running:
                        services_running.remove("Nexus")
                    if "Nexus" not in services_ready:
                        services_ready.append("Nexus")
                    if "Nexus" in services_in_error:
                        services_in_error.remove("Nexus")
                case "ERROR":
                    print("Nexus ERROR")
                    if "Nexus" in services_running:
                        services_running.remove("Nexus")
                    if "Nexus" in services_ready:
                        services_ready.remove("Nexus")
                    if "Nexus" not in services_in_error:
                        services_in_error.append("Nexus")
                         
                case _:
                    print("Invalid Status")
        case "Manual":
            match status:
                case "RUN":
                    print("Manual RUN")
                    if "Manual" not in services_running:
                        services_running.append("Manual")
                    if "Manual" in services_ready:
                        services_ready.remove("Manual")
                    if "Manual" in services_in_error:
                        services_in_error.remove("Manual")
                case "READY":
                    print("Manual READY")
                    if "Manual" in services_running:
                        services_running.remove("Manual")
                    if "Manual" not in services_ready:
                        services_ready.append("Manual")
                    if "Manual" in services_in_error:
                        services_in_error.remove("Manual")
                case "ERROR":
                    print("Manual ERROR")
                    if "Manual" in services_running:
                        services_running.remove("Manual")
                    if "Manual" in services_ready:
                        services_ready.remove("Manual")
                    if "Manual" not in services_in_error:
                        services_in_error.append("Manual")
                         
                case _:
                    print("Invalid Status")
        case "Status":
            print("Invalid Service")
        case _:
            print("Invalid Service")

    if len(services_in_error) > 0:
        status = "ERROR"
        sbar.config(bg="red")
    elif len(services_running) > 0:
        status = "RUN"
        sbar.config(bg="green")
    elif len(services_ready) > 0:
        status = "READY"
        sbar.config(bg="yellow")

    if "OBS" in services_in_error:
        OBS = "ERROR"
    elif "OBS" in services_running:
        OBS = "RUN"
    elif "OBS" in services_ready:
        OBS = "READY"

    if "Stream" in services_in_error:
        Stream = "ERROR"
    elif "Stream" in services_running:
        Stream = "RUN"
    elif "Stream" in services_ready:
        Stream = "READY"
    
    if "ZipLine" in services_in_error:
        Zipline = "ERROR"
    elif "ZipLine" in services_running:
        Zipline = "RUN"
    elif "ZipLine" in services_ready:
        Zipline = "READY"
    
    if "Nexus" in services_in_error:
        Nexus = "ERROR"
    elif "Nexus" in services_running:
        Nexus = "RUN"
    elif "Nexus" in services_ready:
        Nexus = "READY"
    
    if "Manual" in services_in_error:
        Manual = "ERROR"
    elif "Manual" in services_running:
        Manual = "RUN"
    elif "Manual" in services_ready:
        Manual = "READY"

    mastervar.set(f"OBS: {OBS}; Stream: {Stream}; ZipLine: {Zipline}; Nexus: {Nexus}; Manual: {Manual}; Status: {status}")

root = Tk()
root.geometry("600x233")
root.title("WarriorAnger Monitor")

menu_bar = Menu(root)

config = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Config", menu=config)
config.add_command(label="Nexus", command=None)
config.add_command(label="OBS", command=None)
config.add_command(label="Stream", command=None)
config.add_command(label="Zipline", command=None)

manual = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Manual", menu=manual)
manual.add_command(label="Enter Manual", command=None)
manual.add_command(label="Configure", command=None)

event = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Event", menu=event)
event.add_command(label="Start Event", command=start_event)
event.add_command(label="End Event", command=end_event)
event.add_command(label="Configure", command=None)
event.add_command(label="Init", command=init)

root.config(menu=menu_bar)

title = Frame(root)

Label(title, text="WarriorAnger Monitor", font=("Arial", 20)).pack(side=LEFT)
Label(title, text="Developed by MrPurpleSocks", font=("Arial", 10)).pack(side=LEFT)
title.pack(anchor=W)

def placeholder():
    print("pressed")

listbox = Listbox(root, bg="grey", fg="yellow", width=600, height=10)
listbox.insert(1, "OBS: NOT CONFIGURED")
listbox.insert(2, "Stream: NOT CONFIGURED")
listbox.insert(3, "ZipLine: NOT CONFIGURED")
listbox.insert(4, "Nexus: NOT CONFIGURED")
warnings = 4
listbox.pack()

mastervar = StringVar()
mastervar.set("OBS: ERROR; Stream: ERROR; ZipLine: ERROR; Nexus: ERROR; Manual: ERROR; Status: ERROR")
sbar = Label(root, textvariable=mastervar, relief=SUNKEN, anchor="w", bg="red")
sbar.pack(side=BOTTOM, fill=X)

#    obs = Frame(root)
#    obs.pack(anchor=W)
#    Label(obs, text="OBS").pack(side = LEFT)
#    Button(obs, text="Ready", command=lambda: set_status("OBS", "READY")).pack(side = LEFT)
#    Button(obs, text="RUN", command=lambda: set_status("OBS", "RUN")).pack(side = LEFT)
#    Button(obs, text="ERROR", command=lambda: set_status("OBS", "ERROR")).pack(side = LEFT)
#
#    stream = Frame(root)
#    stream.pack(anchor=W)
#    Label(stream, text="Stream").pack(side = LEFT)
#    Button(stream, text="Ready", command=lambda: set_status("Stream", "READY")).pack(side = LEFT)
#    Button(stream, text="RUN", command=lambda: set_status("Stream", "RUN")).pack(side = LEFT)
#    Button(stream, text="ERROR", command=lambda: set_status("Stream", "ERROR")).pack(side = LEFT)
#
#    zip = Frame(root)
#    zip.pack(anchor=W)
#    Label(zip, text="ZipLine").pack(side = LEFT)
#    Button(zip, text="Ready", command=lambda: set_status("ZipLine", "READY")).pack(side = LEFT)
#    Button(zip, text="RUN", command=lambda: set_status("ZipLine", "RUN")).pack(side = LEFT)
#    Button(zip, text="ERROR", command=lambda: set_status("ZipLine", "ERROR")).pack(side = LEFT)
#
#    nexus = Frame(root)
#    nexus.pack(anchor=W)
#    Label(nexus, text="nexus").pack(side = LEFT)
#    Button(nexus, text="Ready", command=lambda: set_status("Nexus", "READY")).pack(side = LEFT)
#    Button(nexus, text="RUN", command=lambda: set_status("Nexus", "RUN")).pack(side = LEFT)
#    Button(nexus, text="ERROR", command=lambda: set_status("Nexus", "ERROR")).pack(side = LEFT)
#
#    manual = Frame(root)
#    manual.pack(anchor=W)
#    Label(manual, text="manual").pack(side = LEFT)
#    Button(manual, text="Ready", command=lambda: set_status("Manual", "READY")).pack(side = LEFT)
#    Button(manual, text="RUN", command=lambda: set_status("Manual", "RUN")).pack(side = LEFT)
#    Button(manual, text="ERROR", command=lambda: set_status("Manual", "ERROR")).pack(side = LEFT)

root.mainloop()