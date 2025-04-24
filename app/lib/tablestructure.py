from sqlalchemy import DATE, VARCHAR, FLOAT, BIGINT, SmallInteger, DATETIME
from sqlalchemy.dialects.mysql import BIT

__author__ = 'bytedance '
__date__ = '2025/3/29 '

RATE_FIELDS_COUNT = 100  # N日收益率字段数目，即N值
_COLLATE = "utf8mb4_general_ci"

TABLE_STOCK_ZT_POOL = {
    'name': 'stock_zt_pool',
    'cn': '每日股票交易数据',
    'columns': {
        'date': {'type': DATE, 'cn': '日期', 'size': 0},
        'code': {'type': VARCHAR(8, _COLLATE), 'cn': '股票代码', 'size': 60},
        'name': {'type': VARCHAR(32, _COLLATE), 'cn': '股票名称', 'size': 120},
        'change_rate': {'type': FLOAT, 'cn': '涨跌幅（%）', 'size': 70},
        'latest_price': {'type': FLOAT, 'cn': '最新价', 'size': 70},
        'trading_volume': {'type': BIGINT, 'cn': '成交额', 'size': 100},
        'circulating_market_cap': {'type': FLOAT, 'cn': '流通市值', 'size': 120},
        'total_market_cap': {'type': FLOAT, 'cn': '总市值', 'size': 120},
        'turnover_rate': {'type': FLOAT, 'cn': '换手率（%）', 'size': 70},
        'sealing_fund': {'type': BIGINT, 'cn': '封板资金', 'size': 100},
        'first_sealing_time': {'type': VARCHAR(16, _COLLATE), 'cn': '首次封板时间', 'size': 80},
        'last_sealing_time': {'type': VARCHAR(16, _COLLATE), 'cn': '最后封板时间', 'size': 80},
        'breaking_board_count': {'type': BIGINT, 'cn': '炸板次数', 'size': 60},
        'limit_up_statistics': {'type': VARCHAR(8, _COLLATE), 'cn': '涨停统计', 'size': 120},
        'consecutive_board_count': {'type': BIGINT, 'cn': '连板数', 'size': 60},
        'industry': {'type': VARCHAR(32, _COLLATE), 'cn': '所属行业', 'size': 120}
    },
    'header_mapping': {
        '代码': 'code',
        '名称': 'name',
        '涨跌幅': 'change_rate',
        '最新价': 'latest_price',
        '最后封板时间': 'last_sealing_time',
        '炸板次数': 'breaking_board_count',
        '涨停统计': 'limit_up_statistics',
        '连板数': 'consecutive_board_count',
        '所属行业': 'industry',
        '成交额': 'trading_volume',
        '流通市值': 'circulating_market_cap',
        '总市值': 'total_market_cap',
        '换手率': 'turnover_rate',
        '封板资金': 'sealing_fund',
        '首次封板时间': 'first_sealing_time'
    },
    'drop_fields': [
        '序号',
    ],
}

