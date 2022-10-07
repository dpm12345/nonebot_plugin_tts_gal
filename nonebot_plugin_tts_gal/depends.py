
import re

from nonebot.rule import Rule
from nonebot.typing import T_State
from nonebot.params import Depends
from nonebot.adapters.onebot.v11 import (
    Bot,
    Message,
    MessageSegment,
    MessageEvent,
    GroupMessageEvent,
)


REGEX_DICT = "REGEX_DICT"
REGEX_ARG = "REGEX_ARG"


def regex(pattern: str) -> Rule:
    def checker(event: MessageEvent, state: T_State) -> bool:
        if isinstance(event,GroupMessageEvent) and not event.is_tome():
            return False
        msg = event.get_message()
        msg_seg: MessageSegment = msg[0]
        if not msg_seg.is_text():
            return False

        seg_text = str(msg_seg).lstrip()
        matched = re.match(rf"(?:{pattern})", seg_text, re.IGNORECASE)
        if not matched:
            return False

        new_msg = msg.copy()
        seg_text = seg_text[matched.end() :].lstrip()
        if seg_text:
            new_msg[0].data["text"] = seg_text
        else:
            new_msg.pop(0)
        state[REGEX_DICT] = matched.groupdict()
        state[REGEX_ARG] = new_msg
        return True

    return Rule(checker)


def RegexArg(key: str):
    async def dependency(state: T_State):
        arg: dict = state[REGEX_DICT]
        return arg.get(key, None)

    return Depends(dependency)