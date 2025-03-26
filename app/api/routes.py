from fastapi import APIRouter, HTTPException
import os

from pydantic import BaseModel
from app.core.stock_analyzer import StockAnalyzer

# 定义请求体模型
# 创建一个请求体模型，用于接收文件路径


# class FilePathModel(BaseModel):
#     filePath: str


# 创建路由
# 创建一个API路由对象
router = APIRouter()

analyzer = StockAnalyzer()


# # 定义一个异步函数，用于处理POST请求，接收文件路径并识别图片中的文本信息
# @router.post("/ocr/")
# async def print_file_path(file_path_model: FilePathModel):
#     filePath = file_path_model.filePath
#     if not os.path.exists(filePath):
#         raise HTTPException(status_code=400, detail="File path does not exist")
#     print(f"Received file path: {filePath}")
#     text = recognize_image_text(filePath)
#     return {"message": text}


@router.get('/api/analyze_stock/{stock_code}')
def analyze(stock_code: str):
    if not stock_code:
        raise HTTPException(status_code=400, detail="Stock code is required")
    print(f"Received stock code: {stock_code}")
    return analyzer.analyze_stock(stock_code)


# @router.post('/api/batch_analyze_stock')
# def batch_analyze(stock_list: []):
#     if not stock_list:
#         raise HTTPException(status_code=400, detail="Stock list is required")
#     print(f"Received stock list: {stock_list}")
#     return analyzer.scan_market(stock_list)
