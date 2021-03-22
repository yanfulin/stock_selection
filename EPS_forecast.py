# ! /usr/bin/python
# -*- coding: utf-8 -*-
import requests
import sys
import os
import time
from bs4 import BeautifulSoup
import pandas as pd

#TODO: estimate the quarterly EPS

# get the monthly revenue and convert it to quarterly data (use resample("Q"))
# get the historical EPS per quarter
## https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=XX_M_QUAR_ACC&STOCK_ID=2330
# Estimate the EPS based on quarterly revenue forecast




# this can disable the requests warnings.
requests.packages.urllib3.disable_warnings()


def GetEPScode(ID):
    # Get the webpage's source html code
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

    payload = {
        'STOCK_ID': ID,
        'REP_CAT': 'XX_M_QUAR_ACC'}

    SHEETS = ['Quarter_EPS']

    columns = {'Quarter_EPS': ['2020Q3', '2020Q2', '2020Q1',
                                  '2019Q4', '2019Q3', '2019Q2', '2019Q1',
                                  '2018Q4', '2018Q3', '2091Q2'],
               'Quarter_EPS2': ['Q1', 'Q2', 'Q3', 'Q4',
                                  'Q5', 'Q6', 'Q7', 'Q8',
                                  'Q9', 'Q10']}

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
        payload['CHT_CAT'] = key

        res = requests.post('https://goodinfo.tw/StockInfo/StockFinDetail.asp?', headers=headers, verify=False,
                            data=payload)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text.replace('&nbsp;', '').replace('　', ''), 'lxml')
        [s.extract() for s in soup('thead')]  # remove thead
        df = pd.read_html(str(soup))[1]
        df.columns = columns[key]
        print(df)

        key = key.replace('/', '_')

        if not os.path.exists(ID):
            os.makedirs(ID)

        key = str(ID) + '/' + key + '.html'
        df.to_html(str(key))
        with open(str(key), 'w', encoding='utf-8') as f:
            f.write(HEADER)
            f.write(df.to_html())
            f.write(FOOTER)

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
