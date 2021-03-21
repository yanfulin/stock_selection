import datetime
import os
import shutil
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
#print(matplotlib.get_backend())
#matplotlib.use('Agg')
from fbprophet import Prophet
import forecast_comparison

## Set Date Formats
today_string = datetime.datetime.today().strftime('%m%d%Y_%I%p')
today_string2 = datetime.datetime.today().strftime('%b %d, %Y')

# Goodinfo provides 5years/10years/ALL monthly revenue
filelist = ["5Y", "10Y", "ALL"]

# Set Folder Targets for Revenue Info
# Based on 5/10/All year revenue to do the coming 5 year forecast
for file in filelist:
    stock_id = "2330"
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

forecast_5y=forecast_comparison.forecast(stock_id, 5)
forecast_5y.to_csv(f'{stock_id}/forecast/forecast_actual_merged.csv')
forecast_comparison.plot_forecast(forecast_5y)