
import httpx
import time
import hashlib
import random
import json
import uuid
from ffmpy import FFmpeg
import os
from .text import text_to_sequence
from .commons import intersperse
from torch import no_grad, LongTensor
from .utils import *
from nonebot.log import logger


def check_character(name, tts_gal):
    index = None
    config_file = ""
    model_file = ""
    for names, model in tts_gal.items():
        if name in names:
            config_file = model[0] + ".json"
            model_file = model[0] + ".pth"
            index = None if len(model) == 1 else int(model[1])
            break
    return config_file, model_file, index


def load_language(hps_ms):
    try:
        return hps_ms.language
    except:
        logger.info("配置文件中缺少language项,请手动添加(新版本内容),具体填写内容请查看github主页\
            https://github.com/dpm12345/nonebot_plugin_tts_gal/")
        logger.info("将默认使用日语配置项")
        return "ja"


def load_symbols(hps_ms, lang, symbols_dict):
    try:
        symbols = hps_ms.symbols
    except:
        logger.info("配置文件中缺失symbols项,建议手动添加")
        if lang in symbols_dict.keys():
            logger.info("采用language指定的symbols项")
            symbols = symbols_dict[lang]
        else:
            logger.info("该语言未有默认symbols项，将采用日语symbols")
            symbols = symbols_dict["ja"]
    return symbols


def get_text(text, hps, symbols, lang, cleaned=False):
    if cleaned:
        text_norm = text_to_sequence(text, symbols, [], lang)
    else:
        text_norm = text_to_sequence(
            text, symbols, hps.data.text_cleaners, lang)
    if hps.data.add_blank:
        text_norm = intersperse(text_norm, 0)
    text_norm = LongTensor(text_norm)
    return text_norm


def changeC2E(s: str):
    return s.replace("。", ".").replace("？", "?").replace("！", "!").replace("，", ",")


def changeE2C(s: str):
    return s.replace(".", "。").replace("?", "？").replace("!", "！").replace(",", "，")


async def translate_youdao(text: str, lang: str) -> str:
    url = f"https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "Cookie": "OUTFOX_SEARCH_USER_ID=467129664@10.169.0.102; JSESSIONID=aaaejjt9lMzrAgeDsHrWx;OUTFOX_SEARCH_USER_ID_NCOO=1850118475.9388125; ___rl__test__cookies=1632381536261",
        "Referer": "https://fanyi.youdao.com/"
    }
    ts = str(int(time.time() * 1000))
    salt = ts + str(random.randint(0, 9))
    temp = "fanyideskweb" + text + salt + "Ygy_4c=r#e#4EX^NUGUc5"
    md5 = hashlib.md5()
    md5.update(temp.encode())
    sign = md5.hexdigest()
    data = {
        "i": text,
        "from": "Auto",
        "to": lang,
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": salt,
        "sign": sign,
        "lts": ts,
        "bv": "5f70acd84d315e3a3e7e05f2a4744dfa",
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_REALTlME",
    }
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, data=data, headers=headers)
            result = json.loads(resp.content)
        res = ""
        for s in result['translateResult'][0]:
            res += s['tgt']
        return res
    except:
        return ""


def change_by_decibel(audio_path: str, output_dir: str, decibel):
    ext = os.path.basename(audio_path).strip().split('.')[-1]
    if ext not in ['wav', 'mp3']:
        raise Exception('format error')
    new_name = uuid.uuid4()
    ff = FFmpeg(inputs={'{}'.format(audio_path): None},
                outputs={os.path.join(output_dir, '{}.{}'.format(new_name, ext)): '-filter:a "volume={}dB" -loglevel quiet'.format(decibel)})
    ff.run()
    os.remove(audio_path)
    return os.path.join(output_dir, '{}.{}'.format(new_name, ext))