TABLE_STOCK_DT_POOL = {
    'name': 'stock_dt_pool',
    'cn': '每日股票跌停池数据',
    'columns': {
        'date': {'type': DATE, 'cn': '日期', 'size': 0},
        'code': {'type': VARCHAR(8), 'cn': '代码', 'size': 60},
        'name': {'type': VARCHAR(32), 'cn': '名称', 'size': 120},
        'change_rate': {'type': FLOAT, 'cn': '涨跌幅', 'size': 70},
        'latest_price': {'type': FLOAT, 'cn': '最新价', 'size': 70},
        'trading_volume': {'type': BIGINT, 'cn': '成交额', 'size': 100},
        'circulating_market_cap': {'type': FLOAT, 'cn': '流通市值', 'size': 120},
        'total_market_cap': {'type': FLOAT, 'cn': '总市值', 'size': 120},
        'dynamic_pe_ratio': {'type': FLOAT, 'cn': '动态市盈率', 'size': 120},
        'turnover_rate': {'type': FLOAT, 'cn': '换手率', 'size': 70},
        'sealing_fund': {'type': BIGINT, 'cn': '封单资金', 'size': 100},
        'last_sealing_time': {'type': VARCHAR(16), 'cn': '最后封板时间', 'size': 80},
        'board_trading_volume': {'type': BIGINT, 'cn': '板上成交额', 'size': 100},
        'consecutive_limit_down': {'type': BIGINT, 'cn': '连续跌停', 'size': 60},
        'breaking_board_count': {'type': BIGINT, 'cn': '开板次数', 'size': 60},
        'industry': {'type': VARCHAR(32), 'cn': '所属行业', 'size': 120}
    },
    'header_mapping': {
        '代码': 'code',
        '名称': 'name',
        '涨跌幅': 'change_rate',
        '最新价': 'latest_price',
        '成交额': 'trading_volume',
        '流通市值': 'circulating_market_cap',
        '总市值': 'total_market_cap',
        '动态市盈率': 'dynamic_pe_ratio',
        '换手率': 'turnover_rate',
        '封单资金': 'sealing_fund',
        '最后封板时间': 'last_sealing_time',
        '板上成交额': 'board_trading_volume',
        '连续跌停': 'consecutive_limit_down',
        '开板次数': 'breaking_board_count',
        '所属行业': 'industry'
    },
    'drop_fields': [
        '序号',
    ]
}

TABLE_STOCK_ZB_POOL = {
    'name': 'stock_zb_pool',
    'cn': '每日股票涨停池数据',
    'columns': {
        'date': {'type': DATE, 'cn': '日期', 'size': 0},
        'code': {'type': VARCHAR(8), 'cn': '代码', 'size': 60},
        'name': {'type': VARCHAR(32), 'cn': '名称', 'size': 120},
        'change_rate': {'type': FLOAT, 'cn': '涨跌幅', 'size': 70},
        'latest_price': {'type': FLOAT, 'cn': '最新价', 'size': 70},
        'limit_up_price': {'type': FLOAT, 'cn': '涨停价', 'size': 70},
        'trading_volume': {'type': BIGINT, 'cn': '成交额', 'size': 100},
        'circulating_market_cap': {'type': FLOAT, 'cn': '流通市值', 'size': 120},
        'total_market_cap': {'type': FLOAT, 'cn': '总市值', 'size': 120},
        'turnover_rate': {'type': FLOAT, 'cn': '换手率', 'size': 70},
        'rise_speed': {'type': FLOAT, 'cn': '涨速', 'size': 70},
        'first_sealing_time': {'type': VARCHAR(16), 'cn': '首次封板时间', 'size': 80},
        'breaking_board_count': {'type': BIGINT, 'cn': '炸板次数', 'size': 60},
        'limit_up_statistics': {'type': VARCHAR(8), 'cn': '涨停统计', 'size': 120},
        'amplitude': {'type': FLOAT, 'cn': '振幅', 'size': 70},
        'industry': {'type': VARCHAR(32), 'cn': '所属行业', 'size': 120}
    },
    'header_mapping': {
        '代码': 'code',
        '名称': 'name',
        '涨跌幅': 'change_rate',
        '最新价': 'latest_price',
        '涨停价': 'limit_up_price',
        '成交额': 'trading_volume',
        '流通市值': 'circulating_market_cap',
        '总市值': 'total_market_cap',
        '换手率': 'turnover_rate',
        '涨速': 'rise_speed',
        '首次封板时间': 'first_sealing_time',
        '炸板次数': 'breaking_board_count',
        '涨停统计': 'limit_up_statistics',
        '振幅': 'amplitude',
        '所属行业': 'industry'
    },
    'drop_fields': [
        '序号',
    ]
}

