#! /usr/bin/python
# -*- coding: utf-8 -*-
import requests
import sys
import os
import time
from bs4 import BeautifulSoup
from bs4 import *
import pandas as pd

# this can disable the requests warnings.
requests.packages.urllib3.disable_warnings()

def Get_Balance_sheet_code(ID):
    # Get the webpage's source html code
    source = 'https://goodinfo.tw/StockInfo/StockFinDetail.asp?'
    url = source + ID
    print (url)

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
        'STEP':  'DATA',
        'RPT_CAT': 'BS_M_QUAR'
        #'QRY_Time':'2020'
        }

    SHEETS = ['BS_M_QUAR', 'BS_M_YEAR']

    # columns = {'5Y': ['月別', '開盤', '收盤', '最高', '最低', '股價漲跌(元)', '股價漲跌(%)', '單月營收(億)', '單月月增(%)', '單月年增(%)',
    #                   '累計營收(億)', '累計月增(%)', '累計年增(%)', '合併營業收入單月月增(%)', '合併營業收入單月年增(%)',
    #                   '合併營業收入累計月增(%)', '合併營業收入累計年增(%)'],
    #
    #            '10Y': ['月別', '開盤', '收盤', '最高', '最低', '股價漲跌(元)', '股價漲跌(%)', '單月營收(億)', '單月月增(%)', '單月年增(%)',
    #                   '累計營收(億)', '累計月增(%)', '累計年增(%)', '合併營業收入單月月增(%)', '合併營業收入單月年增(%)',
    #                   '合併營業收入累計月增(%)', '合併營業收入累計年增(%)'],
    #            'ALL': ['月別', '開盤', '收盤', '最高', '最低', '股價漲跌(元)', '股價漲跌(%)', '單月營收(億)', '單月月增(%)', '單月年增(%)',
    #                   '累計營收(億)', '累計月增(%)', '累計年增(%)', '合併營業收入單月月增(%)', '合併營業收入單月年增(%)',
    #                   '合併營業收入累計月增(%)', '合併營業收入累計年增(%)']}

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

        res = requests.post('https://goodinfo.tw/StockInfo/StockFinDetail.asp?', headers=headers, verify=False, data=payload)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text.replace('&nbsp;', '').replace('　', ''), 'html.parser')

        [s.find_parent('tr').extract() for s in
        soup.find_all('td', style=lambda value: value and 'color:blue' in value)[1:]]
        [s.find_parent('tr').extract() for s in
         soup.find_all('td', string="金額")]


        df = pd.read_html(str(soup))[1]

        df.iloc[1]=df.iloc[1].shift(-1)
        df.drop(columns=[15], inplace=True, axis=1)
        df=df.T
        df.columns = df.iloc[0]
        df.drop(0, inplace=True, axis=0)
        df.columns.name = ""
        df=df.reset_index(drop=True)

        #print (df)

        key = key.replace('/', '_')

        if not os.path.exists(ID):
            os.makedirs(ID)

        key = str(ID) + '/Balance_Sheet_' + key + '.html'
        df.to_html(str(key))
        with open(str(key), 'w', encoding='utf-8') as f:
            f.write(HEADER)
            f.write(df.to_html())
            f.write(FOOTER)

    return soup


def Get_Income_statement_code(ID):
    # Get the webpage's source html code
    source = 'https://goodinfo.tw/StockInfo/StockFinDetail.asp'
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
        'STEP': 'DATA',
        'RPT_CAT': 'IS_M_QUAR'
        # 'QRY_Time':'2020'
    }

    SHEETS = ['IS_M_QUAR','IS_M_QUAR_ACC']


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
        soup = BeautifulSoup(res.text.replace('&nbsp;', '').replace('　', ''), 'html.parser')

        [s.find_parent('tr').extract() for s in
         soup.find_all('td', style=lambda value: value and 'color:blue' in value)[1:]]
        [s.find_parent('tr').extract() for s in
         soup.find_all('td', string="金額")]

        df = pd.read_html(str(soup))[1]

        df.iloc[1] = df.iloc[1].shift(-1)
        df.drop(columns=[15], inplace=True, axis=1)
        df = df.T
        df.columns = df.iloc[0]
        df.drop(0, inplace=True, axis=0)
        df.columns.name = ""
        df = df.reset_index(drop=True)

        #print(df)

        key = key.replace('/', '_')

        if not os.path.exists(ID):
            os.makedirs(ID)

        key = str(ID) + '/Income_statement_' + key + '.html'
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
        print ("ID=", ID)
        page = Get_Balance_sheet_code(ID)
        page2 = Get_Income_statement_code(ID)
        time.sleep(1)

if __name__ == "__main__":
    main()
