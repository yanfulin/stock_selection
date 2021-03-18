#! /usr/bin/python
# -*- coding: utf-8 -*-
from imp import reload
import requests
import sys
import os
import time
import sqlite3
from bs4 import BeautifulSoup
import pandas as pd


def GetHtmlcode(ID):
    # Get the webpage's source html code
    source = 'http://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID='
    url = source + ID
    print(url)
    # 設定headers
    headers2 = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
    # Header
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'Big5,utf-8;q=0.7,*;q=0.3',
        # 'Accept-Encoding' : 'gzip,deflate,sdch',
        'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,ja;q=0.2',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie' : '__gads=ID=a9b4db3df9875a51:T=1491062185:S=ALNI_MahBgxXa6B0VuRdoVYVNbFF3PYmbQ; GOOD%5FINFO%5FSTOCK%5FBROWSE%5FLIST=2%7C1301%7C2311; ASPSESSIONIDSCADSSBR=BJJLMMCAPPLDLCHKCNDJIBCG; ASPSESSIONIDQCCCQSCR=CGPPIMCAPHAOLODAHJLPKAIG; ASPSESSIONIDSAACQRDR=LMENOMCAGIHGEEIDJNCJDKJL; ASPSESSIONIDSABARTCR=DDFPGMCALMLHHEJPNJDIBCGC; _ga=GA1.2.1896088280.1491062185; _gat=1; SCREEN_SIZE=WIDTH=1920&HEIGHT=1080',
        # 'Host' : 'www.goodinfo.tw',
        # 'Referer' : url
        }
    columns = {u'獲利指標': [u'年度', u'股本(億)', u'財報評分', u'股價收盤', u'股價平均', \
                         u'股價漲跌', u'股價漲跌(%)', u'營業收入(億)', u'營業毛利(億)', \
                         u'營業利益(億)', u'業外損益(億)', u'稅後淨利(億)', u'營業毛利(%)', \
                         u'營業利益(%)', u'業外損益(%)', u'稅後淨利(%)', u'ROE(%)', \
                         u'ROA(%)', u'稅後EPS(元)', u'成長(元)', u'BPS(元)'],
               u'年增統計': [u'年度', u'營業收入金額(億)', u'營業收入增減(億)', \
                         u'營業收入增減(%)', u'營業毛利金額(億)', u'營業毛利增減(億)', \
                         u'營業毛利增減(%)', u'毛利(%)', u'毛利增減數', \
                         u'稅後淨利金額(億)', u'稅後淨利增減(億)', u'稅後淨利增減(%)', \
                         u'稅後淨利(%)', u'稅後增減數', u'EPS(元)', u'每股盈餘增減(元)', \
                         u'ROE(%)', u'ROE增減數', u'ROA(%)', u'ROA增減數'],
               u'股利統計': [u'年度', u'股本(億)', u'財報評分', u'股價最高', u'股價最低',
                         u'股價收盤', u'股價平均', u'股價漲跌', u'股價漲跌(%)',
                         u'去年EPS(元)', u'股利現金(元)', u'股利股票(元)', u'股利合計(元)',
                         u'殖利率最高(%)', u'殖利率最低(%)', u'殖利率平均(%)',
                         u'盈餘分配率配息(%)', u'盈餘分配率配股(%)', u'盈餘分配率合計(%)'],
               u'PER/PBR': [u'年度', u'股本(億)', u'財報評分', u'股價最高(元)',
                            u'股價最低(元)', u'股價收盤(元)', u'股價平均(元)',
                            u'股價漲跌(元)', u'股價漲跌(%)', u'EPS(元)',
                            u'最高PER', u'最低PER', u'平均PER', u'BPS(元)',
                            u'最高PBR', u'最低PBR', u'平均PBR']
               }
    payload = {
        u'STOCK_ID': ID,
        u'YEAR_PERIOD': u'9999',
        u'RPT_CAT': u'M_YEAR',
        u'STEP': u'DATA',
        u'SHEET': u'股利統計'}
    res2 = requests.get(url, headers=headers2, data=payload)
    res2.encoding = "utf-8"
    # res = requests.post('http://goodinfo.tw/StockInfo/StockBzPerformance.asp?', headers=headers, verify=False, data = payload, allow_redirects=False)
    # res.encoding = 'utf-8'
    soup = BeautifulSoup(res2.text.replace('&nbsp;', '').replace('　', ''), 'lxml')
    #print("soup==>", soup('thead'))
    [s.extract() for s in soup('thead')]  # remove thead
    print("soup22222==>", soup)
    df = pd.read_html(str(soup))
    print("df===========>",df)
    df.columns = columns[u'股利統計']
    df.insert(0, u'股票代碼', pd.Series([ID for x in range(len(df[u'年度']))], index=df.index))
    print(df)
    # raw_input()

    with sqlite3.connect('finance.sqlite') as db:
        df.to_sql('trading_volume', con=db, if_exists='append')


def main():
    # python2
    reload(sys)
    # sys.setdefaultencoding('utf-8')

    fin = open('StockCode', 'r+')
    StockCodeList = [str(i) for i in fin.read().splitlines()]
    fin.close()

    for ID in StockCodeList:
        GetHtmlcode(ID)
        time.sleep(10)


if __name__ == "__main__":
    main()
