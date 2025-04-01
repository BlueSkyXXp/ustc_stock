import pandas as pd
from sqlalchemy import create_engine


engine = create_engine('mysql+mysqlconnector://root:password:@localhost:3306/stock')


def get_consecutive_limit_up(start_time, end_time):
    sql = f"SELECT * FROM stock_zt_pool WHERE date >= '{start_time}' AND date <= '{end_time}'"
    df = pd.read_sql(sql, engine)
    return df.to_dict(orient='records')