TABLE_STOCK_SNS_SSEINFO = {
    'name': 'stock_sns_sseinfo',
    'cn': '股票问答数据',
    'columns': {
        'Code': {'type': 'VARCHAR(8)', 'cn': '股票代码', 'size': 60},
        'ShortName': {'type': 'VARCHAR(32)', 'cn': '公司简称', 'size': 120},
        'Question': {'type': 'TEXT', 'cn': '问题', 'size': 0},
        'Answer': {'type': 'TEXT', 'cn': '回答', 'size': 0},
        'QuestionTime': {'type': 'DATETIME', 'cn': '问题时间', 'size': 0},
        'AnswerTime': {'type': 'DATETIME', 'cn': '回答时间', 'size': 0},
        'QuestionSource': {'type': 'VARCHAR(32)', 'cn': '问题来源', 'size': 120},
        'AnswerSource': {'type': 'VARCHAR(32)', 'cn': '回答来源', 'size': 120},
        'UserName': {'type': 'VARCHAR(32)', 'cn': '用户名', 'size': 120}
    },
    'header_mapping': {
        '股票代码': 'Code',
        '公司简称': 'ShortName',
        '问题': 'Question',
        '回答': 'Answer',
        '问题时间': 'QuestionTime',
        '回答时间': 'AnswerTime',
        '问题来源': 'QuestionSource',
        '回答来源': 'AnswerSource',
        '用户名': 'UserName'
    },
    'drop_fields': []
}

TABLE_STOCK_INDEX_DAILY_HIST = {
    'name': 'stock_index_daily_hist',
    'cn': '股票指数每日历史数据',
    'columns': {
        'date': {'type': DATE, 'cn': '日期', 'size': 0},
        'code': {'type': VARCHAR(8, _COLLATE), 'cn': '指数代码', 'size': 60},
        'name': {'type': VARCHAR(32, _COLLATE), 'cn': '指数名称', 'size': 120},
        'open_price': {'type': FLOAT, 'cn': '开盘', 'size': 70},
        'close_price': {'type': FLOAT, 'cn': '收盘', 'size': 70},
        'high_price': {'type': FLOAT, 'cn': '最高', 'size': 70},
        'low_price': {'type': FLOAT, 'cn': '最低', 'size': 70},
        'volume': {'type': BIGINT, 'cn': '成交量', 'size': 100},
        'turnover': {'type': BIGINT, 'cn': '成交额', 'size': 100},
        'amplitude': {'type': FLOAT, 'cn': '振幅', 'size': 70},
        'change_rate': {'type': FLOAT, 'cn': '涨跌幅', 'size': 70},
        'change_amount': {'type': FLOAT, 'cn': '涨跌额', 'size': 70},
        'turnover_rate': {'type': FLOAT, 'cn': '换手率', 'size': 70}
    },
    'header_mapping': {
        '日期': 'date',
        '开盘': 'open_price',
        '收盘': 'close_price',
        '最高': 'high_price',
        '最低': 'low_price',
        '成交量': 'volume',
        '成交额': 'turnover',
        '振幅': 'amplitude',
        '涨跌幅': 'change_rate',
        '涨跌额': 'change_amount',
        '换手率': 'turnover_rate'
    },
    'drop_fields': []
}

TABLE_STOCK_BOARD_INDUSTRY = {
    'name': 'stock_board_industry',
    'cn': '股票板块行业数据',
    'columns': {
        'date': {'type': DATETIME, 'cn': '日期', 'size': 0},
        'rank': {'type': BIGINT, 'cn': '排名', 'size': 60},
        'board_name': {'type': VARCHAR(32, _COLLATE), 'cn': '板块名称', 'size': 120},
        'board_code': {'type': VARCHAR(8, _COLLATE), 'cn': '板块代码', 'size': 60},
        'latest_price': {'type': FLOAT, 'cn': '最新价', 'size': 70},
        'change_amount': {'type': FLOAT, 'cn': '涨跌额', 'size': 70},
        'change_rate': {'type': FLOAT, 'cn': '涨跌幅', 'size': 70},
        'total_market_cap': {'type': FLOAT, 'cn': '总市值', 'size': 120},
        'turnover_rate': {'type': FLOAT, 'cn': '换手率', 'size': 70},
        'rising_count': {'type': BIGINT, 'cn': '上涨家数', 'size': 60},
        'falling_count': {'type': BIGINT, 'cn': '下跌家数', 'size': 60},
        'leading_stock': {'type': VARCHAR(32, _COLLATE), 'cn': '领涨股票', 'size': 120},
        'leading_stock_change_rate': {'type': FLOAT, 'cn': '领涨股票-涨跌幅', 'size': 70}
    },
    'header_mapping': {
        '排名': 'rank',
        '板块名称': 'board_name',
        '板块代码': 'board_code',
        '最新价': 'latest_price',
        '涨跌额': 'change_amount',
        '涨跌幅': 'change_rate',
        '总市值': 'total_market_cap',
        '换手率': 'turnover_rate',
        '上涨家数': 'rising_count',
        '下跌家数': 'falling_count',
        '领涨股票': 'leading_stock',
        '领涨股票-涨跌幅': 'leading_stock_change_rate'
    },
    'drop_fields': []
}

