
import datetime
import os
import shutil
import numpy as np
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from fbprophet import Prophet

def make_forecast(stock_id):
    filelist = ["5Y", "10Y", "ALL"]

    # Set Folder Targets for Revenue Info
    # Based on 5/10/All year revenue to do the coming 5 year forecast
    for file in filelist:
        file_html =str(file)+".html"
        stock_revenue_file = Path.cwd() / stock_id / file_html
        df=pd.read_html(stock_revenue_file)[0]
        col=["月別", "單月營收(億)"]
        df=df[col]
        df.columns=["ds", "y"]
        df.ds=pd.to_datetime(df.ds)
        #print(df.head())
        m1=Prophet()
        m1.fit(df)
        future1 = m1.make_future_dataframe(periods=60, freq='MS')
        forecast1 = m1.predict(future1)
        #print(forecast1.dtypes)
        #print (forecast1[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])
        if not os.path.exists(stock_id):
            os.makedirs(stock_id)
        if not os.path.exists(f'{stock_id}/forecast/'):
            os.makedirs(f'{stock_id}/forecast/')
        forecast1.to_csv(f'{stock_id}/forecast/{file}.csv')

def get_forecast(stock_id, year=5):
    stock_revenue_file = Path.cwd() / stock_id / "ALL.html"
    df = pd.read_html(stock_revenue_file)[0]
    col = ["月別", "單月營收(億)"]
    df = df[col]
    df.columns = ["ds", "y"]
    df['forecast']='Actual'
    print("forecast is actual????")
    print(df.head())
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
    df["forecast"] = np.where(df.forecast.isna(), "forecast", "actual")
    print(df.head())
    print(df[(df.ds > "2020-12") & (df.ds < "2022-1")])
    return df[["ds","merged","forecast"]]

def plot_forecast(df,stock_id):
    fig, ax = plt.subplots(figsize=(9, 6))
    # df.plot(kind='line', x='ds', y=["y", "ALL_yhat", "10Y_yhat", "5Y_yhat"], ax=ax)
    df.plot(kind='line', x='ds', y=["merged"], ax=ax)
    fig.autofmt_xdate(bottom=0.2, rotation=30, ha='right')
    plt.title(f"STOCK ID ={stock_id}")
    plt.show(block=True)
    plt.interactive(False)

