#  Copyright (c) 2020
#  Author: Rohit Suratekar
#  This script is part of random data-analysis done in 2020.
#
#  Data Source:
#  https://www.kaggle.com/patrickb1912/ipl-complete-dataset-20082020

import csv
from collections import defaultdict, Counter
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from SecretColors import Palette
from scipy.stats import linregress
import numpy as np

WINNER_TEAM = 10
TEAM1 = 6
TEAM2 = 7
TOSS_WIN = 8
TOSS_DES = 9


def manual_adjust(txt: plt.Text):
    if txt.get_text() == "Delhi":
        txt.set_verticalalignment("top")
        txt.set_y(txt._y - 2)
    elif txt.get_text() == "Hyderabad":
        txt.set_verticalalignment("bottom")
    elif txt.get_text() in ["Chennai", "Rajasthan", "Punjab", "Kolkata"]:
        txt.set_horizontalalignment("right")
        txt.set_verticalalignment("top")
        txt.set_x(txt._x - 6)
    elif txt.get_text() == "Bangalore":
        txt.set_verticalalignment("top")
        txt.set_y(txt._y + 1)


def get_data():
    # After data cleanup in bash
    data = []
    with open("data/ipl.csv") as f:
        next(f)  # Skip header
        for row in csv.reader(f):
            # if row[WINNER_TEAM] in ["Pune", "Gujarat", "Kochi"]:
            #     continue
            if row[WINNER_TEAM] == "NA":
                continue
            other = row[TEAM1] if row[TEAM1] != row[WINNER_TEAM] else row[
                TEAM2]
            data.append(
                (row[WINNER_TEAM], other, row[TOSS_WIN], row[TOSS_DES], row))
    return data


def draw_correlation(x_values, y_values, x_max):
    slope, intercept, r_value, p_value, std_err = linregress(x_values,
                                                             y_values)
    x1, x2 = 0, x_max
    y1 = intercept + x1 * slope
    y2 = intercept + x2 * slope
    plt.plot([x1, x2], [y1, y2], ls="--", color="k",
             alpha=0.3, zorder=0)
    r2 = round(r_value * r_value, 2)
    plt.annotate(f"$R^2$ : {r2}",
                 xy=(0.05, 0.9),
                 xycoords="axes fraction",
                 bbox=dict(fc="white", ec="None"))


def plot_match_played():
    p = Palette()
    data = get_data()
    matches = [x[0] for x in data]
    matches.extend([x[1] for x in data])
    ctr = Counter(matches)
    data_dict = defaultdict(list)
    for d in data:
        data_dict[d[0]].append(d[1])
    success = {k: len(v) for k, v in data_dict.items()}

    x_values, y_values = [], []
    for team in success:
        plt.scatter(ctr[team], success[team], color=p.blue())
        t = plt.text(ctr[team] + 3, success[team], team)
        y_values.append(success[team])
        x_values.append(ctr[team])
        manual_adjust(t)

    plt.xlim(0, 250)
    plt.ylim(0, 140)
    plt.gca().set_facecolor(p.gray(shade=10))
    plt.grid(which="both", ls="--", alpha=0.5)
    plt.xlabel("number of matches played")
    plt.ylabel("number of wins")
    draw_correlation(x_values, y_values, 250)
    plt.tight_layout()
    plt.savefig("plot.png", dpi=150)
    plt.show()


def plot_toss_wins():
    p = Palette()
    data = get_data()
    toss_won = [x[2] for x in data]
    toss = Counter(toss_won)
    win = Counter([x[0] for x in data])
    x_values, y_values = [], []
    for m in win:
        plt.scatter(toss[m], win[m], color=p.red())
        ha = "left"
        x_offset = 2
        if m in ["Punjab"]:
            ha = "right"
            x_offset = -2

        plt.text(toss[m] + x_offset, win[m], m, ha=ha)
        x_values.append(toss[m])
        y_values.append(win[m])

    plt.xlim(0, 130)
    plt.ylim(0, 130)
    plt.gca().set_facecolor(p.gray(shade=10))
    plt.grid(which="both", ls="--", alpha=0.5)
    plt.xlabel("number of times team has won the toss")
    plt.ylabel("number of wins")
    draw_correlation(x_values, y_values, 130)
    plt.tight_layout()
    plt.savefig("plot.png", dpi=150)
    plt.show()


def plot_bat_decision():
    p = Palette()
    data = get_data()
    dec = [x[2] for x in data if x[3] == "bat"]
    dec = Counter(dec)
    win = Counter([x[0] for x in data])

    x_values, y_values = [], []
    for m in win:
        plt.scatter(dec[m], win[m], color=p.green())
        ha = "left"
        x_offset = 1
        if m in ["Bangalore"]:
            ha = "right"
            x_offset = -1
        plt.text(dec[m] + x_offset, win[m], m, ha=ha)
        x_values.append(dec[m])
        y_values.append(win[m])

    plt.xlim(0, 60)
    plt.ylim(0, 130)
    plt.gca().set_facecolor(p.gray(shade=10))
    plt.grid(which="both", ls="--", alpha=0.5)
    plt.xlabel("number of time team decided to bat after winning the toss")
    plt.ylabel("number of wins")
    draw_correlation(x_values, y_values, 60)
    plt.tight_layout()
    plt.savefig("plot.png", dpi=150)
    plt.show()


