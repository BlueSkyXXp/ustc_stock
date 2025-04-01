from datetime import datetime

import akshare as ak
import pandas as pd
import app.core.stock as stock


# 定义大分类列表
big_categories = [
    "银行", "电子", "非银金融", "医药生物", "食品饮料", "化工", "电气设备",
    "采掘", "公用事业", "机械设备", "交通运输", "国防军工", "汽车",
    "有色金属", "建筑装饰", "传媒", "农林牧渔", "轻工制造", "房地产",
    "通信", "商业贸易"
]

# 定义细分分类与大分类的映射字典
category_mapping = {
    "航空机场": "交通运输",
    "铁路公路": "交通运输",
    "物流行业": "交通运输",
    "航运港口": "交通运输",
    "交运设备": "机械设备",
    "水泥建材": "建筑装饰",
    "工程建设": "建筑装饰",
    "装修建材": "建筑装饰",
    "装修装饰": "建筑装饰",
    "工程咨询服务": "建筑装饰",
    "公用事业": "公用事业",
    "电力行业": "公用事业",
    "农牧饲渔": "农林牧渔",
    "纺织服装": "轻工制造",
    "家用轻工": "轻工制造",
    "造纸印刷": "轻工制造",
    "包装材料": "轻工制造",
    "食品饮料": "食品饮料",
    "酿酒行业": "食品饮料",
    "煤炭行业": "采掘",
    "石油行业": "采掘",
    "采掘行业": "采掘",
    "证券": "非银金融",
    "保险": "非银金融",
    "多元金融": "非银金融",
    "银行": "银行",
    "汽车零部件": "汽车",
    "汽车服务": "汽车",
    "汽车整车": "汽车",
    "航天航空": "国防军工",
    "商业百货": "商业贸易",
    "贸易行业": "商业贸易",
    "旅游酒店": "商业贸易",
    "文化传媒": "传媒",
    "化学制药": "医药生物",
    "美容护理": "医药生物",
    "电子元件": "电子",
    "半导体": "电子",
    "消费电子": "电子",
    "光学光电子": "电子",
    "通信设备": "通信",
    "通信服务": "通信",
    "互联网服务": "传媒",
    "计算机设备": "电子",
    "软件开发": "传媒",
    "化肥行业": "化工",
    "化学制品": "化工",
    "化纤行业": "化工",
    "化学原料": "化工",
    "燃气": "公用事业",
    "电池": "电气设备",
    "电机": "电气设备",
    "光伏设备": "电气设备",
    "风电设备": "电气设备",
    "电源设备": "电气设备",
    "工程机械": "机械设备",
    "通用设备": "机械设备",
    "专用设备": "机械设备",
    "仪器仪表": "机械设备",
    "玻璃玻纤": "建筑装饰",
    "环保行业": "公用事业",
    "船舶制造": "国防军工",
    "农药兽药": "化工",
    "贵金属": "有色金属",
    "能源金属": "有色金属",
    "小金属": "有色金属",
    "钢铁行业": "有色金属",
    "珠宝首饰": "轻工制造",
    "橡胶制品": "化工",
    "塑料制品": "化工",
    "家电行业": "轻工制造",
    "电网设备": "电气设备",
    "教育": "传媒",
    "医疗服务": "医药生物",
    "非金属材料": "建筑装饰"
}


if __name__ == "__main__":
    stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
    print(stock_zh_a_spot_em_df.columns.tolist())


    macro_china_urban_unemployment_df = ak.macro_china_urban_unemployment()
    print(macro_china_urban_unemployment_df)
    stock_zt_pool_dtgc_em_df = ak.stock_zt_pool_zbgc_em(date='20250403')

    bb = stock_zt_pool_dtgc_em_df.columns.tolist()
    print(bb)

    print(stock_zt_pool_dtgc_em_df)

    data = {
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'city': ['New York', 'London', 'Paris']
    }
    df = pd.DataFrame(data)

    # 将DataFrame转换为记录列表的JSON格式
    json_data = df.to_json(orient='records')
    print(json_data)

    stock_individual_info_em_df = ak.stock_individual_info_em(symbol="600000")
    print(stock_individual_info_em_df)
    stock_zt_pool_em_df = ak.stock_zt_pool_em(date='20250401')
    print(stock_zt_pool_em_df)

    # 获取stock_zt_pool_em_df 中连板数最高一行数据

    max_zt_num = stock_zt_pool_em_df['连板数'].max()
    max_zt_num_row = stock_zt_pool_em_df[stock_zt_pool_em_df['连板数'] == max_zt_num]
    print(max_zt_num_row)

    l = stock_zt_pool_em_df.columns.tolist()



    df = ak.tool_trade_date_hist_sina()