TABLE_STOCK_BOARD_INDUSTRY_CONS = {
    'name': 'stock_board_industry_cons',
    'cn': '股票板块行业成分股数据',
    'columns': {
        'date': {'type': DATETIME, 'cn': '日期', 'size': 0},
        'board_code': {'type': VARCHAR(8, _COLLATE), 'cn': '板块代码', 'size': 60},
        'board_name': {'type': VARCHAR(32, _COLLATE), 'cn': '板块名称', 'size': 120},
        'board_change_rate': {'type': FLOAT, 'cn': '板块涨跌幅', 'size': 70},
        'board_total_market_cap': {'type': FLOAT, 'cn': '板块总市值', 'size': 120},
        'code': {'type': VARCHAR(8, _COLLATE), 'cn': '代码', 'size': 60},
        'name': {'type': VARCHAR(32, _COLLATE), 'cn': '名称', 'size': 120},
        'latest_price': {'type': FLOAT, 'cn': '最新价', 'size': 70},
        'change_rate': {'type': FLOAT, 'cn': '涨跌幅', 'size': 70},
        'change_amount': {'type': FLOAT, 'cn': '涨跌额', 'size': 70},
        'trading_volume': {'type': BIGINT, 'cn': '成交量', 'size': 100},
        'trading_amount': {'type': BIGINT, 'cn': '成交额', 'size': 100},
        'amplitude': {'type': FLOAT, 'cn': '振幅', 'size': 70},
        'highest_price': {'type': FLOAT, 'cn': '最高', 'size': 70},
        'lowest_price': {'type': FLOAT, 'cn': '最低', 'size': 70},
        'opening_price': {'type': FLOAT, 'cn': '今开', 'size': 70},
        'previous_closing_price': {'type': FLOAT, 'cn': '昨收', 'size': 70},
        'turnover_rate': {'type': FLOAT, 'cn': '换手率', 'size': 70},
        'dynamic_pe_ratio': {'type': FLOAT, 'cn': '市盈率-动态', 'size': 120},
        'pb_ratio': {'type': FLOAT, 'cn': '市净率', 'size': 120},
        'volume_ratio': {'type': FLOAT, 'cn': '量比','size': 120},
        'total_market_cap': {'type': FLOAT, 'cn': '总市值','size': 120},
        'circulating_market_cap': {'type': FLOAT, 'cn': '流通市值','size': 120}
    },
    'header_mapping': {
        '代码': 'code',
        '名称': 'name',
        '最新价': 'latest_price',
        '涨跌幅': 'change_rate',
        '涨跌额': 'change_amount',
        '成交量': 'trading_volume',
        '成交额': 'trading_amount',
        '振幅': 'amplitude',
        '最高': 'highest_price',
        '最低': 'lowest_price',
        '今开': 'opening_price',
        '昨收': 'previous_closing_price',
        '换手率': 'turnover_rate',
        '市盈率-动态': 'dynamic_pe_ratio',
        '市净率': 'pb_ratio',
        '量比': 'volume_ratio',
        '总市值': 'total_market_cap',
        '流通市值': 'circulating_market_cap'
    },
    'drop_fields': [
        '序号',
    ]
}