def plot_field_decision():
    p = Palette()
    data = get_data()
    dec = [x[2] for x in data if x[3] == "field"]
    dec = Counter(dec)
    win = Counter([x[0] for x in data])

    x_values, y_values = [], []
    for m in win:
        plt.scatter(dec[m], win[m], color=p.yellow())
        ha = "left"
        x_offset = 1
        if m in ["Hyderabad", "Punjab"]:
            ha = "right"
            x_offset = -1
        plt.text(dec[m] + x_offset, win[m], m, ha=ha)
        x_values.append(dec[m])
        y_values.append(win[m])

    plt.xlim(0, 80)
    plt.ylim(0, 130)
    plt.gca().set_facecolor(p.gray(shade=10))
    plt.grid(which="both", ls="--", alpha=0.5)
    plt.xlabel("number of time team decided to field after winning the toss")
    plt.ylabel("number of wins")
    draw_correlation(x_values, y_values, 80)
    plt.tight_layout()
    plt.savefig("plot.png", dpi=150)
    plt.show()


def plot_day():
    p = Palette()
    data = get_data()
    winners = [x[0] for x in data]
    data = [x[4][1] for x in data]
    win = Counter(winners)
    cities = Counter()
    for i in range(len(data)):
        if winners[i] == data[i]:
            cities.update({data[i]})
        elif winners[i] == "Rajasthan" and data[i] == "Jaipur":
            cities.update({winners[i]})
        elif winners[i] == "Gujarat" and data[i] == "Rajkot":
            cities.update({winners[i]})
        elif winners[i] == "Punjab" and data[i] == "Chandigarh":
            cities.update({winners[i]})

    x_values, y_values = [], []
    for m in win:
        plt.scatter(cities[m], win[m], color=p.aqua())
        ha = "left"
        x_offset = 1
        va = "center"
        if m in ["Punjab"]:
            ha = "right"
            va = "center"
            x_offset = -1
        plt.text(cities[m] + x_offset, win[m], m, ha=ha, va=va)
        x_values.append(cities[m])
        y_values.append(win[m])

    plt.xlim(0, 70)
    plt.ylim(0, 130)
    plt.gca().set_facecolor(p.gray(shade=10))
    plt.grid(which="both", ls="--", alpha=0.5)
    plt.xlabel("number of time team played in home ground")
    plt.ylabel("number of wins")
    draw_correlation(x_values, y_values, 70)
    plt.tight_layout()
    plt.savefig("plot.png", dpi=150)
    plt.show()


def plot_pca():
    p = Palette()
    data = get_data()
    win = Counter()
    toss = Counter()
    bat = Counter()
    field = Counter()
    ground = Counter()
    for d in data:
        win.update({d[0]})
        if d[0] == d[2]:
            toss.update({d[0]})
        if d[3] == "bat":
            bat.update({d[0]})
        else:
            field.update({d[0]})

        if d[0] == d[4][1]:
            ground.update({d[0]})
        elif d[0] == "Rajasthan" and d[4][1] == "Jaipur":
            ground.update({d[0]})
        elif d[0] == "Gujarat" and d[4][1] == "Rajkot":
            ground.update({d[0]})
        elif d[0] == "Punjab" and d[4][1] == "Chandigarah":
            ground.update({d[0]})

    values = defaultdict(list)
    labels = []
    for m in win:
        labels.append(m)
        values[m].append(win[m])
        values[m].append(toss[m])
        values[m].append(bat[m])
        values[m].append(field[m])
        values[m].append(ground[m])

    values = np.array(list(values.values())).transpose()
    pca = PCA()
    pca.fit_transform(values)
    var = pca.components_
    plt.scatter(var[0, :], var[1, :], color=p.red(shade=40))
    for i, m in enumerate(labels):
        plt.annotate(m, xy=(var[0, i] + 0.005, var[1, i]), )
    percentages = [round(x, 2) for x in pca.explained_variance_ratio_ * 100]
    plt.xlabel(f"PC1: {percentages[0]} %")
    plt.ylabel(f"PC2: {percentages[1]} %")
    plt.xlim(0, 0.51)
    plt.gca().set_facecolor(p.gray(shade=10))
    # plt.grid(which="both", ls="--", color=p.black(), alpha=0.5)
    plt.tight_layout()
    plt.savefig("plot.png", dpi=150)
    plt.show()


def plot_toss_wins_normalized():
    p = Palette()
    data = get_data()
    toss_won = [x[2] for x in data]
    toss = Counter(toss_won)
    win = Counter([x[0] for x in data])
    matches = [x[0] for x in data]
    matches.extend([x[1] for x in data])
    matches = Counter(matches)
    x_values, y_values = [], []
    for m in win:
        plt.scatter(toss[m] / matches[m], win[m] / matches[m], color=p.red())
        ha = "left"
        x_offset = 0.002
        if m in ["Punjab", "Mumbai", "Kolkata", "Gujarat"]:
            ha = "right"
            x_offset = -0.002

        plt.text(toss[m] / matches[m] + x_offset, win[m] / matches[m], m,
                 ha=ha)
        x_values.append(toss[m] / matches[m])
        y_values.append(win[m] / matches[m])

    plt.xlim(0.4, 0.65)
    plt.ylim(0.3, 0.62)
    plt.gca().set_facecolor(p.gray(shade=10))
    plt.grid(which="both", ls="--", alpha=0.5)
    plt.xlabel("number of times team has won the toss (normalized)")
    plt.ylabel("number of wins (normalized)")
    plt.title("after data is normalized to number of matches played")
    draw_correlation(x_values, y_values, 0.65)
    plt.tight_layout()
    plt.savefig("plot.png", dpi=150)
    plt.show()


def run():
    # plot_toss_wins()
    # plot_match_played()
    # plot_bat_decision()
    # plot_field_decision()
    # plot_day()
    plot_toss_wins_normalized()
