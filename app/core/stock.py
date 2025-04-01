from io import StringIO

import pandas as pd
import requests

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

