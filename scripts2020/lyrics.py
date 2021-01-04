#  Copyright (c) 2020
#  Author: Rohit Suratekar
#  This script is part of random data-analysis done in 2020.
#
#  Data is scrapped from https://www.bollywoodlyrics.com/
#  See webscrapers.lyrics.py for the web-scrapping code

import os
from collections import Counter
from itertools import combinations

import pandas as pd

STOP_WORDS = [
    "male", "female"
]


class Lyrics:
    def __init__(self, data: list, uid: int):
        self.uid = uid
        self.data = data
        all_lines = [x.strip() for x in data]
        meta = False
        self.title = ""
        self.movie = ""
        self.artists = []
        self.lines = []
        for line in all_lines:
            if line == "---" and not meta:
                meta = True
                continue
            if meta:
                if line.startswith("title:"):
                    self.title = line.replace("title:", "").strip()
                elif line.startswith("movie:"):
                    self.movie = line.replace("movie:", "").strip()
                elif line.startswith("artists:"):
                    tmp = line.replace("artists:", "").strip()
                    self.artists = tmp.split(",")
                    self.artists = [x.strip() for x in self.artists]
                elif line.startswith("---"):
                    meta = False
                    continue
            if not meta:
                if len(line.strip()) > 0:
                    self.lines.append(line.strip())


def get_all_files():
    all_files = []
    for tree in os.walk("data/downloaded"):
        if len(tree[1]) == 0:
            for k in tree[2]:
                all_files.append(f"{tree[0]}/{k}")
    return all_files


def parse_file(filename, uid):
    with open(filename) as f:
        all_lines = f.readlines()
        return Lyrics(all_lines, uid)


def make_common_file(folder):
    os.makedirs(folder, exist_ok=True)
    data = []
    for file in get_all_files():
        data.append(parse_file(file, len(data)))
    with open(f"{folder}/titles.csv", "w") as f:
        print("uid,title,movie", file=f)
        for d in data:
            if "," in d.movie or "," in d.title:
                print(f"{d.uid},\"{d.title}\",\"{d.movie}\"", file=f)
            else:
                print(f"{d.uid},{d.title},{d.movie}", file=f)
    with open(f"{folder}/artists.csv", "w") as f:
        print("uid,artist", file=f)
        for d in data:
            for art in set(d.artists):
                print(f"{d.uid},{art.strip()}", file=f)
    with open(f"{folder}/lyrics.csv", "w") as f:
        print("uid,lyrics", file=f)
        for d in data:
            tmp = ";".join(d.lines).replace('"', "'")
            print(f"{d.uid},\"{tmp}\"", file=f)


def get_data():
    lyrics = pd.read_csv("data/lyrics/lyrics.csv")
    titles = pd.read_csv("data/lyrics/titles.csv")
    artists = pd.read_csv("data/lyrics/artists.csv")
    return titles, lyrics, artists


def create_artist_file():
    titles, lyrics, artists = get_data()
    artists = artists.groupby(by="uid").agg(list)['artist'].to_list()
    ctr = Counter()
    for m in artists:
        comb = combinations(sorted(m), 2)
        ctr.update(list(comb))

    with open("r_df.csv", "w") as f:
        print(f"artist1,artist2,songs", file=f)
        for c in ctr.most_common():
            if c[1] > 20:
                print(f"{c[0][0]},{c[0][1]},{c[1]}", file=f)


def run():
    # make_common_file("data/lyrics")
    create_artist_file()
