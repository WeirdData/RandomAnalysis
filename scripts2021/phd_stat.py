#  Copyright (c) 2021
#  Author: Rohit Suratekar
#  This script is part of random data-analysis done in 2021.
#
#  data for PhD Awards:
#  https://timesofindia.indiatimes.com/home/education/news
#  /ugc-to-assess-quality-of-phds-awarded-in-the-last-decade/articleshow/69637531.cms
#
#  data for PhD enrolment
#  https://www.ugc.ac.in/stats.aspx,
#  https://www.ugc.ac.in/page/Other-Publications.aspx
#  file names :
#  Higher Education in India at a glance February,2012
#  Higher Education in India at a glance January, 2018
#
#
#  data for PhD Award in 2016
#  https://aishe.nic.in/aishe/viewDocument.action?documentId=245


import matplotlib.pyplot as plt
from SecretColors import Palette
from matplotlib.patches import Patch

data = [
    ("PhD", 92570, 68842),
    ("M.Phil", 12287, 21822),
    ("PG", 1891071, 2223239),
    ("Grad", 15052304, 13964046)
]

phd = [
    ("2010-11", 137000, 81000, 56000, 16093),
    ("2017-18", 161412, 92570, 68842, 34400),
]

others_labels = ["2010-11", "2012-13", "2013-14", "2014-15", "2015-16",
                 "2016-2017", "2017-18"]
others_values = [16093, 17531, 22849, 27327, 27671, 28779, 34400]


def run():
    plt.figure(figsize=(8, 6))
    p = Palette()
    award_color = p.magenta()
    enrol_color = p.cyan()
    plt.bar(len(others_labels) - 1, phd[1][1], color=enrol_color, zorder=3)
    total = sum(others_values[1:])  # Last 6 years
    x = len(others_labels) - 1
    plt.plot([x - 0.5, x + 0.5], [total, total], color="k", ls="--", zorder=3)
    plt.annotate("Total PhD awarded in last 6 years\n(2012-2018)",
                 xy=(x - 0.55, total), xytext=(x - 2.3, total - 30000),
                 ha="center", arrowprops=dict(arrowstyle="->",
                                              connectionstyle="angle",
                                              ec=p.gray(shade=70)))
    for i in range(len(others_values)):
        plt.bar(i, others_values[i], color=award_color, zorder=3)
    plt.gca().set_facecolor(p.gray(shade=20))
    plt.xticks(range(len(others_labels)), others_labels)
    plt.bar(0, phd[0][1], color=enrol_color, zorder=2)
    plt.annotate("Total PhD enrolment\nfor 2010-11",
                 xy=(0, phd[0][1] + 1000),
                 ha="center", va="bottom")
    plt.annotate("Total PhD enrolment\nfor 2017-18",
                 xy=(len(others_values) - 1, phd[1][1] + 1000),
                 ha="center", va="bottom")

    plt.annotate("Assuming average time it takes\nto complete the PhD in "
                 "India is 5-6 years with\n avg of 125K candidates "
                 "enrolling each year,\n"
                 "at the end of 6th year only 21% gets their PhD.",
                 xy=(0.5, 0.455), xycoords="axes fraction",
                 ha="center", va="center")

    plt.xlim(-1.5, len(others_values) + 0.5)
    plt.ylim(0, 190000)

    handles = [
        Patch(fc=enrol_color, label="PhD Enrolment"),
        Patch(fc=award_color, label="PhD Awarded")
    ]
    legend = plt.legend(handles=handles,
                        loc='upper left',
                        bbox_to_anchor=(0, 0.99),
                        fancybox=True,
                        ncol=2)
    frame = legend.get_frame()
    frame.set_facecolor('w')
    frame.set_alpha(1)
    plt.ylabel("Number of Candidates")
    plt.xlabel("Academic Year")
    plt.title("Total PhD Enrolment and Awards granted by UGC")
    plt.grid(axis="y", ls=":", color=p.gray(shade=50), zorder=1)
    plt.tight_layout()
    plt.savefig("plot.png", dpi=300)
    plt.show()