TABLE_STOCK_ZH_A_SPOT = {
    'name': 'stock_zh_a_spot',
    'cn': 'A股实时行情数据',
    'columns': {
        'date': {'type': DATE, 'cn': '日期', 'size': 0},
        'code': {'type': VARCHAR(8, _COLLATE), 'cn': '代码', 'size': 60},
        'name': {'type': VARCHAR(32, _COLLATE), 'cn': '名称', 'size': 120},
        'latest_price': {'type': FLOAT, 'cn': '最新价', 'size': 70},
        'change_rate': {'type': FLOAT, 'cn': '涨跌幅', 'size': 70},
        'change_amount': {'type': FLOAT, 'cn': '涨跌额', 'size': 70},
        'trading_volume': {'type': BIGINT, 'cn': '成交量', 'size': 100},
        'trading_amount': {'type': BIGINT, 'cn': '成交额', 'size': 100},
        'amplitude': {'type': FLOAT, 'cn': '振幅', 'size': 70},
        'highest_price': {'type': FLOAT, 'cn': '最高', 'size': 70},
        'lowest_price': {'type': FLOAT, 'cn': '最低', 'size': 70},
        'opening_price': {'type': FLOAT, 'cn': '今开', 'size': 70},
        'previous_closing_price': {'type': FLOAT, 'cn': '昨收', 'size': 70},
        'volume_ratio': {'type': FLOAT, 'cn': '量比', 'size': 70},
        'turnover_rate': {'type': FLOAT, 'cn': '换手率', 'size': 70},
        'dynamic_pe_ratio': {'type': FLOAT, 'cn': '市盈率-动态', 'size': 120},
        'pb_ratio': {'type': FLOAT, 'cn': '市净率', 'size': 120},
        'total_market_cap': {'type': FLOAT, 'cn': '总市值', 'size': 120},
        'circulating_market_cap': {'type': FLOAT, 'cn': '流通市值', 'size': 120},
        'rise_speed': {'type': FLOAT, 'cn': '涨速', 'size': 70},
        'five_minute_change': {'type': FLOAT, 'cn': '5分钟涨跌', 'size': 70},
        'sixty_day_change_rate': {'type': FLOAT, 'cn': '60日涨跌幅', 'size': 70},
        'ytd_change_rate': {'type': FLOAT, 'cn': '年初至今涨跌幅', 'size': 70}
    },
    'header_mapping': {
        '代码': 'code',
        '名称': 'name',
        '最新价': 'latest_price',
        '涨跌幅': 'change_rate',
        '涨跌额': 'change_amount',
        '成交量': 'trading_volume',
        '成交额': 'trading_amount',
        '振幅': 'amplitude',
        '最高': 'highest_price',
        '最低': 'lowest_price',
        '今开': 'opening_price',
        '昨收': 'previous_closing_price',
        '量比': 'volume_ratio',
        '换手率': 'turnover_rate',
        '市盈率-动态': 'dynamic_pe_ratio',
        '市净率': 'pb_ratio',
        '总市值': 'total_market_cap',
        '流通市值': 'circulating_market_cap',
        '涨速': 'rise_speed',
        '5分钟涨跌': 'five_minute_change',
        '60日涨跌幅': 'sixty_day_change_rate',
        '年初至今涨跌幅': 'ytd_change_rate'
    },
    'drop_fields': [
        '序号',
    ]
}

TABLE_MARKET_CROWDING = {
    'name': 'stock_market_crowding',
    'cn': '大盘拥挤度数据',
    'columns': {
        'date': {'type': DATE, 'cn': '日期', 'size': 0},
        'top_5_percent_total_volume': {'type': FLOAT, 'cn': '前5%的总成交额(亿元)', 'size': 120},
        'all_a_shares_total_volume': {'type': FLOAT, 'cn': '全A股总成交额(亿元)', 'size': 120},
        'crowding_ratio': {'type': FLOAT, 'cn': '拥挤度','size': 120}
    },
    'header_mapping': {
        '日期': 'date',
        '前5%的总成交额': 'top_5_percent_total_volume',
        '全A股总成交额': 'all_a_shares_total_volume'
    },
    'drop_fields': []
}

