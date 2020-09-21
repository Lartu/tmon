#!/usr/bin/env python3

# +--------------------------------+
# |      YouTube Monitor: tmon     |
# | By Lartu, 2020 - www.lartu.net |
# +--------------------------------+

# --- Imports ---
import sys
import os
from subprocess import check_output
from datetime import datetime

# --- Constants ---
VERSION = "1.0.21"
PATH = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = PATH + "/config.tmon"
TEMP_FILE = PATH + "/.temp_list"
DOWNLOAD_DIR = PATH + "/downloads"
HISTORY_FILE = PATH + "/history.tmon"
LOG_FILE = PATH + "/log.tmon"
ERROR_LOG = PATH + "/failed.tmon"
YOUTUBEDL = PATH + "/youtube-dl"

# --- Functions ---
def getYoutubePlaylist(playlistId):
    youtube_dl_command = f"{YOUTUBEDL} -j --flat-playlist 'https://www.youtube.com/playlist?list={playlistId}'"
    temp_file = TEMP_FILE.replace(' ', '\\ ')
    pipe_command = f"| jq -r '.id' | sed 's_^_https://youtu.be/_' > {temp_file}"
    command = f"{youtube_dl_command} {pipe_command}"
    #log(command)
    os.system(command)


def loadConfigURL():
    try:
        with open(CONFIG_FILE, "r+") as f:
            playlistId = f.read()
        playlistId = playlistId.split("\n")[0].strip()
    except BaseException as e:
        log(f"Error found while trying to read {CONFIG_FILE}:\n{e}")
        open(CONFIG_FILE, "w+")
        sys.exit(1)
    return playlistId


def loadVideoURLs():
    try:
        with open(TEMP_FILE, "r+") as f:
            lines = f.readlines()
            urls = []
            for line in lines:
                urls.append(line.strip())
    except BaseException as e:
        log(f"Error found while trying to read {TEMP_FILE}:\n{e}")
        open(TEMP_FILE, "w+")
        sys.exit(1)
    return urls


def loadHistoryURLs():
    try:
        with open(HISTORY_FILE, "r+") as f:
            urls = f.readlines()
    except BaseException as e:
        open(HISTORY_FILE, "w+")
        return []
    # Remove comments
    lines = []
    for url in urls:
        url = url.strip()
        if len(url) > 0:
            if url[0] != "#":
                lines.append(url)
    return lines
    
    
def getVideoTitle(url):
    command = f"{YOUTUBEDL} -e {url}"
    title = check_output(command.split(" ")).decode(encoding='UTF-8').strip()
    return title


def printInBox(message):
    msglen = len(message)
    top = "╔═" + ("═" * msglen) + "═╗"
    middle = "║ " + message + " ║"
    bottom = "╚═" + ("═" * msglen) + "═╝"
    log(top)
    log(middle)
    log(bottom)


def replaceNonChars(filename):
    invalid_chars = "/<>:\"\\|?*"
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    return filename


def downloadMp3(url, filename, title):
    download_dir = DOWNLOAD_DIR.replace('\"', '\\\"')
    os.system(f"mkdir -p \"{download_dir}\"")
    filename = download_dir + "/" + filename.replace('\"', '\\\"')
    command = f'{YOUTUBEDL} --extract-audio --audio-format mp3 --output "{filename}.%(ext)s" {url} --quiet'
    #print(command)
    result = os.system(command)
    if result != 0:
        writeFailed(url)
        writeFailed(f"# {filename}")
        writeFailed(f"# {title}")
        writeFailed("")
        log("Error downloading. Will try again next time")
    else:
        writeHistory(url)
        writeHistory(f"# {filename}")
        writeHistory(f"# {title}")
        writeHistory("")
        log("Downloaded.")
        

def writeHistory(url):
    try:
        with open(HISTORY_FILE, "a+") as f:
            f.write(url + "\n")
    except BaseException as e:
        log(f"Error found while trying to write to {HISTORY_FILE}:\n{e}")
        sys.exit(1)
        

def writeFailed(url):
    try:
        with open(ERROR_LOG, "a+") as f:
            f.write(url + "\n")
    except BaseException as e:
        log(f"Error found while trying to write to {ERROR_LOG}:\n{e}")
        sys.exit(1)


def log(message):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(message)
    try:
        with open(LOG_FILE, "a+") as f:
            f.write(dt_string + " | " + message + "\n")
    except BaseException as e:
        log(f"Error found while trying to write to {HISTORY_FILE}:\n{e}")
        sys.exit(1)


def getYoutubeDl():
    if not os.path.exists(YOUTUBEDL):
        youtubedl = YOUTUBEDL.replace('\"', '\\\"')
        log("The latest version of youtube-dl hasn't been found locally. Downloading...")
        os.system(f'curl -L https://yt-dl.org/downloads/latest/youtube-dl -o {youtubedl}')
        os.system(f'chmod a+rx {youtubedl}')
        log("Youtube-dl obtained.")
        

# --- Procedure ---
log("")
printInBox(f"Running tmon {VERSION}, by Lartu (www.lartu.net)")
log("")
getYoutubeDl()
log(f"Obtaining playlist id from {CONFIG_FILE}...")
playlistId = loadConfigURL()
log(f"Obtained playlist id: '{playlistId}'")
log(f"Obtaining URLs in the playlist...")
getYoutubePlaylist(playlistId)
log(f"Loading URLs from {TEMP_FILE}...")
to_download = loadVideoURLs()
log(f"Obtained {len(to_download)} URLs from the playlist.")
log(f"Loading historic URLs from {HISTORY_FILE}...")
history = loadHistoryURLs()
log(f"Obtained {len(history)} URLs from the history.")

log(f"Purging downloaded URLs from the download list...")
urls = []
for url in to_download:
    if url not in history:
        urls.append(url)
log(f"{len(urls)} left to be downloaded.")

log(f"Proceeding to download the videos...")

counter = 0
for url in urls:
    counter += 1
    counter_message = f"{counter}/{len(urls)}"
    url = url.strip()
    log("")
    title = getVideoTitle(url)
    if len(title) > 60:
        title = title[0:60] + "..."
    url_key = url.split(".be/")[1].strip()
    printInBox("(" + counter_message + ") " + title)
    log(f"(url: {url})")
    log(f"(key: {url_key})")
    filename = title.replace(" ", "_") + "_(" + url_key + ")"
    filename = replaceNonChars(filename)
    log(f"(filename: {filename}.mp3)")
    log("Downloading, please wait...")
    downloadMp3(url, filename, title)




