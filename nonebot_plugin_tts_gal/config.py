from pathlib import Path
from pydantic import Extra, BaseModel
from nonebot import get_driver
from typing import List

data_path = Path() / "data"
base_path = Path() / "data" / "nonebot_plugin_tts_gal"
voice_path = base_path / "voice"
model_path = base_path / "model"
config_path = base_path / "config"


class Config(BaseModel, extra=Extra.ignore):
    tts_gal: str = '{():[""]}'
    auto_delete_voice: bool = True
    decibel: int = -10
    tts_gal_is_at: bool = True
    tts_gal_prefix: str = ""
    tts_gal_priority: int = 3
    tts_gal_tran_type: List[str] = ["youdao"]
    baidu_tran_appid: str = ""
    baidu_tran_apikey: str = ""
    tencent_tran_region: str = "ap-shanghai"
    tencent_tran_secretid: str = ""
    tencent_tran_secretkey: str = ""
    tencent_tran_projectid: int = 0


tts_gal_config = Config.parse_obj(get_driver().config)
trigger_rule = ""
if tts_gal_config.tts_gal_is_at:
    trigger_rule += "@机器人 "
trigger_rule+= tts_gal_config.tts_gal_prefix
