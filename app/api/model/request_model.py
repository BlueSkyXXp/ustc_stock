from pydantic import BaseModel


# 定义请求体模型
class TimeRange(BaseModel):
    StartTime: str
    EndTime: str
