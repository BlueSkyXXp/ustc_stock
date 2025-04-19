# settings.py
import os
import socket


def get_local_ip():
    """
    获取当前计算机的IP地址
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


class Settings:
    """
    配置类
    """
    # 优先从环境变量获取值，获取不到则用默认值
    SERVICE_PORT = int(os.getenv("SERVICE_PORT", 8001))
    SERVICE_IP = os.getenv("SERVICE_IP", get_local_ip())
    SERVICE_NAME = os.getenv("SERVICE_NAME", "stock-service")
    NACOS_SERVER_ADDRESS = os.getenv("NACOS_SERVER_ADDRESS", "172.25.0.4:8848")
    NACOS_NAMESPACE = os.getenv("NACOS_NAMESPACE", "public")
    NACOS_DATA_ID = os.getenv("NACOS_DATA_ID", "stock-service")
    NACOS_USERNAME = os.getenv("NACOS_USERNAME", "nacos")
    NACOS_PASSWORD = os.getenv("NACOS_PASSWORD", "nacos")
    NACOS_GROUP_NAME = os.getenv("NACOS_GROUP_NAME", "DEFAULT_GROUP")
    DB_HOST_NAME = os.getenv("DB_HOST_NAME", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_USERNAME = os.getenv("DB_USERNAME", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "qwer1234!")
    DB_NAME = os.getenv("DB_NAME", "stock")

    # 定时任务
    SCHEDULE_HOUR_JOB = os.getenv("SCHEDULE_HOUR_JOB", "basic_data_daily_job.main")
    SCHEDULE_NIGHT_JOB = os.getenv("SCHEDULE_NIGHT_JOB", "basic_data_in_night_job.main")
    SCHEDULE_MINUTE_JOB = os.getenv("SCHEDULE_MINUTE_JOB", "basic_data_minute_job.main")
    SCHEDULE_AFTER_CLOSE_FOUR_JOB = os.getenv("SCHEDULE_AFTER_CLOSE_FOUR_JOB", "basic_data_after_close_four_job.main")
    SCHEDULE_TEST_JOB = os.getenv("SCHEDULE_TEST_JOB", "test.main")


settings = Settings()
