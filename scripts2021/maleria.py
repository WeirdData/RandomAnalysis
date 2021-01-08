#  Copyright (c) 2021
#  Author: Rohit Suratekar
#  This script is part of random data-analysis done in 2021.
#
#  Data : https://www.who.int/malaria/data/en/

import matplotlib.pyplot as plt
import pandas as pd
from SecretColors import Palette
import numpy as np

palette = Palette()


def fill_nan(x):
    try:
        return float(x)
    except ValueError:
        return np.NaN


def get_data():
    df = pd.read_csv("data/maleria_deaths.csv")
    df = df.set_index("Country")
    df = df.applymap(fill_nan)
    df["total"] = df.apply(lambda x: sum(x), axis=1)
    df = df.sort_values(by="2018", ascending=False)
    df = df[df["total"] > 0]
    del df["total"]
    return df


def color_cycle():
    colors = [palette.red(),
              palette.blue(),
              palette.green()]
    for c in colors:
        yield c
    while True:
        yield palette.gray()


def plot_data():
    color = color_cycle()
    data = get_data()
    labels = sorted(list(data.columns))
    label_count = 0
    for key, value in data.iterrows():
        current_color = next(color)
        points = []
        for year in labels:
            try:
                points.append((labels.index(year), float(value[year])))
            except ValueError:
                pass

        x = [m[0] for m in points]
        y = [m[1] for m in points]
        plt.plot(x, y, color=current_color)
        if key == "Democratic Republic of the Congo":
            key = "Congo"
        if label_count < 3:
            plt.annotate(key, xy=(x[-1] + 0.2, y[-1]), color=current_color)
            label_count += 1

    plt.title("Reported Malaria Deaths (2000-2018)")
    plt.xticks(range(len(labels)), labels, rotation=90)
    plt.xlim(-1, len(labels) + 2)
    plt.show()


def run():
    plot_data()
