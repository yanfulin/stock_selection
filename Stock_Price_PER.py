import pandas as pd
from pathlib import Path
from openpyxl import load_workbook
from datetime import date




def GetPER(stock_id):
    PER_file = Path.cwd() / stock_id / "PER_PBR.html"
    df_PER = pd.read_html(PER_file)[0]
    #print(df_PER.head())
    max_PER=float(df_PER.loc[1,"最高PER"])
    min_PER=float(df_PER.loc[1,"最低PER"])
    avg_PER=float(df_PER.loc[1,"平均PER"])
    return max_PER, min_PER, avg_PER

def GetEPS(stock_id):
    max_PER, min_PER, avg_PER = GetPER(stock_id)
    print(stock_id, max_PER, min_PER, avg_PER)
    EPS_file = Path.cwd() / stock_id / "forecast" / "forecast_actual_merged.csv"
    EPS_yearly_file = Path.cwd() / stock_id / "forecast" / "EPS_yearly.csv"
    df_EPS = pd.read_csv(EPS_file)
    EPS_yearly = df_EPS.groupby("Year")["EPS_forecast"].sum().round(2)
    EPS_yearly = pd.DataFrame({'Year': EPS_yearly.index, 'EPS': EPS_yearly.values})

    EPS_yearly["max_stock_price"]= (max_PER * EPS_yearly["EPS"]).round(1)
    EPS_yearly["avg_stock_price"] = (avg_PER * EPS_yearly["EPS"]).round(1)
    EPS_yearly["min_stock_price"] = (min_PER * EPS_yearly["EPS"]).round(1)
    EPS_yearly.to_csv(EPS_yearly_file)
    this_year=date.today().year
    three_year_EPS=EPS_yearly.loc[(EPS_yearly["Year"]>=this_year-1),"EPS"].values[0:3]

    #print(three_year_EPS)
    return three_year_EPS

def export_to_excel(stock_id):
    Excel_file = Path.cwd() / "stocks.xlsx"
    wb = load_workbook(Excel_file)
    sheet = wb['evaluation']
    # data = sheet.values
    # data =list(data)
    # stock_list2 = [r[0] for r in data]
    # print(stock_list2)



def export_to_excel2():
    Excel_file = Path.cwd() / "stocks.xlsx"
    wb = load_workbook(Excel_file)
    sheet = wb['evaluation']
    #print (sheet.values)
    stock_list=[]
    for row in sheet["A"]:
            stock_list.append(row.value)
    # stock list: some are in text. some are int. Needs to convert them to right format
    # Get the corresponding EPS and PER and write them into the right position
    for index, stock in enumerate(stock_list, start=1):
        #print(index, stock)
        if index ==1:
            pass
        else:
            stock = str(stock)
            print(stock)
            EPS = GetEPS(stock)
            PER_max, PER_avg, PER_min = GetPER(stock)
            print (EPS[0])
            sheet.cell(row=index, column=15).value = EPS[0]
            sheet.cell(row=index, column=16).value = EPS[1]
            sheet.cell(row=index, column=17).value = EPS[2]
            sheet.cell(row=index, column=18).value = PER_max
            sheet.cell(row=index, column=19).value = PER_avg
            sheet.cell(row=index, column=20).value = PER_min
            wb.save(Excel_file)





def main():
    fin = open('StockCode', 'r+')
    StockCodeList = [str(i) for i in fin.read().splitlines()]
    fin.close()
    print(StockCodeList)

    for ID in StockCodeList:
        print("ID=", ID)
        max_PER, min_PER, avg_PER = GetPER(ID)
        EPS = GetEPS(ID)
        #print (ID, max_PER, min_PER, avg_PER)
        print ("2020 EPS=" , EPS)
    export_to_excel2()



if __name__ == "__main__":
    main()