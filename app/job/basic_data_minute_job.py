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
import akshare as ak
import app.core.stock as stock
import app.lib.tablestructure as tbs
import app.lib.database as mdb
import app.lib.trade_time as trd
import pandas as pd

__author__ = 'bytedance'
__date__ = '2025/04/09 '


def save_nph_stock_board_industry(date, before=True):
    if before:
        return
    if date != datetime.datetime.now().date():
        return

    if not trd.is_trade_date(date):
        return

    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    if not trd.is_fetch_time(now_time):
        return
    try:

        board_industry_data = ak.stock_board_industry_name_em()
        if board_industry_data is None:
            return

        # 新建一个总的df， 新增一列industry_code， 后续遍历板块代码， 然后获取板块下的股票列表， 然后合并到总的df中
        # 对stock_board_industry_name 进行遍历
        total_stock_df = pd.DataFrame()

        for index, row in board_industry_data.iterrows():
            stock_board_industry_cons_em_df = stock.get_stock_board_industry_cons(symbol=row['板块代码'])
            if stock_board_industry_cons_em_df is None:
                continue
            stock_board_industry_cons_em_df.insert(0, 'date', now_time)
            stock_board_industry_cons_em_df.insert(1, 'board_code', row['板块代码'])
            stock_board_industry_cons_em_df.insert(2, 'board_name', row['板块名称'])
            stock_board_industry_cons_em_df.insert(3, 'board_change_rate', row['涨跌幅'])
            stock_board_industry_cons_em_df.insert(4, 'board_total_market_cap', row['总市值'])
            stock_board_industry_cons_em_df = stock_board_industry_cons_em_df.sort_values(by='流通市值', ascending=False).head(15)
            total_stock_df = pd.concat([total_stock_df, stock_board_industry_cons_em_df], ignore_index=True)

        table_name = tbs.TABLE_STOCK_BOARD_INDUSTRY['name']
        # 删除老数据。
        if mdb.checkTableIsExist(table_name):
            del_sql = f"DELETE FROM `{table_name}` where `date` = '{now_time}'"
            mdb.executeSql(del_sql)
            cols_type = None
        else:
            cols_type = tbs.get_field_types(tbs.TABLE_STOCK_BOARD_INDUSTRY['columns'])
        df = board_industry_data.rename(columns=tbs.TABLE_STOCK_BOARD_INDUSTRY['header_mapping'])
        df.drop(columns=tbs.TABLE_STOCK_BOARD_INDUSTRY['drop_fields'], inplace=True)
        df.insert(0, 'date', now_time)
        mdb.insert_db_from_df(df, table_name, cols_type, False, "`date`,`board_code`")

        stock_cron_table_name = tbs.TABLE_STOCK_BOARD_INDUSTRY_CONS['name']
        if mdb.checkTableIsExist(stock_cron_table_name):
            del_sql = f"DELETE FROM `{stock_cron_table_name}` where `date` = '{now_time}'"
            mdb.executeSql(del_sql)
            cols_type = None
        else:
            cols_type = tbs.get_field_types(tbs.TABLE_STOCK_BOARD_INDUSTRY_CONS['columns'])
        total_stock_df = total_stock_df.rename(columns=tbs.TABLE_STOCK_BOARD_INDUSTRY_CONS['header_mapping'])
        total_stock_df.drop(columns=tbs.TABLE_STOCK_BOARD_INDUSTRY_CONS['drop_fields'], inplace=True)

        total_stock_df = total_stock_df[~total_stock_df['code'].str.startswith('900')]
        total_stock_df = total_stock_df[~total_stock_df['code'].str.startswith('200')]
        total_stock_df = total_stock_df[total_stock_df['change_rate'].notnull()]
        # code 需要去重
        total_stock_df = total_stock_df.drop_duplicates(subset=['code'])

        mdb.insert_db_from_df(total_stock_df, stock_cron_table_name, cols_type, False, "`date`,`board_code`,`code`", "date")
    except Exception as e:
        logging.error(f"basic_data_daily_job.save_stock_spot_data处理异常：{e}")


def main():
    runt.run_with_args(save_nph_stock_board_industry)


# main函数入口
if __name__ == '__main__':
    main()
