# settings.py

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


# 服务端口
SERVICE_PORT = 8001
SERVICE_IP = get_local_ip()
# 服务名
SERVICE_NAME = "stock-service"

# Nacos 配置
NACOS_SERVER_ADDRESS = "10.37.43.33:8848"
NACOS_NAMESPACE = "public"
NACOS_DATA_ID = "stock-service"
NACOS_USERNAME = "nacos"
NACOS_PASSWORD = "nacos"
NACOS_GROUP_NAME = "DEFAULT_GROUP"
