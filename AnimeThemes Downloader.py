import tkinter as tk
from tkinter import filedialog
import requests
import sys
import re
import os
import urllib.request
from urllib.error import HTTPError

root = tk.Tk()
root.withdraw()

print("Select a directory!")

path = filedialog.askdirectory()

if not path:
    print("No path is selected")
    input("Press enter to Exit...")
    sys.exit()


def dl_progress(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%" % percent)
    sys.stdout.flush()


baseUrl = 'https://animethemes.moe/video/'

userAnswer = input(
    "Do you wanna search a specific anime to download [y] or you want to download from your anilist/mal account? [n]\n").lower()

if userAnswer == 'y':
    animeAnswer = input("What anime do you want to search?\n")
    response = requests.get(
        f' https://api.jikan.moe/v3/search/anime?q={animeAnswer}').json()
    animeid = response['results'][0]['mal_id']
    resp = requests.get(f'https://themes.moe/api/themes/{animeid}').json()
    if not resp:
        input("Nothing found...\nPress enter to exit")
        sys.exit()
    files = []
    for item in resp:
        counted = resp.index(item)
        themes = resp[counted]['themes']
        for mirror in themes:
            mirror = themes.index(mirror)
            url = resp[counted]['themes'][mirror]['mirror']['mirrorURL']
            filename = re.sub('https://animethemes.moe/video/', "", url)
            files.append(filename)

    allfiles = len(files)

    for file in files:

        checkfile = re.sub(".webm", ".mp3", file)
        fullpathmp3 = path + "/" + checkfile
        fullpathwebm = path + "/" + file

        if not os.path.exists(fullpathmp3) and not os.path.exists(fullpathwebm):
            remainingfiles = files.index(file)

            print(f'\nDownloading {file} | {remainingfiles + 1} / {allfiles}\n')

            dlUrl = baseUrl + file

            dlPath = path + "/" + file

            opener = urllib.request.build_opener()
            opener.addheaders = [
                ('User-agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)')]
            urllib.request.install_opener(opener)
            try:
                urllib.request.urlretrieve(
                    dlUrl, dlPath, reporthook=dl_progress)
            except urllib.error.HTTPError as e:

                if e.code == 503:
                    print(
                        f"{file} was skipped because of error 503 service unavailable")
                    pass
                else:
                    raise
        else:
            print(
                f'\nCannot create [{file}] or [{checkfile}]  because a file with that name already exists.')

    sys.exit()

if userAnswer == 'n':

    checkaccount = input(
        'choose account type anilist or mal. WARNING! put those exact types!\n')

    if checkaccount == 'anilist':
        username = input(
            'Enter your username of your anilist or mal account\n')
        response = requests.get(
            f'https://themes.moe/api/anilist/{username}').json()

    elif checkaccount == 'mal':
        username = input(
            'Enter your username of your anilist or mal account\n')
        response = requests.get(
            f'https://themes.moe/api/mal/{username}').json()
    else:
        print("You have to type either anilist or mal!")
        input("Press Enter to continue...")
        sys.exit()

    files = []
    themelist = []
    for item in response:
        counted = response.index(item)
        themes = response[counted]['themes']
        for mirror in themes:
            mirror = themes.index(mirror)
            url = response[counted]['themes'][mirror]['mirror']['mirrorURL']
            themenames = response[counted]['themes'][mirror]['themeName']
            filename = re.sub('https://animethemes.moe/video/', "", url)
            themelist.append(themenames)
            files.append(filename)

    allfiles = len(files)

    for file, theme in zip(files, themelist):
        checkfile = re.sub(".webm", ".mp3", file)
        fullpathmp3 = path + "/" + checkfile
        fullpathwebm = path + "/" + file

        if not os.path.exists(fullpathmp3) and not os.path.exists(fullpathwebm):
            remainingfiles = files.index(file)

            print(f'\nDownloading {file} | {remainingfiles + 1} / {allfiles}\n')

            dlUrl = baseUrl + file

            dlPath = path + "/" + "{} -- {}".format(theme, file)

            opener = urllib.request.build_opener()
            opener.addheaders = [
                ('User-agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)')]
            urllib.request.install_opener(opener)

            urllib.request.urlretrieve(
                dlUrl, dlPath, reporthook=dl_progress)

        else:
            print(
                f'\nCannot create [{file}] or [{checkfile}]  because a file with that name already exists.')
