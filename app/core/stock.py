import math
from io import StringIO

import aiohttp
import pandas as pd
import requests
import asyncio

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36",
    "Content-Type": "application/json"
}


def get_stock_market_activity():
    url = "https://legulegu.com/stockdata/market-activity"
    r = requests.get(url, headers=headers)
    bb = pd.read_html(StringIO(r.text))[1]
    temp_df = pd.read_html(StringIO(r.text))[0]


def get_daily_stock_market_activity():
    url = "https://legulegu.com/stockdata/market-activity-trend-data"
    try:
        resp = requests.get(url, headers=headers)
        # 检查响应状态码
        resp.raise_for_status()
        # 将响应内容转换为 JSON 格式
        data = resp.json()
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 错误发生: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"请求发生错误: {req_err}")
    except ValueError as json_err:
        print(f"JSON 解析错误: {json_err}")
    return None



async def _async_get_top_5_stock():
    url = 'https://push2.eastmoney.com/api/qt/clist/get'
    params = {
        'np': '1',
        'fltt': '1',
        'invt': '2',
        'fs': 'm:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048',
        'fields': 'f12,f13,f14,f1,f2,f4,f3,f152,f5,f6,f7,f15,f18,f16,f17,f10,f8,f9,f23',
        'fid': 'f6',
        'pn': '1',
        'pz': '100',
        'po': '1',
        'dect': '1',
        'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
        'wbp2u': '|0|0|0|web',
        '_': '1745046448296'
    }
    result = await fetch_5_percent_top_async(url, params)
    return process_data(result)

async def fetch_5_percent_top_async(url: str, base_params: dict[str, str]) -> list[dict[str, str]]:
    first_page_params = base_params.copy()
    first_page_params["pn"] = "1"
    async with aiohttp.ClientSession() as session:
        first_page_data = await fetch_single_page(session, url, first_page_params)
        if first_page_data.get("rc") != 0 or not first_page_data.get("data"):
            return [first_page_data]


        total_count = first_page_data["data"]["total"]
        single_page_size = int(first_page_params["pz"]) # 每页大小

            # 计算前5%的股票数量取整数
        top_5_percent_count = int(total_count * 0.05)
        # 计算需要的页数
        total_pages = top_5_percent_count//single_page_size
        remaining_stocks = top_5_percent_count % single_page_size

        task = []
        for i in range(2, total_pages+1):
            params = base_params.copy()
            params["pn"] = i
            task.append(fetch_single_page(session, url, params))


        results = await asyncio.gather(*task)
        results.insert(0, first_page_data)
        if remaining_stocks > 0:
            params = base_params.copy()
            params["pn"] = total_pages + 1
            params["pz"] = remaining_stocks
            results.append(await fetch_single_page(session, url, params))

        return results

            

def get_top_5_stock():
    import nest_asyncio

    nest_asyncio.apply()
    return asyncio.run(_async_get_top_5_stock())

async def fetch_single_page(
    session: aiohttp.ClientSession, url: str, params: dict[str, str]
) -> dict[str, str]:
    """异步获取单页数据"""
    async with session.get(url, params=params, ssl=False) as response:
        return await response.json()

