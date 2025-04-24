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
from sqlalchemy import String
import pandas as pd

__author__ = 'bytedance'
__date__ = '2025/3/31 '


def save_after_close_stock_board_concept_spot(date):
    """
    保存后复权的股票、板块、概念、指数的实时行情
    """

    try:

        stock_board_concept_name_em_df = ak.stock_board_concept_name_em()
        stock_board_concept_name_em_df = stock_board_concept_name_em_df.rename(columns=tbs.TABLE_STOCK_BOARD_CONCEPT_SPOT['header_mapping'])
        # total_stock_df = total_stock_df[total_stock_df['change_rate'].notnull()]
        stock_board_concept_name_em_df = stock_board_concept_name_em_df[stock_board_concept_name_em_df['board_code'].notnull()]
        # stock_board_concept_name_em_df.insert(0, 'date', date)
        stock_board_concept_name_em_df.drop(columns=tbs.TABLE_STOCK_BOARD_CONCEPT_SPOT['drop_fields'], inplace=True)
        total_stock_df = pd.DataFrame()



        for index, row in stock_board_concept_name_em_df.iterrows():
            code = row['board_code']
            name = row['board_name']

            stock_df = stock.get_stock_board_concept_cons_em(code)
            stock_df['board_concept_code'] = code
            stock_df['board_concept_name'] = name
            stock_df['combine_code'] = stock_df['代码'] + '-' + code
            
            total_stock_df = pd.concat([total_stock_df, stock_df], ignore_index=True)
  

        table_name = tbs.TABLE_STOCK_BOARD_CONCEPT_SPOT['name']

        if mdb.checkTableIsExist(table_name):
            del_sql = f"DELETE FROM `{table_name}`"
            mdb.executeSql(del_sql)
            cols_type = None
        else:
            cols_type = tbs.get_field_types(tbs.TABLE_STOCK_BOARD_CONCEPT_SPOT['columns'])
    
        mdb.insert_db_from_df(stock_board_concept_name_em_df, table_name, cols_type, False, "`board_code`")

        table_name = tbs.TABLE_STOCK_BOARD_CONCEPT_SPOT_CONS['name']
        total_stock_df = total_stock_df.rename(columns=tbs.TABLE_STOCK_BOARD_CONCEPT_SPOT_CONS['header_mapping'])
        # 去重
        total_stock_df = total_stock_df.drop_duplicates(subset=['combine_code'], keep='first')
        if mdb.checkTableIsExist(table_name):
            del_sql = f"DELETE FROM `{table_name}`"
            mdb.executeSql(del_sql)
            cols_type = None
        else:
            cols_type = tbs.get_field_types(tbs.TABLE_STOCK_BOARD_CONCEPT_SPOT_CONS['columns'])
        mdb.insert_db_from_df(total_stock_df, table_name, cols_type, False, "combine_code")

    except Exception as e:
        logging.error(f"save_after_close_stock_board_concept_spot error: {e}")


def main():
    runt.run_with_args(save_after_close_stock_board_concept_spot)


# main函数入口
if __name__ == '__main__':
    main()
