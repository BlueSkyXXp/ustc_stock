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
    SERVICE_PORT = 8001
    SERVICE_IP = get_local_ip()
    SERVICE_NAME = "stock-service"
    NACOS_SERVER_ADDRESS = "10.37.43.33:8848"
    NACOS_NAMESPACE = "public"
    NACOS_DATA_ID = "stock-service"
    NACOS_USERNAME = "nacos"
    NACOS_PASSWORD = "nacos"
    NACOS_GROUP_NAME = "DEFAULT_GROUP"
    DB_HOST_NAME = "localhost"
    DB_PORT = 3306
    DB_USERNAME = "root"
    DB_PASSWORD = "123456"
    DB_NAME = "stock"

    def __init__(self):
        """
        初始化配置
        """
        self.SERVICE_PORT = 8001
        self.SERVICE_IP = get_local_ip()
        self.SERVICE_NAME = "stock-service"
        self.NACOS_SERVER_ADDRESS = "10.37.43.33:8848"
        self.NACOS_NAMESPACE = "public"
        self.NACOS_DATA_ID = "stock-service"
        self.NACOS_USERNAME = "nacos"
        self.NACOS_PASSWORD = "nacos"
        self.NACOS_GROUP_NAME = "DEFAULT_GROUP"

    def first_update_from_os_env(self):
        self.NACOS_SERVER_ADDRESS = os.getenv("NACOS_SERVER_ADDRESS", "10.37.43.33:8848")
        self.SERVICE_PORT = int(os.getenv("SERVICE_PORT", 8001))


settings = Settings()
