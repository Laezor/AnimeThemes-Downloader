import tkinter as tk
from tkinter import filedialog
import requests
import sys
import re
import os
import urllib.request

root = tk.Tk()
root.withdraw()

path = filedialog.askdirectory()

if not path:
    print("No path is selected")
    input("Press enter to Exit...")
    sys.exit()

checkaccount = input(
    'choose account type anilist or mal. WARNING! put those exact types!\n')


def dl_progress(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%" % percent)
    sys.stdout.flush()


if checkaccount == 'anilist':
    username = input('Enter your username of your anilist or mal account\n')
    response = requests.get(
        f'https://themes.moe/api/anilist/{username}').json()


elif checkaccount == 'mal':
    username = input('Enter your username of your anilist or mal account\n')
    response = requests.get(
        f'https://themes.moe/api/mal/{username}').json()
else:
    print("You have to type either anilist or mal!")
    input("Press Enter to continue...")
    sys.exit()

baseUrl = 'https://animethemes.moe/video/'

files = []

for item in response:
    counted = response.index(item)
    themes = response[counted]['themes']
    for mirror in themes:
        mirror = themes.index(mirror)
        url = response[counted]['themes'][mirror]['mirror']['mirrorURL']
        filename = re.sub('https://animethemes.moe/video/', "", url)
        files.append(filename)

allfiles = len(files)

for file in files:
    checkfile = re.sub(".webm", ".mp3", file)
    fullpathmp3 = path+"/"+checkfile
    fullpathwebm = path+"/"+file

    if not os.path.exists(fullpathmp3) and not os.path.exists(fullpathwebm):
        remainingfiles = files.index(file)

        print(f'\nDownloading {file} | {remainingfiles} / {allfiles}\n')

        dlUrl = baseUrl+file

        dlPath = path+"/"+file

        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('User-agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)')]
        urllib.request.install_opener(opener)

        urllib.request.urlretrieve(
            dlUrl, dlPath, reporthook=dl_progress)

    else:
        print(
            f'\nCannot create [{file}] or [{checkfile}]  because a file with that name already exists.')
