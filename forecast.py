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
import time

import Stock_Price_PER
import forecast_comparison
import EPS_forecast
import goodinfo_revenue_monthly
import goodinfo_balance_sheet
import goodinfo2
import Stock_Price_PER
from openpyxl import load_workbook


def Get_StockCodeList():
    Excel_file = Path.cwd() / "stocks.xlsx"
    wb = load_workbook(Excel_file)
    sheet = wb['evaluation']
    #print (sheet.values)
    colnames = ["Stock ID","Chinese Name","Name","Current Price","52W High","52W Low","Beta","Market Cap","PBR","PER",
                "Target Price","Rick's PER","Comment","短中長投資屬性",
                "Dividend","Yield %","Previous Year EPS","This Year EPS","Next Year EPS", "Max PER","Min PER","Avg PER",
                "Price @ High PER","Price @ Avg PER","Price @ Min PER",
                "2010 Q1 EPS", "2010 Q2 EPS", "2010 Q3 EPS", "2010 Q4 EPS",
                "2011 Q1 EPS","2011 Q2 EPS","2011 Q3 EPS","2011 Q4 EPS",
                "2012 Q1 EPS","2012 Q2 EPS","2012 Q3 EPS","2012 Q4 EPS",
                "2010 Total EPS","2011 Total EPS","2012 Total EPS",
                "過去五年平均配息％","股利", "Yield %", "PER High","PER Low","Price @High PE", "Price @Low PE",
                "Price@Low PE- Market Price", "Price @6% Yield"]
    col_indices = {n: cell.value for n, cell in enumerate(sheet['1']) if cell.value in colnames}
    print (col_indices)
    stock_list=[]
    for row in sheet["A"]:
            if row.value != None:
                #print ("row===>", row.value)
                stock_list.append(str(row.value))
    print(stock_list[1:])
    return stock_list[1:]

def main():

    StockCodeList = Get_StockCodeList()
    # fin = open('StockCode', 'r+')
    # StockCodeList = [str(i) for i in fin.read().splitlines()]
    # fin.close()

    for stock_id in StockCodeList:
        print ("ID=", stock_id)
        goodinfo2.GetHtmlcode(stock_id)
        goodinfo_revenue_monthly.GetHtmlcode(stock_id)
        goodinfo_balance_sheet.Get_Balance_sheet_code(stock_id)
        goodinfo_balance_sheet.Get_Income_statement_code(stock_id)
        EPS_forecast.GetEPScode(stock_id)
        forecast_comparison.make_forecast(stock_id)
        forecast_10y=forecast_comparison.get_forecast2(stock_id, 10)
        print("forecast==>", forecast_10y)
        forecast_10y.to_csv(f'{stock_id}/forecast/forecast_actual_merged.csv')

    Stock_Price_PER.export_to_excel2()
        #comment
        #forecast_comparison.plot_forecast(forecast_10y, stock_id)


        #######test code is here######
        # forecast_10y = forecast_comparison.get_forecast2(stock_id, 10)
        # print("forecast==>", forecast_10y)

if __name__ == "__main__":
    main()