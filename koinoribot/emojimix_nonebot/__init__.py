import io
import os
import re
import emoji

from hoshino import Service
from ..build_image import BuildImage

from .data_source import mix_emoji

sv = Service('合成emoji')

emojis = filter(lambda e: len(e) == 1, emoji.EMOJI_DATA.keys())
pattern = "(" + "|".join(re.escape(e) for e in emojis) + ")"


@sv.on_rex(rf"^\s*({pattern})\s*\+\s*({pattern})\s*$")
async def mix_emoji_func(bot, ev):
    match = ev.match
    emoji_1 = match.group(1)
    emoji_2 = match.group(3)
    await bot.send(ev, '冰祈咏唱中...')
    result = await mix_emoji(emoji_1, emoji_2)
    if isinstance(result, str):
        await bot.send(ev, result)
    else:
        icon = io.BytesIO(result)
        bg = BuildImage(0, 0, background=icon, is_alpha=True)
        await bot.send(ev, f"[CQ:image,file=base64://{bg.pic2bs4()}]")
