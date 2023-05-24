from ..build_image import BuildImage
from hoshino import Service
import os
from .._R import get

no = f"{get('emotion/no.png').cqcode}"

sv_help = '''
名人们：我当年确实说过
'''.strip()

sv = Service('鲁迅草图', enable_on_default = True, help_ = sv_help)
luxun_author = BuildImage(0, 0, plain_text="——鲁迅", font_size=30, font='STKAITI.TTF', font_color=(255, 255, 255))
shake_author = BuildImage(0, 0, plain_text="——莎士比亚", font_size=30, font='HGFS_CNKI.TTF', font_color=(255, 255, 255))


@sv.on_prefix('鲁迅说', '鲁迅说过', '鲁迅讲', '鲁迅讲过')
async def luxun_once_said(bot, ev):
    message = ev.message.extract_plain_text().strip()
    for biaodian in [',', '，', ':', '：']:
        if message.startswith(biaodian):
            message.strip(biaodian)
    imageFile = os.path.join(os.path.dirname(__file__), f'luxun.jpg')
    bg = BuildImage(0, 0, font_size=37, background=imageFile, font='STKAITI.TTF')
    say = ''
    if len(message) > 40:
        say = '太长了，我说不完。'
    if len(message) == 0:
        say = '你得让我说点啥。'
    if not say:
        while bg.getsize(message)[0] > bg.w - 50:
            n = int(len(message) / 2)
            say += message[:n] + '\n'
            message = message[n:]
        say += message
    if len(say.split('\n')) > 2:
        say = '太长了，我说不完。'
    bg.text((int((480 - bg.getsize(say.split("\n")[0])[0]) / 2), 300), say, (255, 255, 255))
    bg.paste(luxun_author, (320, 400), True)
    imageToSend = f"[CQ:image,file=base64://{bg.pic2bs4()}]"
    await bot.send(ev, imageToSend)


@sv.on_prefix('莎士比亚说', '莎士比亚说过', '莎士比亚讲', '莎士比亚讲过')
async def shashibiya_once_said(bot, ev):
    message = ev.message.extract_plain_text().strip()
    for biaodian in [',', '，', ':', '：']:
        if message.startswith(biaodian):
            message.strip(biaodian)
    imageFile = os.path.join(os.path.dirname(__file__), f'shashibiya.jpg')
    bg = BuildImage(0, 0, font_size=37, background=imageFile, font='HGFS_CNKI.TTF')
    say = ''
    if len(message) > 40:
        say = '太长了，这是个问题。'
    if len(message) == 0:
        say = '我什么也没有说。'
    if not say:
        while bg.getsize(message)[0] > bg.w - 50:
            n = int(len(message) / 2)
            say += message[:n] + '\n'
            message = message[n:]
        say += message
    if len(say.split('\n')) > 2:
        say = '太长了，这是个问题。'
    bg.text((int((440 - bg.getsize(say.split("\n")[0])[0]) / 2), 380), say, (255, 255, 255))
    bg.paste(shake_author, (230, 510), True)
    imageToSend = f"[CQ:image,file=base64://{bg.pic2bs4()}]"
    await bot.send(ev, imageToSend)
