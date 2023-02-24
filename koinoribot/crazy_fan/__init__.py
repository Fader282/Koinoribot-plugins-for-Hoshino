import io
import random

from ..build_image import BuildImage
from .._R import imgPath
from aiocqhttp.exceptions import ActionFailed
from hoshino import Service
import os
import aiohttp
import re


sv = Service('狂粉表情包', enable_on_default = True, help_ = '爱到不能自已')
bgPath = os.path.join(imgPath, 'crazy_fan')
crazy_list = [
    {
        'background': 'crazy_fan_0.png',
        'diameter': 192,
        'pos-x': 216,
        'pos-y': 45
    },
    {
        'background': 'crazy_fan_1.png',
        'diameter': 150,
        'pos-x': 162,
        'pos-y': 19
    },
    {
        'background': 'crazy_fan_2.png',
        'diameter': 162,
        'pos-x': 189,
        'pos-y': 39
    },
]


async def creep_img(session, url, uid):  # 异步爬取
    imgname = f'{uid}.jpg'
    async with session.get(url) as r:
        content = await r.read()
        return content


@sv.on_prefix(('！狂粉', '!狂粉', '#狂粉'))
async def crazy_fan_image(bot, ev):

    message = ev.message
    image_check = 0
    qid_check = 0
    text_check = 1
    for raw_dict in message:
        if raw_dict['type'] == 'image':
            imageUrl = raw_dict['data']['url']
            image_check = 1
        elif raw_dict['type'] == 'at':
            image_qid = raw_dict['data']['qq']
            imageUrl = f'https://q1.qlogo.cn/g?b=qq&nk={image_qid}&src_uin=www.jlwz.cn&s=0'
            qid_check = 1
        elif raw_dict['type'] == 'text':
            image_qid = (raw_dict['data']['text']).strip()
            if str.isdigit(image_qid):
                imageUrl = f'https://q1.qlogo.cn/g?b=qq&nk={image_qid}&src_uin=www.jlwz.cn&s=0'
                qid_check = 1
        else:
            text_check = 1
    if image_check or qid_check:
        await bot.send(ev, '正在生成中，请稍候...')
        crazyIndex = random.randint(0, len(crazy_list) - 1)
        crazy_dict = crazy_list[crazyIndex]
        imageFile = os.path.join(bgPath, crazy_dict['background'])
        bg = BuildImage(0, 0, background = imageFile)
        async with aiohttp.ClientSession() as session:
            img = await creep_img(session, url = imageUrl, uid = ev.user_id)
        iconFile = io.BytesIO(img)
        icon = BuildImage(0, 0, background = iconFile)
        w, h = icon.size
        icon.resize(ratio = crazy_dict['diameter'] / min(w, h))
        icon.circle()
        bg.paste(icon, (crazy_dict['pos-x'], crazy_dict['pos-y']), True)
        imageToSend = f"[CQ:image,file=base64://{bg.pic2bs4()}]"
        await bot.send(ev, imageToSend)
        return
    elif text_check == 1:
        imageFile = os.path.join(bgPath, 'crazy_fan_3.png')
        bg = BuildImage(0, 0, background = imageFile)
        imageToSend = f"[CQ:image,file=base64://{bg.pic2bs4()}]"
        await bot.send(ev, imageToSend)
        return
    else:
        await bot.finish(ev, '没有找到要狂粉的对象...')


@sv.on_message('group')
async def crazy_fan_reply(bot, ev):
    if ev.group_id not in [837052156, 807505574]:
        return
    mid = ev.message_id
    uid = ev.user_id
    ret = re.search(r"\[CQ:reply,id=(-?\d*)\](.*)(！狂粉|!狂粉)", str(ev.message))
    if not ret:
        return
    replyMessageId = ret.group(1)
    try:
        replyMessage = await bot.get_msg(self_id=ev.self_id, message_id=int(replyMessageId))
    except ActionFailed:
        await bot.finish(ev, '该消息已过期，请重新转发~')
    ret = re.search(r"\[CQ:image,file=(.*)?,url=(.*)\]", str(replyMessage["message"]))
    if not ret:
        await bot.send(ev, '没有找到要狂粉的图片...')
        return
    await bot.send(ev, '正在生成中，请稍候...')
    crazyIndex = random.randint(0, len(crazy_list) - 1)
    crazy_dict = crazy_list[crazyIndex]
    imageUrl = ret.group(2)
    imageFile = os.path.join(bgPath, crazy_dict['background'])
    bg = BuildImage(0, 0, background = imageFile)
    async with aiohttp.ClientSession() as session:
        img = await creep_img(session, url = imageUrl, uid = ev.user_id)
    iconFile = io.BytesIO(img)
    icon = BuildImage(0, 0, background = iconFile)
    w, h = icon.size
    icon.resize(ratio = crazy_dict['diameter'] / min(w, h))
    icon.circle()
    bg.paste(icon, (crazy_dict['pos-x'], crazy_dict['pos-y']), True)
    imageToSend = f"[CQ:image,file=base64://{bg.pic2bs4()}]"
    await bot.send(ev, imageToSend)
    return

