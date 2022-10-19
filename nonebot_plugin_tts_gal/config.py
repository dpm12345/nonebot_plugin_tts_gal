from typing import Optional
from pathlib import Path
from pydantic import Extra, BaseModel

data_path = Path() / "data"
base_path = Path() / "data" / "nonebot_plugin_tts_gal"
voice_path = base_path / "voice"
model_path = base_path / "model"
config_path = base_path / "config"


class Config(BaseModel, extra=Extra.ignore):
    auto_delete_voice: Optional[bool] = None
    tts_gal: Optional[str] = None