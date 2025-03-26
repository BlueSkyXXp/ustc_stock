import json
import logging

import nacos
import asyncio
import yaml
import app.settings as settings

# 初始化 Nacos 客户端
# 使用settings中的NACOS_SERVER_ADDRESS, NACOS_NAMESPACE, NACOS_USERNAME, NACOS_PASSWORD来初始化Nacos客户端
# client = nacos.NacosClient(settings.NACOS_SERVER_ADDRESS, namespace=settings.NACOS_NAMESPACE,
#                            username=settings.NACOS_USERNAME, password=settings.NACOS_PASSWORD)

client = nacos.NacosClient(settings.Settings.NACOS_SERVER_ADDRESS, namespace=settings.settings.NACOS_NAMESPACE)


def register_service():
    # 向Nacos注册服务实例
    client.add_naming_instance(
        settings.settings.SERVICE_NAME, settings.settings.SERVICE_IP, settings.settings.SERVICE_PORT,
        group_name=settings.settings.NACOS_GROUP_NAME)


async def send_heartbeat():
    # 异步发送心跳，每10秒发送一次心跳
    while True:
        try:
            client.send_heartbeat(settings.settings.SERVICE_NAME,
                                  settings.settings.SERVICE_IP, settings.settings.SERVICE_PORT)
        except Exception as e:
            print(f"Failed to send heartbeat: {e}")
        await asyncio.sleep(10)  # 每10秒发送一次心跳


def load_config(content):
    # 加载配置文件，解析yaml格式，设置语言
    # 解析json格式的配置文件
    json_config = json.loads(content)
    logging.info("json_config: %s", json_config)

    if json_config is None:
        return
    settings.settings.DB_HOST_NAME = json_config.get('DB_HOST_NAME', 'localhost')

    settings.settings.DB_PORT = json_config.get('DB_PORT', 3306)
    settings.settings.DB_USERNAME = json_config.get('DB_USERNAME', 'root')
    settings.settings.DB_PASSWORD = json_config.get('DB_PASSWORD', '123456')
    settings.settings.DB_DATABASE = json_config.get('DB_DATABASE', 'stock')
    logging.info("DB_HOST_NAME: %s", settings.settings.DB_HOST_NAME)
    logging.info("DB_PORT: %s", settings.settings.DB_PORT)
    logging.info("DB_USERNAME: %s", settings.settings.DB_USERNAME)
    logging.info("DB_PASSWORD: %s", settings.settings.DB_PASSWORD)
    logging.info("DB_DATABASE: %s", settings.settings.DB_DATABASE)
    # 解析yaml格式的配置文件
    # yaml_config = yaml.full_load(content)
    # print("yaml_config:", yaml_config)


def nacos_config_callback(args):
    # Nacos配置回调函数，处理配置更新
    content = args['raw_content']
    load_config(content)


def watch_config():
    # 启动时，强制同步一次配置
    config = client.get_config(settings.settings.NACOS_DATA_ID,
                               settings.settings.NACOS_GROUP_NAME)
    print("config:", config)
    load_config(config)
    # 启动监听器，监控配置变化
    client.add_config_watcher(settings.settings.NACOS_DATA_ID,
                              settings.settings.NACOS_GROUP_NAME, nacos_config_callback)
