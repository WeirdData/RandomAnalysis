#  Copyright (c) 2020
#  Author: Rohit Suratekar
#  This script is part of random data-analysis done in 2020.
#

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from typing import List


def adjust_text(texts: List[plt.Text]):
    plt.draw()
    r = plt.gca().renderer()
    for text in texts:
        print(text.get_bbox_patch())
