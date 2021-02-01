#  Copyright (c) 2021
#  Author: Rohit Suratekar
#  This script is part of random data-analysis done in 2021.
#
#  Data: https://www.indiabudget.gov.in/doc/Budget_at_Glance/bag6.pdf

import pandas as pd
import squarify
from SecretColors import Palette
import matplotlib.pyplot as plt
from matplotlib.text import Text
from matplotlib.patches import Patch
import matplotlib

matplotlib.rc("font", family="IBM Plex Sans")


def get_data():
    p = Palette()
    _, ax = plt.subplots(1, 1)
    df = pd.read_csv("data/budget.csv")
    df["color"] = p.gray(shade=15)
    df = df.set_index("entity")
    df.loc["Scientific Departments", "color"] = p.red()
    df = df.reset_index()
    df = df.sort_values(by="amount", ascending=False)
    squarify.plot(df["amount"].to_list(),
                  label=df["entity"].to_list(),
                  color=df["color"].to_list(),
                  pad=True)
    show = df.head(7)["entity"].to_list()
    for child in ax.get_children():
        if isinstance(child, Text):
            child.set_fontsize("13")
            child.set_fontname("IBM Plex Sans")
            if child.get_text() not in show:
                child.set_text("")
            else:
                child.set_fontsize(11)
                child.set_color(p.gray())
                if child.get_text() == "Rural Development":
                    child.set_text("Rural\nDevelopment")
                elif child.get_text() == "Transfer to States":
                    child.set_text("Transfer\nto States")
    handles = [
        Patch(fc=p.red(), label="Scientific Departments"),
        Patch(fc=p.gray(shade=15), label="Other Categories"),
    ]
    ax.set_axisbelow(True)
    plt.legend(handles=handles, loc="lower center", ncol=3,
               bbox_to_anchor=(0.5, -0.15))
    plt.title("The Union Budget 2021 Expenditure Estimates")
    plt.annotate("Source: indiabudget.gov.in",
                 xy=(0.5, -0.18), xycoords="axes fraction", ha="center",
                 color=p.gray())
    plt.tight_layout()
    plt.axis('off')
    plt.savefig("plot.png", dpi=150)
    plt.show()


def run():
    get_data()
