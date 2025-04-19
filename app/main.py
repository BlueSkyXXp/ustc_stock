import importlib
from fastapi import FastAPI  # 导入 FastAPI 框架
import uvicorn  # 导入 uvicorn 用于运行 ASGI 应用
import asyncio  # 异步编程库
from app.nacos_client import register_service, send_heartbeat, watch_config  # 从 app.nacos_client 模块导入注册服务、发送心跳和监听配置的函数
from app.api.routes import router  # 从 app.routes 模块导入路由
import app.settings as settings  # 从 app.settings 模块导入配置
from apscheduler.schedulers.background import BackgroundScheduler
from app.util.log import loggings

# 创建 FastAPI 应用
app = FastAPI()

# 注册路由
app.include_router(router)


def run_job(action: str):
    loggings.info(f"Starting to execute job with action: {action}")
    try:
        if '.' not in action:
            loggings.error(f"Invalid action format: {action}. Action should be in the format 'module_name.function_name'")
            raise ValueError("Action should be in the format 'module_name.function_name'")
        module_name, function_name = action.split('.', 1)
        loggings.debug(f"Extracted module name: {module_name}, function name: {function_name}")
        module = importlib.import_module(f'app.job.{module_name}')
        loggings.debug(f"Successfully imported module: app.job.{module_name}")
        function = getattr(module, function_name)
        loggings.debug(f"Successfully retrieved function: {function_name} from module {module_name}")
        function()
        loggings.info(f"Job with action {action} executed successfully")
    except ImportError as e:
        loggings.error(f"Failed to import module app.job.{module_name}: {e}")
    except AttributeError as e:
        loggings.error(f"Function {function_name} not found in module {module_name}: {e}")
    except Exception as e:
        loggings.error(f"An unexpected error occurred while executing job {action}: {e}")
        


# 当应用启动时执行的事件
@app.on_event("startup")
async def startup_event():
    register_service()  # 调用注册服务函数

    watch_config()  # 调用监听配置函数

    # 启动心跳任务
    asyncio.create_task(send_heartbeat())  # 创建异步任务发送心跳

    # 启动定时任务
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_job, 'cron', minute='0,30', hour='9,10,11,13,14,15', day_of_week='mon-fri', args=[settings.Settings.SCHEDULE_HOUR_JOB])
    scheduler.add_job(run_job, 'cron', hour='16', day_of_week='mon-fri', args=[settings.Settings.SCHEDULE_NIGHT_JOB])
    scheduler.add_job(run_job, 'cron', hour='16', day_of_week='mon-fri', args=[settings.Settings.SCHEDULE_AFTER_CLOSE_FOUR_JOB])
    scheduler.add_job(run_job, 'cron', minute='0,30', hour='9,10,11,13,14,15', day_of_week='mon-fri', args=[settings.Settings.SCHEDULE_MINUTE_JOB])

    # scheduler.add_job(run_job, 'cron', minute='0, 2', hour='3', args=[settings.Settings.SCHEDULE_TEST_JOB])

    scheduler.start()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.Settings.SERVICE_PORT)  # 运行应用，监听指定端口
