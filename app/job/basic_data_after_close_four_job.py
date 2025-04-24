#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import datetime
import logging
import os.path
import sys

cpath_current = os.path.dirname(os.path.dirname(__file__))
cpath = os.path.abspath(os.path.join(cpath_current, os.pardir))
sys.path.append(cpath)
import app.lib.run_template as runt
import app.core.stock as StockService
import akshare as ak
import app.lib.tablestructure as tbs
import app.lib.database as mdb
import pandas as pd

__author__ = 'bytedance'
__date__ = '2025/3/31 '


def save_after_close_ashares_congestion(date):
    try:
        data = StockService.get_top_5_stock()
        top_5_total = data['成交额'].sum()

        index_zh_a_hist_df = ak.index_zh_a_hist(symbol="000001", period="daily", start_date=date, end_date=date)

        index_zh_a_hist_df.insert(1, 'code', '000001')
        index_zh_a_hist_df.insert(2, 'name', '上证指数')


        sz_index_df = ak.index_zh_a_hist(symbol="399001", period="daily", start_date=date, end_date=date)

        sz_index_df.insert(1, 'code', '399001')
        sz_index_df.insert(2, 'name', '深证指数')

        bz_index_df = ak.index_zh_a_hist(symbol="899050", period="daily", start_date=date, end_date=date)
        bz_index_df.insert(1, 'code', '899050')
        bz_index_df.insert(2, 'name', '北证50')

        index_zh_a_hist_df = pd.concat([index_zh_a_hist_df, sz_index_df, bz_index_df], ignore_index=True)


        total = index_zh_a_hist_df['成交额'].sum()

        total = round(total / 100000000, 2)
        top_5_total = round(top_5_total / 100000000, 2)

        # 拥挤度， 计算带百分号，并且保留两位小数
        congestion = round((top_5_total / total) * 100, 2)

        
        market_crowding_df = pd.DataFrame({'date': [date], 'all_a_shares_total_volume': [total], 'top_5_percent_total_volume': [top_5_total], 'crowding_ratio': [congestion]})

        table_name = tbs.TABLE_MARKET_CROWDING['name']
        if mdb.checkTableIsExist(table_name):
            del_sql = f"DELETE FROM `{table_name}` where `date` = '{date}'"
            mdb.executeSql(del_sql)
            cols_type = None
        else:
            cols_type = tbs.get_field_types(tbs.TABLE_MARKET_CROWDING['columns'])
        mdb.insert_db_from_df(market_crowding_df, table_name, cols_type, False, "`date`")


    except Exception as e:
        logging.error(f"basic_data_other_daily_job.save_stock_index_daily_hist处理异常:{e}")

def save_after_close_stock_a_spot(date, before=True):
    if before:
        return
    try:
        data = ak.stock_zh_a_spot_em()
        if data is None:
            return
        table_name = tbs.TABLE_STOCK_ZH_A_SPOT['name']
        # 删除老数据。
        if mdb.checkTableIsExist(table_name):
            del_sql = f"DELETE FROM `{table_name}` where `date` = '{date}'"
            mdb.executeSql(del_sql)
            cols_type = None
        else:
            cols_type = tbs.get_field_types(tbs.TABLE_STOCK_ZH_A_SPOT['columns'])
        df = data.rename(columns=tbs.TABLE_STOCK_ZH_A_SPOT['header_mapping'])
        df.drop(columns=tbs.TABLE_STOCK_ZH_A_SPOT['drop_fields'], inplace=True)
        df.insert(0, 'date', date)

        df = df[~df['code'].str.startswith('900')]
        df = df[~df['code'].str.startswith('200')]
        df = df[df['change_rate'].notnull()]

        mdb.insert_db_from_df(df, table_name, cols_type, False, "`date`,`code`")
    except Exception as e:
        logging.error(f"basic_data_daily_job.save_stock_spot_data处理异常：{e}")




def main():
    runt.run_with_args(save_after_close_ashares_congestion)
    runt.run_with_args(save_after_close_stock_a_spot)


# main函数入口
if __name__ == '__main__':
    main()
