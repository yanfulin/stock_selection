
import datetime
import os
import shutil
import numpy as np
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from fbprophet import Prophet

def forecast(stock_id, year=5):
    stock_revenue_file = Path.cwd() / stock_id / "ALL.html"
    df = pd.read_html(stock_revenue_file)[0]
    col = ["月別", "單月營收(億)"]
    df = df[col]
    df.columns = ["ds", "y"]
    df.ds = pd.to_datetime(df.ds)

    df_5Y = pd.read_csv(f"{stock_id}/forecast/5Y.csv")
    df_10Y = pd.read_csv(f"{stock_id}/forecast/10Y.csv")
    df_ALL = pd.read_csv(f"{stock_id}/forecast/ALL.csv")

    df_5Y = df_5Y[["ds", "yhat"]].rename(columns={"yhat": "5Y_yhat"})
    df_5Y.ds = pd.to_datetime(df_5Y.ds)
    df_10Y = df_10Y[["ds", "yhat"]].rename(columns={"yhat": "10Y_yhat"})
    df_10Y.ds = pd.to_datetime(df_10Y.ds)
    df_ALL = df_ALL[["ds", "yhat"]].rename(columns={"yhat": "ALL_yhat"})
    df_ALL.ds = pd.to_datetime(df_ALL.ds)

    df = pd.merge(df_ALL, df, how='left', on='ds')
    df = df.merge(df_10Y, how="left", on='ds')
    df = df.merge(df_5Y, how="left", on='ds')
    if year==5:
        df["merged"] = np.where(df.y.isna(), df["5Y_yhat"], df.y)
    elif year==10:
        df["merged"] = np.where(df.y.isna(), df["10Y_yhat"], df.y)
    else:
        df["merged"] = np.where(df.y.isna(), df["ALL_yhat"], df.y)
    print(df.head())
    print(df[(df.ds > "2020-12") & (df.ds < "2022-1")])
    return df[["ds","merged"]]

def plot_forecast(df):
    fig, ax = plt.subplots(figsize=(9, 6))
    # df.plot(kind='line', x='ds', y=["y", "ALL_yhat", "10Y_yhat", "5Y_yhat"], ax=ax)
    df.plot(kind='line', x='ds', y=["merged"], ax=ax)
    fig.autofmt_xdate(bottom=0.2, rotation=30, ha='right')
    plt.show(block=True)
    plt.interactive(False)

