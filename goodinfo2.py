#! /usr/bin/python
# -*- coding: utf-8 -*-
import requests
import sys
import os
import time
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
from openpyxl import load_workbook


# this can disable the requests warnings.
requests.packages.urllib3.disable_warnings()
def GetHtmlcode(ID):
    # Get the webpage's source html code
    #ID = str(ID)
    source = 'https://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID='
    url = source + ID
    #print (url)
    source_dividend = 'https://goodinfo.tw/StockInfo/StockDividendPolicy.asp?'


    # Header
    headers = {'accept': '*/*',
               'accept-encoding': 'gzip, deflate, br',
               'accept-language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2',
               'content-length': '0',
               'content-type': 'application/x-www-form-urlencoded;',
               'cookie': '__gads=ID=fe562308f92c2979:T=1511748749:S=ALNI_MZDfWP11BwzcEPLDztntanza0Uc0Q; GOOD%5FINFO%5FSTOCK%5FBROWSE%5FLIST=4%7C2324%7C2385%7C9924%7C2103; _ga=GA1.2.1450427542.1511748749; _gid=GA1.2.614910067.1512647858; SCREEN_SIZE=WIDTH=1680&HEIGHT=1050',
               'dnt': '1',
               'origin': 'https://goodinfo.tw',
               'referer': url,
               'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

    # 'PER/PBR' '獲利指標' '股利統計'
    payload = {
        u'STOCK_ID': ID,
        u'YEAR_PERIOD': u'9999',
        u'RPT_CAT': u'M_YEAR',
        u'STEP': u'DATA',
        #u'SHEET': u'股利統計'}
        u'SHEET': '獲利指標'}
        # 'SHEET': 'PER/PBR'}

    payload_dividend = {
        u'STOCK_ID': ID,
        u'SHEET': '股利所屬年度'}



    SHEETS = ['獲利指標', '年增統計', 'PER/PBR', '股利所屬年度']

    columns = {'獲利指標': ['年度', '股本(億)', '財報評分', '股價收盤', '股價平均', u'股價漲跌', u'股價漲跌(%)', u'營業收入(億)', u'營業毛利(億)',
                         u'營業利益(億)', u'業外損益(億)', u'稅後淨利(億)', u'營業毛利(%)', u'營業利益(%)', u'業外損益(%)', u'稅後淨利(%)', u'ROE(%)',
                         u'ROA(%)', u'稅後EPS(元)', u'成長(元)', u'BPS(元)'],

               u'年增統計': [u'年度', u'營業收入金額(億)', u'營業收入增減(億)', u'營業收入增減(%)', u'營業毛利金額(億)', u'營業毛利增減(億)',
                         u'營業毛利增減(%)', u'毛利(%)', u'毛利增減數', u'稅後淨利金額(億)', u'稅後淨利增減(億)', u'稅後淨利增減(%)',
                         u'稅後淨利(%)', u'稅後增減數', u'EPS(元)', u'每股盈餘增減(元)', u'ROE(%)', u'ROE增減數', u'ROA(%)', u'ROA增減數'],

               u'股利統計': [u'年度', u'股本(億)', u'財報評分', u'股價最高', u'股價最低', u'股價收盤', u'股價平均', u'股價漲跌', u'股價漲跌(%)',
                         u'去年EPS(元)', u'股利現金(元)', u'股利股票(元)', u'股利合計(元)', u'殖利率最高(%)', u'殖利率最低(%)', u'殖利率平均(%)',
                         u'盈餘分配率配息(%)', u'盈餘分配率配股(%)', u'盈餘分配率合計(%)'],

               u'PER/PBR': [u'年度', u'股本(億)', u'財報評分', u'股價最高(元)', u'股價最低(元)', u'股價收盤(元)', u'股價平均(元)', u'股價漲跌(元)',
                            u'股價漲跌(%)', u'EPS(元)', u'最高PER', u'最低PER', u'平均PER', u'BPS(元)', u'最高PBR', u'最低PBR',
                            u'平均PBR'],
               u'股利所屬年度': [u'股利所屬年度', u'股利發放年度',u'現金股利盈餘',u'現金股利公積',u'現金股利合計',u'股票股利盈餘',u'股票股利公積',u'股票股利合計',
                          u'股利合計',u'股利現金總計(億)', u'股利股票總計(千張)',u'填息花費日數',u'填權花費日數', u'股價年度', u'股價統計最高(元)',
                          u'股價統計最低(元)',u'股價統計平均(元)',u'年均殖利率現金(%)',u'年均殖利率股票(%)',u'年均殖利率合計(%)',u'股利所屬期間',
                          u'EPS(元)',u'盈餘分配率配息(%)',u'盈餘分配率配股(%)',u'盈餘分配率合計(%)']
               }

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

    labels = [u'年度',
              u'股本',
              u'財報評分',
              u'營收(億)',
              # u'稅後淨利(億)',
              # u'毛利(%)',
              # u'營益(%)',
              # u'ROE',
              # u'EPS',
              '股價收盤',
              '股價平均',
              u'股價漲跌',
              u'股價漲跌(%)',
              u'營業收入(億)',
              u'營業毛利(億)',
              u'營業利益(億)',
              u'業外損益(億)',
              u'稅後淨利(億)',
              u'營業毛利(%)',
              u'營業利益(%)',
              u'業外損益(%)',
              u'稅後淨利(%)',
              u'ROE(%)',
              u'ROA(%)',
              u'稅後EPS(元)',
              u'成長(元)',
              u'BPS(元)'
              u'獲利矩陣',
              u'現金',
              u'股票',
              u'股利合計',
              u'高低價差',
              u'最高價',
              u'最高本益比',
              u'日期',
              u'最低價',
              u'最低本益比',
              u'日期',
              u'收盤平均價',
              u'平均本益比',
              'BPS',
              '最高PBR',
              '最低PBR',
              '平均PBR'
              ]

    w, h = 38, 20
    raw_data = [['-' for x in range(w)] for y in range(h)]
    df_final = pd.DataFrame(raw_data, columns=labels)

    for key in SHEETS:
        payload['SHEET'] = key
        if key != '股利所屬年度':
            res = requests.post('https://goodinfo.tw/StockInfo/StockBzPerformance.asp?', headers=headers, verify=False, data=payload)
        else:
            res = requests.post(source_dividend, headers=headers, verify=False, data=payload_dividend)
        res.encoding = 'utf-8'
        #print(res.url)
        #print(res.text)
        soup = BeautifulSoup(res.text.replace('&nbsp;', '').replace('　', ''), 'lxml')
        [s.extract() for s in soup('thead')]  # remove thead

        df = pd.read_html(str(soup))[0]
        df.columns = columns[key]
        #print (df.info)

        if key == u'獲利指標':
            print ("key is", key)
            df_final[u'年度'] = df[u'年度']
            df_final[u'股本'] = df[u'股本(億)']
            df_final[u'財報評分'] = df[u'財報評分']

            df_final[u'營收(億)'] = df[u'營業收入(億)']
            df_final[u'稅後淨利(億)'] = df[u'稅後淨利(億)']
            df_final[u'毛利(%)'] = df[u'營業毛利(%)']
            df_final[u'營益(%)'] = df[u'營業利益(%)']
            df_final[u'ROE'] = df[u'ROE(%)']
            df_final[u'EPS'] = df[u'稅後EPS(元)']

            df_final['股價收盤'] = df['股價收盤']
            df_final['股價平均'] = df['股價平均']
            df_final[u'股價漲跌'] = df[u'股價漲跌']
            df_final[u'股價漲跌(%)'] = df[u'股價漲跌(%)']

            df_final[u'營業收入(億)'] = df[u'營業收入(億)']
            df_final[u'營業毛利(億)'] = df[u'營業毛利(億)']
            df_final[u'營業利益(億)'] = df[u'營業利益(億)']
            df_final[u'業外損益(億)'] = df[u'業外損益(億)']
            df_final[u'稅後淨利(億)'] = df[u'稅後淨利(億)']
            df_final[u'營業毛利(%)'] = df[u'營業毛利(%)']
            df_final[u'營業利益(%)'] = df[u'營業利益(%)']
            df_final[u'業外損益(%)'] = df[u'業外損益(%)']
            df_final[u'稅後淨利(%)'] = df[u'稅後淨利(%)']
            df_final[u'ROE(%)'] = df[u'ROE(%)']
            df_final[u'ROA(%)'] = df[u'ROA(%)']
            df_final[u'稅後EPS(元)'] = df[u'稅後EPS(元)']
            df_final[u'成長(元)'] = df[u'成長(元)']
            df_final[u'BPS(元)'] = df[u'BPS(元)']



        elif key == u'股利統計':
            print("key is", key)
            df_final[u'現金'] = df[u'股利現金(元)']
            df_final[u'股票'] = df[u'股利股票(元)']
            df_final[u'股利合計'] = df[u'股利合計(元)']

            # 高低價差
            h = df[u'股價最高']
            l = df[u'股價最低']

            count = 0
            for hh in h:
                if hh == u'-':
                    break
                count = count + 1

            if count > 10:
                count = 10
            # print count

            h = h[:count]
            l = l[:count]
            # raw_input()
            h = pd.to_numeric(h)
            l = pd.to_numeric(l)
            df_final[u'高低價差'] = h - l
            df_final[u'最高價'] = df[u'股價最高']
            df_final[u'最低價'] = df[u'股價最低']
        elif key == u'PER/PBR':
            print("key is", key)
            df_final[u'最高本益比'] = df[u'最高PER']
            df_final[u'最低本益比'] = df[u'最低PER']
            df_final[u'收盤平均價'] = df[u'股價平均(元)']
            df_final[u'平均本益比'] = df[u'平均PER']
            df_final[u'最高價'] = df[u'股價最高(元)']
            df_final[u'最低價'] = df[u'股價最低(元)']
            df_final[u'BPS'] = df[u'BPS(元)']
            df_final[u'最高PBR'] = df[u'最高PBR']
            df_final[u'最低PBR'] = df[u'最低PBR']
            df_final[u'平均PBR'] = df[u'平均PBR']
            # add code to remove the extra "年度" row
            df2 = df[df['年度'] == '年度'].index
            df = df.drop(df2)


            # print df_final[u'平均本益比']
            # raw_input()
        elif key == u'股利所屬年度':
            print("key is", key)
            #df = df.drop(df.index[-1])

            df_final['年度']=df_final['年度'].astype(object)
            # print (df.dtypes)
            # print (df_final.dtypes)
            result = pd.merge(df_final, df,  left_on='年度', right_on='股利所屬年度', how="left")
            # df_final[u'現金'] = df[u'現金股利合計']
            # df_final[u'股票'] = df[u'股票股利合計']
            # df_final[u'股利合計'] = df[u'股利合計']
            df_final = result

            #df_final[u'平均本益比'] = df[u'平均PER']


        key = key.replace('/', '_')

        if not os.path.exists(ID):
            os.makedirs(ID)

        key = str(ID) + '/' + key + '.html'
        # print key
        # raw_input()
        df.to_html(str(key))
        with open(str(key), 'w', encoding='utf-8') as f:
            f.write(HEADER)
            f.write(df.to_html())
            f.write(FOOTER)

    key = str(ID) + '/基本資料表.html'
    with open(str(key), 'w', encoding='utf-8') as f:
        f.write(HEADER)
        f.write(df_final.to_html(classes='df_final'))
        f.write(FOOTER)



    Excel_file = Path.cwd() / "stocks.xlsx"
    book = load_workbook(Excel_file)
    with pd.ExcelWriter(Excel_file, engine='openpyxl') as writer:
        writer.book = book
        writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
        df_final.to_excel(writer, ID, index=False)
        writer.save()


    return soup


def main():
    # python2
    #reload(sys)
    #sys.setdefaultencoding('utf-8')

    fin = open('StockCode', 'r+')
    StockCodeList = [str(i) for i in fin.read().splitlines()]
    fin.close()

    for ID in StockCodeList:
        print ("ID=", ID)
        page = GetHtmlcode(ID)
        time.sleep(1)


if __name__ == "__main__":
    main()
