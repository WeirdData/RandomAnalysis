#  Copyright (c) 2021
#  Author: Rohit Suratekar
#  This script is part of random data-analysis done in 2021.
#
#  Data from :
#  https://www.kaggle.com/utkarshxy/who-worldhealth-statistics-2020-complete


import pandas as pd


def medical_doctors():
    df = pd.read_csv("data/health/medicalDoctors.csv")
    flow = pd.read_csv("data/flourish.csv")
    del df["Indicator"]
    df = pd.pivot_table(df, values="First Tooltip", index="Location",
                        columns="Period")
    flow = flow.set_index("Country Name")
    df = pd.concat([flow, df], axis=1)
    df = df.rename_axis("Country Name")
    df = df.reset_index()
    df.to_csv("data.csv", index=False)


def basic_water():
    df = pd.read_csv("data/health/basicDrinkingWaterServices.csv")
    df = df.sort_values(by="Period")
    df = df.drop_duplicates(subset=["Location"], keep="last")
    df = df[df["Period"] == 2017]
    df = df[["Location", "First Tooltip"]].sort_values(by="Location")
    df.to_csv("basicDrinkingWater.csv", index=False)


def run():
    basic_water()
