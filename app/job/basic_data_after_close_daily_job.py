#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import logging
import os.path
import sys

cpath_current = os.path.dirname(os.path.dirname(__file__))
cpath = os.path.abspath(os.path.join(cpath_current, os.pardir))
sys.path.append(cpath)
import app.lib.run_template as runt
import app.lib.tablestructure as tbs
import app.lib.database as mdb
import akshare as ak
import pandas as pd

__author__ = 'bytedance'
__date__ = '2025/4/06 '


def save_after_close_stock_index_daily_hist(date):
    try:
        # 中证2000  932000    中证500 399905  上证50 000016
        # 沪深300 399300  中证1000  000852

        # 上证 000001    486510412986.40002
        # 深证 399001    651109936767.68994

        # 获取今天的时间 ，开始时间是今天， 结束时间也是今天

        index_zh_a_hist_df = ak.index_zh_a_hist(symbol="000001", period="daily", start_date=date, end_date=date)
        # index_zh_a_hist_df 添加两列， 在第二列和第三列分别添加 代码 名称
        index_zh_a_hist_df.insert(1, 'code', '000001')
        index_zh_a_hist_df.insert(2, 'name', '上证指数')

        sz_index_df = ak.index_zh_a_hist(symbol="399001", period="daily", start_date=date, end_date=date)
        # sz_index_df 添加两列， 在第二列和第三列分别添加 代码 名称
        sz_index_df.insert(1, 'code', '399001')
        sz_index_df.insert(2, 'name', '深证指数')

        bz_index_df = ak.index_zh_a_hist(symbol="899050", period="daily", start_date=date, end_date=date)
        # sz_index_df 添加两列， 在第二列和第三列分别添加 代码 名称
        bz_index_df.insert(1, 'code', '899050')
        bz_index_df.insert(2, 'name', '北证50')

        # 合并两个DataFrame
        index_zh_a_hist_df = pd.concat([index_zh_a_hist_df, sz_index_df, bz_index_df], ignore_index=True)

        hs_300_index_df = ak.index_zh_a_hist(symbol="399300", period="daily", start_date=date, end_date=date)
        # hs_300_index_df 添加两列， 在第二列和第三列分别添加 代码 名称
        hs_300_index_df.insert(1, 'code', '399300')
        hs_300_index_df.insert(2, 'name', '沪深300')
        # 合并两个DataFrame
        index_zh_a_hist_df = pd.concat([index_zh_a_hist_df, hs_300_index_df], ignore_index=True)

        sz_50_index_df = ak.index_zh_a_hist(symbol="000016", period="daily", start_date=date, end_date=date)
        # sz_50_index_df 添加两列， 在第二列和第三列分别添加 代码 名称
        sz_50_index_df.insert(1, 'code', '000016')
        sz_50_index_df.insert(2, 'name', '上证50')
        # 合并两个DataFrame
        index_zh_a_hist_df = pd.concat([index_zh_a_hist_df, sz_50_index_df], ignore_index=True)

        zz_500_index_df = ak.index_zh_a_hist(symbol="932000", period="daily", start_date=date, end_date=date)
        # zz_500_index_df 添加两列， 在第二列和第三列分别添加 代码 名称
        zz_500_index_df.insert(1, 'code', '932000')
        zz_500_index_df.insert(2, 'name', '中证500')
        # 合并两个DataFrame
        index_zh_a_hist_df = pd.concat([index_zh_a_hist_df, zz_500_index_df], ignore_index=True)

        zz_1000_index_df = ak.index_zh_a_hist(symbol="000852", period="daily", start_date=date, end_date=date)
        # zz_1000_index_df 添加两列， 在第二列和第三列分别添加 代码 名称
        zz_1000_index_df.insert(1, 'code', '000852')
        zz_1000_index_df.insert(2, 'name', '中证1000')
        # 合并两个DataFrame
        index_zh_a_hist_df = pd.concat([index_zh_a_hist_df, zz_1000_index_df], ignore_index=True)

        zz_2000_index_df = ak.index_zh_a_hist(symbol="399905", period="daily", start_date=date, end_date=date)
        # zz_2000_index_df 添加两列， 在第二列和第三列分别添加 代码 名称
        zz_2000_index_df.insert(1, 'code', '399905')
        zz_2000_index_df.insert(2, 'name', '中证2000')
        # 合并两个DataFrame
        index_zh_a_hist_df = pd.concat([index_zh_a_hist_df, zz_2000_index_df], ignore_index=True)

        if index_zh_a_hist_df is None:
            return

        index_zh_a_hist_df = index_zh_a_hist_df.rename(columns=tbs.TABLE_STOCK_INDEX_DAILY_HIST['header_mapping'])

        table_name = tbs.TABLE_STOCK_INDEX_DAILY_HIST['name']
        # 删除老数据。
        if mdb.checkTableIsExist(table_name):
            del_sql = f"DELETE FROM `{table_name}` where `date` = '{date}'"
            mdb.executeSql(del_sql)
            cols_type = None
        else:
            cols_type = tbs.get_field_types(tbs.TABLE_STOCK_INDEX_DAILY_HIST['columns'])
        mdb.insert_db_from_df(index_zh_a_hist_df, table_name, cols_type, False, "`date`,`code`")
    except Exception as e:
        logging.error(f"basic_data_other_daily_job.save_stock_index_daily_hist处理异常：{e}")


def main():
    runt.run_with_args(save_after_close_stock_index_daily_hist)


# main函数入口
if __name__ == '__main__':
    main()