def process_data(page_results: list[dict[str,str]]) -> pd.DataFrame:
    """处理获取到的数据，转换为DataFrame"""
    all_data = []

    # 保存每个页面的结果和页码
    page_number = 1
    items_per_page = 100  # 假设每页100条

    for result in page_results:
        if result.get("rc") == 0 and result.get("data") and result["data"].get("diff"):
            page_data = result["data"]["diff"]

            # 添加页面信息以便后续计算序号
            for item in page_data:
                item["page_number"] = page_number
                item["page_index"] = page_data.index(item)

            all_data.extend(page_data)
            page_number += 1

    if not all_data:
        return pd.DataFrame()

    df = pd.DataFrame(all_data)

    # 计算正确的序号
    df["序号"] = df.apply(
        lambda row: (row["page_number"] - 1) * items_per_page + row["page_index"] + 1,
        axis=1,
    )

    # 删除临时列
    df.drop(columns=["page_number", "page_index"], inplace=True, errors="ignore")

    # 设置列名 - 修正了5分钟涨跌的映射 (f11 是正确的5分钟涨跌字段)
    column_map = {
        "f1": "原序号",
        "f2": "最新价",
        "f3": "涨跌幅",
        "f4": "涨跌额",
        "f5": "成交量",
        "f6": "成交额",
        "f7": "振幅",
        "f8": "换手率",
        "f9": "市盈率-动态",
        "f10": "量比",
        "f11": "5分钟涨跌",
        "f12": "代码",
        "f13": "_",
        "f14": "名称",
        "f15": "最高",
        "f16": "最低",
        "f17": "今开",
        "f18": "昨收",
        "f20": "总市值",
        "f21": "流通市值",
        "f22": "涨速",
        "f23": "市净率",
        "f24": "60日涨跌幅",
        "f25": "年初至今涨跌幅",
        "f62": "-",
        "f115": "-",
        "f128": "-",
        "f136": "-",
        "f152": "-",
    }

    df.rename(columns=column_map, inplace=True)

    # 选择需要的列并确保所有需要的列都存在
    desired_columns = [
        "序号",
        "代码",
        "名称",
        "最新价",
        "涨跌幅",
        "涨跌额",
        "成交量",
        "成交额",
        "振幅",
        "最高",
        "最低",
        "今开",
        "昨收",
        "量比",
        "换手率",
        "市盈率-动态",
        "市净率",
        "总市值",
        "流通市值",
        "涨速",
        "5分钟涨跌",
        "60日涨跌幅",
        "年初至今涨跌幅",
    ]

    # 过滤出存在的列
    available_columns = [col for col in desired_columns if col in df.columns]
    df = df[available_columns]

    # 转换数值类型
    numeric_columns = [
        "最新价",
        "涨跌幅",
        "涨跌额",
        "成交量",
        "成交额",
        "振幅",
        "最高",
        "最低",
        "今开",
        "昨收",
        "量比",
        "换手率",
        "市盈率-动态",
        "市净率",
        "总市值",
        "流通市值",
        "涨速",
        "5分钟涨跌",
        "60日涨跌幅",
        "年初至今涨跌幅",
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 按涨跌幅降序排序
    df.sort_values(by="涨跌幅", ascending=False, inplace=True)

    # 重新生成序号
    df.reset_index(drop=True, inplace=True)
    df["序号"] = df.index + 1

    return df

def get_stock_board_industry_cons(symbol: str = "BK1027"):
    url = "https://29.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "100",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "fs": f"b:{symbol} f:!50",
        "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,"
                  "f23,f24,f25,f22,f11,f62,f128,f136,f115,f152,f45",
    }
    new_params = params.copy()
    # 获取第一页数据，用于确定分页信息
    r = requests.get(url, params=new_params, timeout=15)
    data_json = r.json()
    # 计算分页信息
    per_page_num = len(data_json["data"]["diff"])
    total_page = math.ceil(data_json["data"]["total"] / per_page_num)
    # 存储所有页面数据
    temp_list = []
    # 添加第一页数据
    temp_list.append(pd.DataFrame(data_json["data"]["diff"]))
    # 获取剩余页面数据
    for page in range(2, total_page + 1):
        new_params.update({"pn": page})
        r = requests.get(url, params=params, timeout=15)
        data_json = r.json()
        inner_temp_df = pd.DataFrame(data_json["data"]["diff"])
        temp_list.append(inner_temp_df)
    # 合并所有数据
    temp_df = pd.concat(temp_list, ignore_index=True)
    temp_df["f3"] = pd.to_numeric(temp_df["f3"], errors="coerce")
    temp_df.sort_values(by=["f3"], ascending=False, inplace=True, ignore_index=True)
    temp_df.reset_index(inplace=True)
    temp_df["index"] = temp_df["index"].astype(int) + 1

    temp_df.columns = [
        "序号",
        "_",
        "最新价",
        "涨跌幅",
        "涨跌额",
        "成交量",
        "成交额",
        "振幅",
        "换手率",
        "市盈率-动态",
        "量比",
        "_",
        "代码",
        "_",
        "名称",
        "最高",
        "最低",
        "今开",
        "昨收",
        "总市值",
        "流通市值",
        "_",
        "市净率",
        "_",
        "今年涨幅",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
    ]
    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "最新价",
            "涨跌幅",
            "涨跌额",
            "成交量",
            "成交额",
            "振幅",
            "最高",
            "最低",
            "今开",
            "昨收",
            "换手率",
            "市盈率-动态",
            "市净率",
            "量比",
            "总市值",
            "流通市值"
        ]
    ]

    temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
    temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
    temp_df["振幅"] = pd.to_numeric(temp_df["振幅"], errors="coerce")
    temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
    temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
    temp_df["今开"] = pd.to_numeric(temp_df["今开"], errors="coerce")
    temp_df["昨收"] = pd.to_numeric(temp_df["昨收"], errors="coerce")
    temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
    temp_df["市盈率-动态"] = pd.to_numeric(temp_df["市盈率-动态"], errors="coerce")
    temp_df["市净率"] = pd.to_numeric(temp_df["市净率"], errors="coerce")
    temp_df["量比"] = pd.to_numeric(temp_df["量比"], errors="coerce")
    temp_df["总市值"] = pd.to_numeric(temp_df["总市值"], errors="coerce")
    temp_df["流通市值"] = pd.to_numeric(temp_df["流通市值"], errors="coerce")

    return temp_df


def get_stock_board_concept_cons_em(symbol: str="BK1145"):
    url = "https://29.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "100",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "fs": f"b:{symbol} f:!50",
        "fields": "f12,f14",
    }

    new_params = params.copy()
    # 获取第一页数据，用于确定分页信息
    r = requests.get(url, params=new_params, timeout=15)
    data_json = r.json()
    # 计算分页信息
    per_page_num = len(data_json["data"]["diff"])
    total_page = math.ceil(data_json["data"]["total"] / per_page_num)
    # 存储所有页面数据
    temp_list = []
    # 添加第一页数据
    temp_list.append(pd.DataFrame(data_json["data"]["diff"]))
    # 获取剩余页面数据
    for page in range(2, total_page + 1):
        new_params.update({"pn": page})  # 更新页码
        r = requests.get(url, params=params, timeout=15)
        data_json = r.json()
        inner_temp_df = pd.DataFrame(data_json["data"]["diff"])
        temp_list.append(inner_temp_df)
    # 合并所有数据
    temp_df = pd.concat(temp_list, ignore_index=True)

    temp_df.columns = [
        "代码",
        "名称",
    ]

    return temp_df


if __name__ == '__main__':
    data = get_top_5_stock()
    print(data)