# ['排名', '板块名称', '板块代码', '最新价', '涨跌额', '涨跌幅', '总市值', '换手率', '上涨家数', '下跌家数', '领涨股票', '领涨股票-涨跌幅']
TABLE_STOCK_BOARD_CONCEPT_SPOT = {
    'name':'stock_board_concept_spot',
    'cn': '板块概念数据',
    'columns': {
        'date': {'type': DATE, 'cn': '日期','size': 0},
        'board_code': {'type': VARCHAR(8, _COLLATE), 'cn': '板块代码','size': 60},
        'board_name': {'type': VARCHAR(32, _COLLATE), 'cn': '板块名称','size': 120},
        'latest_price': {'type': FLOAT, 'cn': '最新价','size': 70},
        'change_amount': {'type': FLOAT, 'cn': '涨跌额','size': 70},
        'change_rate': {'type': FLOAT, 'cn': '涨跌幅','size': 70},
        'total_market_cap': {'type': FLOAT, 'cn': '总市值','size': 120},
        'turnover_rate': {'type': FLOAT, 'cn': '换手率','size': 70},
        'rise_stock': {'type': VARCHAR(32, _COLLATE), 'cn': '领涨股票','size': 120},
        'rise_stock_change_rate': {'type': FLOAT, 'cn': '领涨股票-涨跌幅','size': 70}
    },
    'header_mapping': {
        '板块名称': 'board_name',
        '板块代码': 'board_code',
        '最新价': 'latest_price',
        '涨跌额': 'change_amount',
        '涨跌幅': 'change_rate',
        '总市值': 'total_market_cap',
        '换手率': 'turnover_rate',  
        '领涨股票': 'rise_stock',
        '领涨股票-涨跌幅': 'rise_stock_change_rate'
    },
    'drop_fields': []
}



    # board_concept_code    board_concept_name
TABLE_STOCK_BOARD_CONCEPT_SPOT_CONS = {
    'name':'stock_board_concept_spot_cons',
    'cn': '板块概念数据',
    'columns': {
        'board_concept_code': {'type': VARCHAR(8, _COLLATE), 'cn': '板块代码','size': 60},
        'board_concept_name': {'type': VARCHAR(32, _COLLATE), 'cn': '板块名称','size': 120}
    },
    'header_mapping': {
        '板块名称': 'board_concept_name',
        '板块代码': 'board_concept_code'
    },
    'drop_fields': []
}



def get_field_cn(key, table):
    f = table.get('columns').get(key)
    if f is None:
        return key
    return f.get('cn')


def get_field_cns(cols):
    data = []
    for k in cols:
        if k == 'code':
            data.append({"value": k, "caption": cols[k]['cn'], "width": cols[k]['size'],
                         "headerStyle": {"font": "bold 9pt Calibri", "wordWrap": "true"}, "style": ""})
        elif k == 'change_rate':
            data.append({"value": k, "caption": cols[k]['cn'], "width": cols[k]['size'],
                         "headerStyle": {"font": "bold 9pt Calibri", "wordWrap": "true"}, "conditionalFormats": [
                    {"ruleType": "formulaRule", "formula": "@>0", "style": {"foreColor": "red"}},
                    {"ruleType": "formulaRule", "formula": "@<0", "style": {"foreColor": "green"}}]})
        else:
            data.append({"value": k, "caption": cols[k]['cn'], "width": cols[k]['size'],
                         "headerStyle": {"font": "bold 9pt Calibri", "wordWrap": "true"}})
        # data.append({"value": k, "caption": cols[k]['cn'], "width": cols[k]['size'], "headerStyle": {"font": "bold 9pt Calibri", "wordWrap": "true"}})
        # data.append({"name": k, "displayName": cols[k]['cn'], "size": cols[k]['size']})
    return data


def get_field_types(cols):
    data = {}
    for k in cols:
        data[k] = cols[k]['type']
    return data


def get_field_type_name(col_type):
    if col_type == DATE:
        return "datetime"
    elif col_type == FLOAT or col_type == BIGINT or col_type == SmallInteger or col_type == BIT:
        return "numeric"
    else:
        return "string"
