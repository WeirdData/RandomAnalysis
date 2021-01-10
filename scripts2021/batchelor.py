#  Copyright (c) 2021
#  Author: Rohit Suratekar
#  This script is part of random data-analysis done in 2021.
#
#  Data Source: Box 19, All India Survey on Higher Education 2017-18, 2018-29

import matplotlib.pyplot as plt
from SecretColors import Palette

data = [("B.A.", 9099473, 9860520, 9651891, 9527060, 9299437, 9198205),
        ("B.Sc.", 3579526, 4299538, 4618172, 4978564, 5138250, 5043732),
        ("B.Com.", 3117265, 3338111, 3422312, 3484301, 3548572, 3571436),
        ("B.Tech./B.E.", 4336149, 4254919, 4203933, 4085321, 3940080, 3770949),
        ("B.Ed.", 559028, 657194, 514518, 810914, 1014882, 1175517),
        ("B.C.A.", 421191, 432341, 426229, 415007, 432382, 446680),
        ("B.B.A", 317024, 343237, 349667, 383827, 424785, 476169),
        ("L.L.B.", 240419, 283231, 300716, 205402, 338716, 362493),
        ("B.Pharm.", 174820, 183695, 195178, 313776, 225457, 246358),
        ("M.B.B.S", 160402, 170406, 191040, 211366, 241601, 267197),
        ("B.Sc.(Nursing)", 176781, 179496, 191612, 218882, 239485, 255071)]

labels = ["2013-14", "2014-15", "2015-16", "2016-17", "2017-18", "2018-19"]


def run():
    p = Palette()
    cc = p.cycle()
    courses = []

    colors = []
    for d in data[:4]:
        points_x = []
        points_y = []
        c = next(cc)
        colors.append(c)
        courses.append(d[0])
        for i in range(1, len(d)):
            points_x.append(i)
            points_y.append(d[i])

        plt.plot(points_x, points_y, color=c,
                 marker="o")
        yf = 0
        if d[0] == data[3][0]:
            yf = 250000
        plt.annotate(d[0], xy=(len(d) - 0.8, d[-1] + yf),
                     va="center", color=c)

    other = []
    other_values = [0] * (len(data[0]) - 1)
    for d in data[4:]:
        other.append(d[0])
        for i in range(1, len(d)):
            other_values[i - 1] += d[i]

    other_str = ""
    for i, m in enumerate(other):
        other_str += m + ", "
        if (i + 1) % 2 == 0:
            other_str += "\n"

    other_str = other_str[:-2]  # Remove last comma
    c = next(cc)
    plt.plot(range(1, len(other_values) + 1), other_values, color=c,
             marker="o")

    plt.annotate("Other", xy=(len(other_values) + 0.2, other_values[-1]),
                 va="top", color=c)

    plt.xticks(range(1, len(labels) + 1), labels)
    plt.gca().set_facecolor(p.gray(shade=10))
    plt.grid(axis="x", ls="--")
    plt.ylabel("Students Enrolled")
    plt.xlabel("Academic Year")
    plt.annotate("Student enrollment in major graduate level programs ("
                 "regular mode)",
                 xy=(0.5, 1.06), xycoords="axes fraction",
                 ha="center")
    plt.annotate("Data Source: All India Survey on Higher Education ("
                 "2017-18, 2018-19)",
                 xy=(0.5, 1.02), xycoords="axes fraction",
                 fontsize=7, color=p.gray(),
                 ha="center")
    plt.annotate(other_str, xy=(len(other_values) + 0.9,
                                other_values[-1] - 400000),
                 va="top", fontsize=6, ha="right",
                 color=p.teal(shade=40))
    plt.ylim(data[-1][-1], data[0][-1] * 1.2)
    plt.xlim(0, len(data[0]) * 1.2 - 1)
    plt.tight_layout()
    plt.savefig("plot.png", dpi=150)
    plt.show()
