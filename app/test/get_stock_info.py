from datetime import datetime

import akshare as ak
import pandas as pd
import app.core.stock as stock


if __name__ == "__main__":
    sz_index_df = ak.index_zh_a_hist(symbol="899050", period="daily", start_date="20250418", end_date="20250418")

    print(sz_index_df)
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20170301", end_date='20240528', adjust="")
    print(stock_zh_a_hist_df)
    stock_sse_summary_df = ak.stock_sse_summary()
    print(stock_sse_summary_df)
    stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
    print(stock_zh_a_spot_em_df.columns.tolist())


    macro_china_urban_unemployment_df = ak.macro_china_urban_unemployment()
    print(macro_china_urban_unemployment_df)
    stock_zt_pool_dtgc_em_df = ak.stock_zt_pool_zbgc_em(date='20250403')

    bb = stock_zt_pool_dtgc_em_df.columns.tolist()
    print(bb)

    print(stock_zt_pool_dtgc_em_df)

    data = {
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'city': ['New York', 'London', 'Paris']
    }
    df = pd.DataFrame(data)

    # 将DataFrame转换为记录列表的JSON格式
    json_data = df.to_json(orient='records')
    print(json_data)

    stock_individual_info_em_df = ak.stock_individual_info_em(symbol="600000")
    print(stock_individual_info_em_df)
    stock_zt_pool_em_df = ak.stock_zt_pool_em(date='20250401')
    print(stock_zt_pool_em_df)

    # 获取stock_zt_pool_em_df 中连板数最高一行数据

    max_zt_num = stock_zt_pool_em_df['连板数'].max()
    max_zt_num_row = stock_zt_pool_em_df[stock_zt_pool_em_df['连板数'] == max_zt_num]
    print(max_zt_num_row)

    l = stock_zt_pool_em_df.columns.tolist()



    df = ak.tool_trade_date_hist_sina()





