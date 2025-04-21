import importlib
from app.util.log import loggings
import re
from datetime import datetime
import akshare as ak
import pandas as pd

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core import stock
from app.core.stock_analyzer import StockAnalyzer
from app.api.model.request_model import TimeRange
from app.lib.trade_time import is_tradetime
from app.lib.database import engine
import app.lib.tablestructure as tbs
import app.lib.run_template as runt
import app.lib.trade_time as trd
import app.core.stock as StockService
import json

# 创建路由
# 创建一个API路由对象
router = APIRouter()

analyzer = StockAnalyzer()

# 复用时间校验函数
def validate_time_range(time_range: TimeRange, date_format=r'^\d{4}-\d{2}-\d{2}$'):
    if not time_range.StartTime or not time_range.EndTime:
        raise HTTPException(status_code=400, detail="时间范围不能为空")
    if not re.match(date_format, time_range.StartTime) or not re.match(date_format, time_range.EndTime):
        raise HTTPException(status_code=400, detail=f"时间范围格式不正确，应为{date_format.replace('^', '').replace('$', '')}")
    end_time = datetime.strptime(time_range.EndTime, '%Y-%m-%d')
    if end_time.date() > datetime.now().date():
        raise HTTPException(status_code=400, detail="结束时间不能晚于今天")
    return end_time



@router.get('/api/analyze_stock/{stock_code}')
def analyze(stock_code: str):
    if not stock_code:
        raise HTTPException(status_code=400, detail="Stock code is required")
    loggings.info(f"Received stock code: {stock_code}")
    return analyzer.analyze_stock(stock_code)

@router.get('/api/consecutive_limit_up')
def get_consecutive_limit_up(start_time: str, end_time: str):
    loggings.info(f"action: get_consecutive_limit_up, Received start_time: {start_time}, end_time: {end_time}")
    # 临时创建 TimeRange 实例
    time_range = TimeRange(StartTime=start_time, EndTime=end_time)
    end_time = validate_time_range(time_range)


    query = f"""
                SELECT si.* 
                FROM `{tbs.TABLE_STOCK_ZT_POOL['name']}` si
                JOIN (
                    SELECT date, MAX(consecutive_board_count) AS max_boards 
                    FROM `{tbs.TABLE_STOCK_ZT_POOL['name']}` 
                    GROUP BY date
                ) sub
                ON si.date = sub.date AND si.consecutive_board_count = sub.max_boards
                WHERE si.date >= %s AND si.date <= %s
                """
    # 使用参数化查询
    stock_df = pd.read_sql(query, engine(), params=(time_range.StartTime, time_range.EndTime))

    return {
        "StockConsecutiveLimitUp": stock_df.to_dict(orient='records')
    }

@router.post('/api/get_stock_import_index_info')
def get_stock_import_index_info(time_range: TimeRange):
    validate_time_range(time_range)

    query = f"""
                    SELECT * 
                    FROM `{tbs.TABLE_STOCK_INDEX_DAILY_HIST['name']}` 
                    WHERE date >= %s AND date <= %s
                    """
    # 使用参数化查询
    stock_df = pd.read_sql(query, engine(), params=(time_range.StartTime, time_range.EndTime))

    stock_df = stock_df.groupby('date').apply(lambda x: x.to_dict(orient='records')).reset_index(name='data')
    stock_df = stock_df.to_dict(orient='records')
    return {
        "StockImportIndexInfo": stock_df
    }

@router.get('/api/get_stock_board_industry_data')
def get_stock_board_industry_data(time: str):
    # 校验时间范围和格式
    loggings.info(f"Received time: {time}, action: get_stock_board_industry_data")
    if not time:
        raise HTTPException(status_code=400, detail="时间不能为空")

    full_time = None
    # 尝试匹配 2025-04-21 10:30 格式
    match_full = re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$', time)
    if match_full:
        full_time = f"{time}:00"
    else:
        # 尝试匹配 14:30 格式
        match_partial = re.match(r'^\d{2}:\d{2}$', time)
        if match_partial:
            _, trade_time = trd.get_trade_date_last()
            full_time = f"{trade_time} {time}:00"
        else:
            raise HTTPException(status_code=400, detail="时间格式不正确，应为 YYYY-MM-DD HH:MM 或 HH:MM")

    query = f"""
        SELECT 
            sbic.board_code, 
            sbic.board_name, 
            sbic.board_change_rate, 
            sbic.board_total_market_cap, 
            sbic.code,
            sbic.name, 
            sbic.latest_price, 
            sbic.change_rate, 
            sbic.circulating_market_cap
        FROM {tbs.TABLE_STOCK_BOARD_INDUSTRY_CONS['name']} sbic 
        WHERE sbic.date = %s
    """

    # 使用参数化查询
    stock_df = pd.read_sql(query, engine(), params=(full_time,))

    result = {"StockBoardIndustryData": []}
    grouped = stock_df.groupby('board_code')

    for board_code, group in grouped:
        board_info = {
            "board_code": board_code,
            "board_name": group['board_name'].iloc[0],
            "change_rate": group['board_change_rate'].iloc[0],
            "total_market_cap": group['board_total_market_cap'].iloc[0],
            "stocks": []
        }

        for _, row in group.iterrows():
            stock_info = {
                "board_code": board_code,
                "board_name": group['board_name'].iloc[0],
                "code": row['code'],
                "name": row['name'],
                "latest_price": row['latest_price'],
                "change_rate": row['change_rate'],
                "circulating_market_cap": row['circulating_market_cap']
            }
            board_info["stocks"].append(stock_info)

        result["StockBoardIndustryData"].append(board_info)

    return result




