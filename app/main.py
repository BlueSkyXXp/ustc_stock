from fastapi import FastAPI  # 导入 FastAPI 框架
import uvicorn  # 导入 uvicorn 用于运行 ASGI 应用
import asyncio  # 异步编程库
from app.nacos_client import register_service, send_heartbeat, watch_config  # 从 app.nacos_client 模块导入注册服务、发送心跳和监听配置的函数
from app.api.routes import router  # 从 app.routes 模块导入路由
import app.settings as settings  # 导入 app.settings 模块，并重命名为 settings

# 创建 FastAPI 应用
app = FastAPI()

# 注册路由
app.include_router(router)


# 当应用启动时执行的事件
@app.on_event("startup")
async def startup_event():
    register_service()  # 调用注册服务函数

    watch_config()  # 调用监听配置函数

    # 启动心跳任务
    asyncio.create_task(send_heartbeat())  # 创建异步任务发送心跳


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.SERVICE_PORT)  # 运行应用，监听指定端口
