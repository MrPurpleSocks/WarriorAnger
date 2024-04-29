<div align="center">
  <img margin="auto" width="572px" src="https://github.com/MrPurpleSocks/WarriorAnger/blob/779b15242323b06937dc770d1bfbb151ef47f508/images/WarriorAnger_Banner_white.png" alt="WarriorAnger Logo">
</div>

## Notice
The current version of WarriorAnger (3.0) doesn't support custom (non-3256) zipline instances

## System Requirements
- Windows 11 (10 may work)
- Open Broadcaster Software Studio 30.1.1 (64bit)
- OBS WebSockets (Enabled)
- Python 3.11.7

## Server Setup (uses Amazon EC2)
- Create EC2 Instance (t2.micro minimum, debian)
- `ssh -i /path/to/key.pem  ubuntu@public-DNS` - SSH into Instance
- `git clone https://github.com/diced/zipline.git` - clone zipline (file server)
- `curl -fsSL https://get.docker.com -o get-docker.sh` - Download docker convenience script
- `sudo sh get-docker.sh` - Run convenience script
- `cd zipline` - Use the `zipline` directory
- `docker compose up -d`- Run Docker container detached
- Optional:
- Setup either nginx or apache reverse proxy
- Configure DNS to point to zipline instance

 ## Client Setup
- `git clone https://github.com/mrpurplesocks/warrioranger` - Clone Repo.
- `cd WarriorAnger` - Use WarriorAnger directory.
- `cp .env.example .env` - duplicate .env.example to .env
- edit `.env` - Edit .env to use your info
- `pip install -r requirements.txt` - install required dependancies
- `python WB-Capture.py` - Run main script.


# Release 3.0

## Current Features
- CLI User Interface
- Match schedule fetching from TBA
- ~~File Upload~~ nvm it isnt working rn
- Discord Embed Webhook
- OBS WebSockets Integration
- Automatic File Naming
- Automatic Stream Graphics

## What's Changed
- Manual Mode added
- Automatic Mode Temporarily Disabled (Womp Womp)
- File Upload Broken :(
- Easy (ish) Setup

## Upcoming Features and Fixes
- Fixing File Upload (Async file upload, File Chunking)
- GUI
- Match Scores (Stream Graphics, OCR)
- Fixing Automatic Mode
- Proper error handling
- Prevent Start/Stop Double Click
- Custom File Server Solution
- Allow Custom zipline instances
