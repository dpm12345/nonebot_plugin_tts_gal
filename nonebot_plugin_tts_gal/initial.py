
import os
from nonebot.log import logger
from .function import support_tran

async def checkDir(*args):
    for path in args:
        if not os.path.exists(path):
            logger.info(f"{path}目录不存在，正在创建...")
            try:
                os.mkdir(path)
                logger.info(f"{path}目录创建成功")
            except:
                logger.info(f"{path}目录创建失败")

async def checkFile(model_path,config_path,filenames,tts_gal,plugin_meta,valid_names):
    exist_file = []
    for filename in filenames:
        flag = True
        model_file = filename + ".pth"
        config_file = filename + ".json"
        if not os.path.exists(model_path / model_file):
            logger.info(f"模型文件{model_file}缺失")
            flag = False
        if not os.path.exists(config_path / config_file):
            logger.info(f"配置文件{config_file}缺失")
            flag = False
        if flag:
            exist_file.append(filename)
    
    '''添加目前检测出来的可以使用的角色语音'''
    valid_character_names_list = [name for name,model in tts_gal.items() if model[0] in exist_file]
    valid_names += valid_character_names_list
    valid_character_names = []
    for name in valid_character_names_list:
        if isinstance(name,str):
            valid_character_names.append(name)
        else:
            valid_character_names.append("/".join(name))
    if len(valid_character_names):
        plugin_meta.usage = plugin_meta.usage + "\n目前可使用的语音角色：\n" + "\n".join(valid_character_names)
    else:
        plugin_meta.usage = plugin_meta.usage + "\n目前无可使用的语音角色\n"


async def checkEnv(plugin_config,tran_type):
    if plugin_config.auto_delete_voice == None:
        logger.info("未配置auto_delete_voice项,将默认为true")
    if not plugin_config.tts_gal:
        logger.info("未配置tts_gal项,请根据模型及项目主页Usage.md指南进行配置")

    for i in range(len(tran_type)-1,-1,-1):
        if tran_type[i] not in support_tran.keys():
            logger.info(f"未支持{tran_type[i]}翻译,请及时修改")
            del tran_type[i]
        if tran_type[i] in tran_type[:i]:
            del tran_type[i]
    if "youdao" not in tran_type:
        tran_type.append("youdao")
    logger.info(f"可使用翻译有{','.join(tran_type)}")
    plugin_config.tts_gal_tran_type = tran_type.copy()


