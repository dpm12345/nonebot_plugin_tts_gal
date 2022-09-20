from pathlib import Path
from nonebot import on_message, get_driver
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11.message import  MessageSegment
from nonebot.adapters.onebot.v11 import Bot, MessageEvent

from nonebot.log import logger

import hashlib
import random
import string
from nonebot.exception import ActionFailed, NetworkError
from .depends import *
from .japanese_g2p import *
from .initial import *
from torch import no_grad, LongTensor
from .utils import *
from .models import SynthesizerTrn
from .function import *

from scipy.io.wavfile import write
import asyncio
import traceback


__plugin_meta__ = PluginMetadata(
    name="gal角色语音",
    description="部分gal角色文本转语音",
    usage="触发方式：@机器人 [角色名][发送|说][文本内容]",
    extra={
        "unique_name": "petpet",
        "example": "@机器人 宁宁说おはようございます.",
        "author": "zhong <1006975692@qq.com>",
        "version": "0.1.0",
    },
)

data_path  = Path() / "data"
base_path = Path() / "data" / "nonebot_plugin_tts_gal"
voice_path = base_path / "voice"
model_path = base_path / "model"
config_path = base_path / "config"
speak = [
    ["宁宁","绫地宁宁"],
    ["因幡爱瑠","爱瑠"],
    ["朝武芳乃","芳乃"],
    ["常陸茉子","茉子"],
    ["丛雨","幼刀"],
    ["鞍馬小春","鞍马小春","小春"],
    ["在原七海","七海"],
    ["ATRI","atri","亚托莉"]
]

config_files = [
    "YuzuSoft.json",
    "ATRI.json"
]

models = ["YuzuSoft_365_epochs.pth","ATRI_vits_900E_G_38000.pth"]


auto_delete_voice = get_driver().config.auto_delete_voice
driver = get_driver()


@driver.on_startup
def _():
    logger.info("正在检查目录是否存在...")
    asyncio.ensure_future(checkDir(data_path,base_path,voice_path))

    


voice = on_message(regex(r"(?P<name>\S+)(?:说|发送|说话)(?P<text>.*?)$"),block=False,priority=3)


@voice.handle()
async def voicHandler(
    bot: Bot, event: MessageEvent, 
    name: str = RegexArg("name"),
    text: str = RegexArg("text")
):
    text = await translate(text)
    text = get_romaji_with_space_and_accent(text)
    first_name = "".join(random.sample([x for x in string.ascii_letters + string.digits] , 8))
    filename = hashlib.md5(first_name.encode()).hexdigest() + ".mp3"
    index = 0
    for i in range(len(speak)):
        if name in speak[i]:
            index = i
            break
    config_file = ""
    model_file = ""
    if index <= 6:
        model_file = model_path / models[0]
        config_file = config_path / config_files[0]
    elif index == 7:
        model_file = model_path / models[1]
        config_file = config_path / config_files[1]

    try:
        hps_ms = get_hparams_from_file(config_file)
        net_g_ms = SynthesizerTrn(
            len(hps_ms.symbols),
            hps_ms.data.filter_length // 2 + 1,
            hps_ms.train.segment_size // hps_ms.data.hop_length,
            n_speakers=hps_ms.data.n_speakers,
            **hps_ms.model)
        _ = net_g_ms.eval()
        load_checkpoint(model_file, net_g_ms)
    except:
        await voice.send("加载模型失败")
    text = get_text(text, hps_ms, cleaned=True)
    try:
        if index <= 6:
            with no_grad():
                x_tst = text.unsqueeze(0)
                x_tst_lengths = LongTensor([text.size(0)])
                sid = LongTensor([index])
                audio = net_g_ms.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()
        elif index == 7:
            with no_grad():
                x_tst = text.unsqueeze(0)
                x_tst_lengths = LongTensor([text.size(0)])
                audio = net_g_ms.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()
        write(voice_path / filename, hps_ms.data.sampling_rate, audio)
        new_voice = Path(change_by_decibel(voice_path / filename,voice_path,-10))
        try:
            await voice.send(MessageSegment.record(file=new_voice))
        except ActionFailed:
            traceback.print_exc()
            await voice.send("发送失败,请重试")
        except NetworkError:
            await voice.send("发送超时,也许等等就好了")
        finally:
            if auto_delete_voice:
                os.remove(new_voice)
    except:
        traceback.print_exc()
        await voice.send('生成失败')
