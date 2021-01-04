#  Copyright (c) 2020
#  Author: Rohit Suratekar
#  This script is part of random data-analysis done in 2020.
#
#  Scraps https://www.bollywoodlyrics.com/ for lyrics
#
#  All lyrics scrapped are used for data-analysis purpose and analysis is
#  kept public. No commercial use is intended. As of 12 December 2020,
#  website do not mention anything about the web-scrapping.


import pathlib
import random
import time

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.bollywoodlyrics.com"
FOLDER = f"data/downloaded"


def get_page(url) -> BeautifulSoup:
    print(f"fetching {url}")
    time.sleep(random.randint(0, 3))
    page = requests.get(url)
    if page.status_code != 200:
        print(f"Something went wrong. Skipping URL: {url}")
        return None
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def extract_all_pages(no_of_pages, alphabet):
    if no_of_pages == 0:
        return []
    urls = []
    for x in range(2, no_of_pages + 1):
        url = f"{BASE_URL}/alphabet/page/{x}?letter={alphabet.strip().upper()}"
        urls.append(url)
    return urls


def extract_all_songs_urls(url):
    soup = get_page(url)
    if soup is None:
        print("Skipping page URL extraction")
        return []
    links = soup.find_all('a')
    links = [str(x['href']) for x in links]
    selected = [x for x in links if f"{BASE_URL}/lyrics" in x]
    return selected


def extract_lyrics(url, folder_name):
    soup = get_page(url)
    head = soup.find_all("div", attrs={"class": "lyrics-title"})[0]
    title = head.find_all("h1")[0].text
    movie = ""
    artists = []
    for link in head.find_all('a'):
        if f"{BASE_URL}/movie/" in link['href']:
            movie = link.text
        if f"{BASE_URL}/artist/" in link['href']:
            artists.append(link.text)

    lyrics = ""
    for p in soup.find_all("div", attrs={"class": "lyric-text"}):
        for child in p.findChildren("p"):
            lyrics += child.text
            lyrics += "\n"

    if len(lyrics.strip()) == 0:
        pres = []
        for p in soup.find_all("pre"):
            pres.append(p.text)
        if len(pres) > 1:
            final_pre = [x for x in pres[1:] if x.strip() != pres[0].strip()]
            final_pre.append(pres[0])
            lyrics = "".join(final_pre)
        else:
            lyrics = pres[0]

    name = url.replace(f"{BASE_URL}/lyrics/", "")

    with open(f"{folder_name}/{name}.txt", "w") as f:
        print("---", file=f)
        print(f"title: {title}", file=f)
        print(f"movie: {movie}", file=f)
        print(f"artists: {','.join(artists)}", file=f)
        print("---\n", file=f)
        print(lyrics, file=f)


def start_analysis(alphabet: str):
    data_folder = f"data/downloaded/{alphabet.strip()}"
    pathlib.Path(data_folder).mkdir(parents=True, exist_ok=True)
    url = f"{BASE_URL}/alphabet?letter={alphabet.strip().upper()}"
    soup = get_page(url)
    if soup is None:
        print(f"Analysis halted because URL not working : {url}")
        return
    links = soup.find_all('a')
    links = [str(x['href']) for x in links]
    no_of_pages = [x for x in links if
                   f"{BASE_URL}/alphabet/page/" in x]
    no_of_pages = [x.replace(f"{BASE_URL}/alphabet/page"
                             "/", "") for x in no_of_pages]
    no_of_pages = [x.replace(f"?letter={alphabet.strip().upper()}", "") for x
                   in no_of_pages]
    no_of_pages = [int(x) for x in no_of_pages if str(x).isnumeric()]
    if len(no_of_pages) > 0:
        no_of_pages = max(no_of_pages)
    else:
        no_of_pages = 0
    urls = [url]
    urls.extend(extract_all_pages(no_of_pages, alphabet))
    songs = []
    for ur in urls:
        songs.extend(extract_all_songs_urls(ur))

    for s in songs:
        extract_lyrics(s, data_folder)


def run():
    for abc in ["x"]:
        start_analysis(abc)
