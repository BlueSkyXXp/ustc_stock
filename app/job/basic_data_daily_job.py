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
import app.lib.tablestructure as tbs
import app.lib.database as mdb

__author__ = 'bytedance'
__date__ = '2025/3/31 '


def save_nph_stock_zt_pool_data(date, before=True):
    if before:
        return
    # 涨停池股票列表
    try:
        data = ak.stock_zt_pool_em(date.strftime("%Y%m%d"))
        if data is None:
            return
        table_name = tbs.TABLE_STOCK_ZT_POOL['name']
        # 删除老数据。
        if mdb.checkTableIsExist(table_name):
            del_sql = f"DELETE FROM `{table_name}` where `date` = '{date}'"
            mdb.executeSql(del_sql)
            cols_type = None
        else:
            cols_type = tbs.get_field_types(tbs.TABLE_STOCK_ZT_POOL['columns'])
        df = data.rename(columns=tbs.TABLE_STOCK_ZT_POOL['header_mapping'])
        df.drop(columns=tbs.TABLE_STOCK_ZT_POOL['drop_fields'], inplace=True)
        df.insert(0, 'date', date)
        mdb.insert_db_from_df(df, table_name, cols_type, False, "`date`,`code`")
    except Exception as e:
        logging.error(f"basic_data_daily_job.save_stock_spot_data处理异常：{e}")


def save_nph_stock_dt_pool_data(date, before=True):
    if before:
        return
    # 涨停池股票列表
    try:
        data = ak.stock_zt_pool_dtgc_em(date.strftime("%Y%m%d"))
        if data is None:
            return
        table_name = tbs.TABLE_STOCK_DT_POOL['name']
        # 删除老数据。
        if mdb.checkTableIsExist(table_name):
            del_sql = f"DELETE FROM `{table_name}` where `date` = '{date}'"
            mdb.executeSql(del_sql)
            cols_type = None
        else:
            cols_type = tbs.get_field_types(tbs.TABLE_STOCK_DT_POOL['columns'])
        df = data.rename(columns=tbs.TABLE_STOCK_DT_POOL['header_mapping'])
        df.drop(columns=tbs.TABLE_STOCK_DT_POOL['drop_fields'], inplace=True)
        df.insert(0, 'date', date)
        mdb.insert_db_from_df(df, table_name, cols_type, False, "`date`,`code`")
    except Exception as e:
        logging.error(f"basic_data_daily_job.save_stock_spot_data处理异常：{e}")


def save_nph_stock_zb_pool_data(date, before=True):
    if before:
        return
    # 涨停池股票列表
    try:
        data = ak.stock_zt_pool_zbgc_em(date.strftime("%Y%m%d"))
        if data is None:
            return
        table_name = tbs.TABLE_STOCK_ZB_POOL['name']
        # 删除老数据。
        if mdb.checkTableIsExist(table_name):
            del_sql = f"DELETE FROM `{table_name}` where `date` = '{date}'"
            mdb.executeSql(del_sql)
            cols_type = None
        else:
            cols_type = tbs.get_field_types(tbs.TABLE_STOCK_ZB_POOL['columns'])
        df = data.rename(columns=tbs.TABLE_STOCK_ZB_POOL['header_mapping'])
        df.drop(columns=tbs.TABLE_STOCK_ZB_POOL['drop_fields'], inplace=True)
        df.insert(0, 'date', date)
        mdb.insert_db_from_df(df, table_name, cols_type, False, "`date`,`code`")
    except Exception as e:
        logging.error(f"basic_data_daily_job.save_stock_spot_data处理异常：{e}")


def main():
    runt.run_with_args(save_nph_stock_zt_pool_data)
    runt.run_with_args(save_nph_stock_dt_pool_data)
    runt.run_with_args(save_nph_stock_zb_pool_data)


# main函数入口
if __name__ == '__main__':
    main()
