# ! /usr/bin/python
# -*- coding: utf-8 -*-
import requests
import sys
import os
import time
from bs4 import BeautifulSoup
import pandas as pd
import re

#TODO: estimate the quarterly EPS
#TODO: estimate the yearly EPS, backward 4Q PES, forward 4Q PES

# get the monthly revenue and convert it to quarterly data (use resample("Q"))
# get the historical EPS per quarter
## https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=XX_M_QUAR_ACC&STOCK_ID=2330
# Estimate the EPS based on quarterly revenue forecast




# this can disable the requests warnings.
requests.packages.urllib3.disable_warnings()


def GetEPScode(ID):
    # Get the webpage's source html code 財務比率表 (合併)
    source = 'https://goodinfo.tw/StockInfo/StockFinDetail.asp?STOCK_ID='
    url = source + ID
    print(url)

    # Header
    headers = {'accept': '*/*',
               'accept-encoding': 'gzip, deflate, br',
               'accept-language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2',
               'content-length': '0',
               'content-type': 'application/x-www-form-urlencoded;',
               'cookie': '__gads=ID=fe562308f92c2979:T=1511748749:S=ALNI_MZDfWP11BwzcEPLDztntanza0Uc0Q; GOOD%5FINFO%5FSTOCK%5FBROWSE%5FLIST=4%7C2324%7C2385%7C9924%7C2103; _ga=GA1.2.1450427542.1511748749; _gid=GA1.2.614910067.1512647858; SCREEN_SIZE=WIDTH=1680&HEIGHT=1050',
               'dnt': '1',
               'origin': 'http://goodinfo.tw',
               'referer': url,
               'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

    # < option
    # value = 'XX_M_QUAR' > 合併報表 – 單季 < / option >
    # < option
    # value = 'XX_M_QUAR_ACC' > 合併報表 – 累季 < / option >
    # < option
    # value = 'XX_M_YEAR'
    # selected > 合併報表 – 年度 < / option >
    # < option
    # value = 'XX_M_Y4Q' > 合併報表 – 近四季 < / option >
    # < option
    # value = 'XX_QUAR' > 個別報表 – 單季 < / option >

    payload = {
        'STEP': 'DATA',
        'STOCK_ID': ID,
        'RPT_CAT': 'XX_M_QUAR',
        #'RPT_CAT':'XX_M_QUAR_ACC'
        # 'RPT_CAT': 'XX_M_YEAR'
        # 'QRY_TIME': '20204'
        # 'RPT_CAT':'XX_M_Y4Q'
        # 'QRY_TIME': '2020'
        #'QRY_TIME': '20204'
        }
    # value = 'XX_M_QUAR' > 合併報表 – 單季 < / option >
    SHEETS = ['XX_M_QUAR']

    # columns = {'XX_M_QUAR': ['2004Q4','2020Q3', '2020Q2', '2020Q1',
    #                               '2019Q4', '2019Q3', '2019Q2', '2019Q1',
    #                               '2018Q4', '2018Q3', '2091Q2'],
    #            'Quarter_EPS2': ['Q1', 'Q2', 'Q3', 'Q4',
    #                               'Q5', 'Q6', 'Q7', 'Q8',
    #                               'Q9', 'Q10']}

    HEADER = '''
    <!DOCTYPE html> 
    <html  lang="zh-Hant-TW">
	<head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	</head>
	<body>
    '''
    FOOTER = '''
	</body>
    </html>
    '''

    for key in SHEETS:
        payload['RPT_CAT'] = key

        res = requests.post('https://goodinfo.tw/StockInfo/StockFinDetail.asp?', headers=headers, verify=False,
                            data=payload)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text.replace('&nbsp;', '').replace('　', ''), 'lxml')
        #[s.extract() for s in soup('thead')] # remove thead
        #[s.find_parent('tr').extract() for s in soup.find_all('td', style=re.compile(r"color:blue;width:25%"))]
        #找到td style = color:blue ,然後往上一層找tr, extract結果
        [s.find_parent('tr').extract() for s in soup.find_all('td', style=lambda value: value and 'color:blue' in value)[1:]]

        df = pd.read_html(str(soup))[1]
        # duplicate the first row as the columns name
        df.columns = df.iloc[0]
        #df.index.name = "Financial_Ratio"
        df.columns.name =""
        df=df.drop([0]).T

        df.columns = df.iloc[0]
        df.columns.name =""
        df = df.drop(["獲利能力"])

        #print (df)

        #print(df[["獲利能力"]].head(20))
        #EPS = df[df["獲利能力"]=="每股稅後盈餘(元)"].T
        EPS=df[["稅後淨利率(母公司)","每股稅後盈餘(元)"]]
        EPS["每股稅後盈餘(元)"]=EPS["每股稅後盈餘(元)"].astype(float)
        EPS["稅後淨利率(母公司)"] = EPS["稅後淨利率(母公司)"].astype(float)*0.01
        EPS["date"] = pd.to_datetime(EPS.index)
        #EPS["date"]=EPS["date"].dt.to_period("Q").dt.end_time.dt.date
        EPS["quarter_end"] = EPS["date"].dt.to_period("Q").dt.end_time
        EPS["quarter_end"] = EPS["quarter_end"].dt.strftime("%Y-%m-%d")
        EPS=EPS.set_index("quarter_end")
        print(EPS)

        # add column "Quarter" and "Year" and "EPS estimation"
        Q1_month = [1, 2, 3]
        Q2_month = [4, 5, 6]
        Q3_month = [7, 8, 9]
        Q4_month = [10, 11, 12]
        print(EPS.info)
        print(EPS.dtypes)

        EPS["Year"] = EPS.date.dt.year
        EPS["Month"] = EPS.date.dt.month
        for index, row in EPS.iterrows():
            if row['Month'] in Q1_month:
                EPS.loc[index, 'Quarter'] = 'Q1'
            elif row['Month'] in Q2_month:
                EPS.loc[index, 'Quarter'] = 'Q2'
            elif row['Month']in Q3_month:
                EPS.loc[index, 'Quarter'] = 'Q3'
            else:
                EPS.loc[index, 'Quarter'] = 'Q4'

        key = key.replace('/', '_')

        if not os.path.exists(ID):
            os.makedirs(ID)
        # add one comment
        key = str(ID) + '/' + key + '.html'
        df.to_html(str(key))
        with open(str(key), 'w', encoding='utf-8') as f:
            f.write(HEADER)
            f.write(df.to_html())
            f.write(FOOTER)

        EPS_file = str(ID) + '/' + 'EPS_per_quarter.csv'
        EPS.to_csv(EPS_file)

    return soup


def main():

    fin = open('StockCode', 'r+')
    StockCodeList = [str(i) for i in fin.read().splitlines()]
    fin.close()

    for ID in StockCodeList:
        print("ID=", ID)
        page = GetEPScode(ID)
        time.sleep(10)


if __name__ == "__main__":
    main()
