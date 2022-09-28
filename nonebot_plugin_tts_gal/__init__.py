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
        "example": "@机器人 宁宁说おはようございます.",
        "author": "dpm12345 <1006975692@qq.com>",
        "version": "0.2.2",
    },
)

data_path  = Path() / "data"
base_path = Path() / "data" / "nonebot_plugin_tts_gal"
voice_path = base_path / "voice"
model_path = base_path / "model"
config_path = base_path / "config"


auto_delete_voice = get_driver().config.auto_delete_voice
tts_gal = eval(get_driver().config.tts_gal)
driver = get_driver()


@driver.on_startup
def _():
    logger.info("正在检查目录是否存在...")
    asyncio.ensure_future(checkDir(data_path,base_path,voice_path))
    filenames = []
    [filenames.append(model[0]) for model in tts_gal.values() if not model[0] in filenames]
    logger.info("正在检查配置文件是否存在...")
    asyncio.ensure_future(checkFile(model_path,config_path,filenames))

    


voice = on_message(regex(r"(?P<name>\S+)(?:说|发送|说话)(?P<text>.*?)$"),block=False,priority=3)


@voice.handle()
async def voicHandler(
    bot: Bot, event: MessageEvent, 
    name: str = RegexArg("name"),
    text: str = RegexArg("text")
):
    index = None
    config_file = ""
    model_file = ""
    for names,model in tts_gal.items():
        if name in names:
            config_file = model[0] + ".json"
            model_file = model[0] + ".pth"
            index = None if len(model) == 1 else int(model[1])
            break
    if config_file == "":
        await voice.finish(MessageSegment.at(event.get_user_id()) + "暂时还未有该角色")
    text = changeC2E(text)
    text = await translate_youdao(text)
    text = get_romaji_with_space_and_accent(text)
    first_name = "".join(random.sample([x for x in string.ascii_letters + string.digits] , 8))
    filename = hashlib.md5(first_name.encode()).hexdigest() + ".mp3"
    try:
        hps_ms = get_hparams_from_file( config_path / config_file)
        net_g_ms = SynthesizerTrn(
            len(hps_ms.symbols),
            hps_ms.data.filter_length // 2 + 1,
            hps_ms.train.segment_size // hps_ms.data.hop_length,
            n_speakers=hps_ms.data.n_speakers,
            **hps_ms.model)
        _ = net_g_ms.eval()
        load_checkpoint(model_path / model_file, net_g_ms)
    except:
        await voice.finish("加载模型失败")
    text = get_text(text, hps_ms, cleaned=True)
    try:
        with no_grad():
            x_tst = text.unsqueeze(0)
            x_tst_lengths = LongTensor([text.size(0)])
            sid = LongTensor([index]) if not index == None else None
            audio = net_g_ms.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()
        write(voice_path / filename, hps_ms.data.sampling_rate, audio)
        new_voice = Path(change_by_decibel(voice_path / filename,voice_path,-10))
    except:
        traceback.print_exc()
        await voice.finish('生成失败')
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
