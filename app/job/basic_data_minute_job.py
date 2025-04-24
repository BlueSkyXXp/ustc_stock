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







# main函数入口
if __name__ == '__main__':
    main()
