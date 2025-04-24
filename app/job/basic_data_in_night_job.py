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
import pandas as pd

__author__ = 'bytedance'
__date__ = '2025/3/31 '


def save_after_close_stock_board_concept_spot(date):
    """
    保存后复权的股票、板块、概念、指数的实时行情
    """

    stock_board_concept_name_em_df = ak.stock_board_concept_name_em()

    total_stock_df = pd.DataFrame()

    for index, row in stock_board_concept_name_em_df.iterrows():
        code = row['代码']
        name = row['名称']

        stock_df = stock.get_stock_board_concept_cons_em(code)
        stock_df['board_concept_code'] = code
        stock_df['board_concept_name'] = name
        
        total_stock_df = pd.concat([total_stock_df, stock_df], ignore_index=True)

    table_name = tbs.TABLE_STOCK_BOARD_CONCEPT_SPOT['name']
    # 删除老数据。
    if mdb.checkTableIsExist(table_name):
        del_sql = f"DELETE FROM `{table_name}` where `date` = '{datetime.datetime.now().strftime('%Y-%m-%d')}'"
        mdb.delete_table_data(table_name, del_sql)

    # 写入数据
    mdb.insert_db_from_df(stock_board_concept_name_em_df, table_name, tbs.TABLE_STOCK_BOARD_CONCEPT_SPOT['cols_type'], True, ['date', 'code'])

    # total_stock_df 写入数据库 ，如果存在则更新， 否则插入。 这个表是新表。
    table_name = tbs.TABLE_STOCK_BOARD_CONCEPT_SPOT_CONS['name']

    mdb.update_db_from_df(total_stock_df, table_name, ('date', 'code'))





    


def main():
    runt.run_with_args(save_after_close_stock_board_concept_spot)


# main函数入口
if __name__ == '__main__':
    main()
