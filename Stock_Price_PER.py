import pandas as pd
from pathlib import Path




def GetPER(stock_id):
    PER_file = Path.cwd() / stock_id / "PER_PBR.html"
    df_PER = pd.read_html(PER_file)[0]
    print(df_PER.head())
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
    print(EPS_yearly)


def main():

    fin = open('StockCode', 'r+')
    StockCodeList = [str(i) for i in fin.read().splitlines()]
    fin.close()

    for ID in StockCodeList:
        print("ID=", ID)
        max_PER, min_PER, avg_PER = GetPER(ID)
        print (ID, max_PER, min_PER, avg_PER)
        GetEPS(ID)


if __name__ == "__main__":
    main()