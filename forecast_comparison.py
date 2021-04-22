
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
    EPS_per_quarte_file= Path.cwd() / stock_id / "EPS_per_quarter.csv"
    Balance_Sheet_file = Path.cwd() / stock_id / "Balance_Sheet_BS_M_QUAR.html"
    df = pd.read_html(stock_revenue_file)[0]
    df_EPS = pd.read_csv(EPS_per_quarte_file)
    df_BS = pd.read_html(Balance_Sheet_file)[0]

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

    # add column "Quarter" and "Year" and "EPS estimation"
    Q1_month = [1, 2, 3]
    Q2_month = [4, 5, 6]
    Q3_month = [7, 8, 9]
    Q4_month = [10, 11, 12]
    # add column "Quarter" and "Year"
    df["Year"]=0
    for index, row in df.iterrows():
        df.loc[index, "Year"]= row['ds'].year
        #print (row, row['ds'].year, row['ds'].month)
        month =row['ds'].month
        if month in Q1_month:
            Q_number = 'Q1'
            df.loc[index, 'Quarter'] = Q_number
            df.loc[index, 'EPS_ratio']= df_EPS[df_EPS["Quarter"]== Q_number]["稅後淨利率(母公司)"].iloc[0]
        elif month in Q2_month:
            Q_number = 'Q2'
            df.loc[index, 'Quarter'] = Q_number
            df.loc[index, 'EPS_ratio'] = df_EPS[df_EPS["Quarter"] == Q_number]["稅後淨利率(母公司)"].iloc[0]
        elif month in Q3_month:
            Q_number = 'Q3'
            df.loc[index, 'Quarter'] = Q_number
            df.loc[index, 'EPS_ratio'] = df_EPS[df_EPS["Quarter"] == Q_number]["稅後淨利率(母公司)"].iloc[0]
        else:
            Q_number = 'Q4'
            df.loc[index, 'Quarter'] = Q_number
            df.loc[index, 'EPS_ratio'] = df_EPS[df_EPS["Quarter"] == Q_number]["稅後淨利率(母公司)"].iloc[0]

    ##Todo get the captital for each stock from balance sheet
    # I put TSMC capital below to verify the formula first. This is to be udpated.

    df["capital"] = df_BS.loc[0,"普通股股本"]
    #df["capital"] = 2593
    #print("普通股股本", df["capital"])
    df["EPS_forecast"]=df["merged"]*df["EPS_ratio"]/df["capital"] * 10


    print(df.head())
    print(df[(df.ds > "2020-12") & (df.ds < "2022-1")])
    return df[["ds","merged","forecast","Quarter","Year","capital", "EPS_ratio", "EPS_forecast"]]

def plot_forecast(df,stock_id):
    fig, ax = plt.subplots(figsize=(9, 6))
    # df.plot(kind='line', x='ds', y=["y", "ALL_yhat", "10Y_yhat", "5Y_yhat"], ax=ax)
    df.plot(kind='line', x='ds', y=["merged"], ax=ax)
    fig.autofmt_xdate(bottom=0.2, rotation=30, ha='right')
    plt.title(f"STOCK ID ={stock_id}")
    plt.show(block=True)
    plt.interactive(False)

