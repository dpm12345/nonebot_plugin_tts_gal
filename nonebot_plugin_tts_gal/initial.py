
import os
from nonebot.log import logger

async def checkDir(*args):
    for path in args:
        if not os.path.exists(path):
            logger.info(f"{path}目录不存在，正在创建...")
            try:
                os.mkdir(path)
                logger.info(f"{path}目录创建成功")
            except:
                logger.info(f"{path}目录创建失败")

async def checkFile(model_path,config_path,filenames):
    for filename in filenames:
        model_file = filename + ".pth"
        config_file = filename + ".json"
        if not os.path.exists(model_path / model_file):
            logger.info(f"模型文件{model_file}缺失")
        if not os.path.exists(config_path / config_file):
            logger.info(f"配置文件{config_file}缺失")

