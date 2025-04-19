import requests
import pandas as pd
from io import StringIO
import app.lib.tablestructure as tbs
import app.lib.database as mdb


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36",
    "Content-Type": "application/json"
}

def get_stock_market_activity():
    url = "https://legulegu.com/stockdata/ashares-congestion"
    r = requests.get(url, headers=headers)
    data = pd.read_html(StringIO(r.text))[1]
    date = "2025-04-18"
    
    # 去掉收盘价这一列
    data = data.drop(columns=['收盘价'])
    # 第一列表头设置为date，后面为top_5_percent_total_volume , 
    data.columns = ['date', 'top_5_percent_total_volume', 'all_a_shares_total_volume', 'crowding_ratio']

    table_name = tbs.TABLE_MARKET_CROWDING['name']

    if mdb.checkTableIsExist(table_name):
        del_sql = f"DELETE FROM `{table_name}` where `date` = '{date}'"
        mdb.executeSql(del_sql)
        cols_type = None
    else:
        cols_type = tbs.get_field_types(tbs.TABLE_MARKET_CROWDING['columns'])
    mdb.insert_db_from_df(data, table_name, cols_type, False, "`date`")




def main():
    data = get_stock_market_activity()

    print(data)
    pass

if __name__ == '__main__':
    main()