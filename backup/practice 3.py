import requests
import pandas as pd
from pandas import DataFrame

url = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date=20200530&stockNo=2330'
data_temp = pd.read_html(requests.get(url).text)

data = pd.read_html(requests.get(url).text)[0]

data.columns = data.columns.droplevel(0)

data.to_csv('2330_20200201.csv', index=False)

dates = [20200201, 20200101, 20191201]
stockNo = 2330
url_template = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date={}&stockNo={}"

for date in dates:
    url = url_template.format(date, stockNo)
    file_name = "{}_{}.csv".format(stockNo, date)

    data = pd.read_html(requests.get(url).text)
    print(data)

    data.columns = data.columns.droplevel(0)
    data.to_csv(file_name, index=False)