@router.get('/api/market_activity_trend_data')
def get_market_activity_trend_data():
    result = StockService.get_daily_stock_market_activity()
    if result is None:
        raise HTTPException(status_code=500, detail="获取市场活动趋势数据失败")
    return result

@router.get('/api/execute_job')
def execute_job(action: str):
    if not action:
        raise HTTPException(status_code=400, detail="Action is required")
    try:
        # 假设 action 格式为 module_name.function_name
        if '.' not in action:
            raise ValueError("Action should be in the format 'module_name.function_name'")
        module_name, function_name = action.split('.', 1)
        # 动态导入模块
        module = importlib.import_module(f'app.job.{module_name}')
        # 获取函数
        function = getattr(module, function_name)

        runt.run_with_args(function)
        # 调用函数
        result = function()
        return {"result": result}
    except ImportError as e:
        loggings.error(f"Module {module_name} not found in app.job: {e}")
        raise HTTPException(status_code=500, detail=f"Module {module_name} not found in app.job")
    except AttributeError as e:
        loggings.error(f"Function {function_name} not found in module {module_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Function {function_name} not found in module {module_name}")
    except Exception as e:
        loggings.error(f"Job execution failed: {e}")
        raise HTTPException(status_code=500, detail=f"Job execution failed: {str(e)}")

@router.get('/api/get_stock_market_crowd_data')
def get_stock_market_crowd_data(start_time: str, end_time: str):
    # 验证时间格式
    date_format = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(date_format, start_time) or not re.match(date_format, end_time):
        raise HTTPException(status_code=400, detail=f"时间格式不正确，应为{date_format.replace('^', '').replace('$', '')}")
    end_date = datetime.strptime(end_time, '%Y-%m-%d')
    if end_date.date() > datetime.now().date():
        raise HTTPException(status_code=400, detail="结束时间不能晚于今天")

    # 构建查询语句
    query = f"""
        SELECT * 
        FROM `{tbs.TABLE_STOCK_ZB_POOL['name']}` 
        WHERE date >= %s AND date <= %s
    """
    # 使用参数化查询
    try:
        stock_df = pd.read_sql(query, engine(), params=(start_time, end_time))
        result = stock_df.to_dict(orient='records')
        return {
            "StockMarketCrowdData": result
        }
    except Exception as e:
        loggings.error(f"查询股票市场拥挤度数据失败: {e}")
        raise HTTPException(status_code=500, detail="查询股票市场拥挤度数据失败")


@router.get('/api/get_limit_up_stocks')
def get_limit_up_stocks(time: str):
    # 校验时间范围和格式，格式为 YYYY-MM-DD
    loggings.info(f"Received time: {time}, action: get_limit_up_stocks")
    if not time:
        raise HTTPException(status_code=400, detail="时间不能为空")
    date_format = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(date_format, time):
        raise HTTPException(status_code=400, detail=f"时间格式不正确，应为{date_format.replace('^', '').replace('$', '')}")
    
    # 假设表名为 TABLE_STOCK_LIMIT_UP，你需要根据实际情况修改
    query = f"""
        SELECT * 
        FROM `{tbs.TABLE_STOCK_LIMIT_UP['name']}` 
        WHERE date = %s
    """
    try:
        # 使用参数化查询
        stock_df = pd.read_sql(query, engine(), params=(time,))
        result = stock_df.to_dict(orient='records')
        return {
            "LimitUpStocks": result
        }
    except Exception as e:
        loggings.error(f"查询涨停股票数据失败: {e}")
        raise HTTPException(status_code=500, detail="查询涨停股票数据失败")


