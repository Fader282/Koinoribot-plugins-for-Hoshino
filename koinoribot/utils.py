import io
import json
import os
import re

import aiohttp
import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from .build_image import BuildImage


def saveData(obj, fp):
    """
    保存数据

    :param obj: 将要保存的数据
    :param fp: 文件路径
    """
    with open(fp, 'r+', encoding="utf-8") as file:
        file.truncate(0)
        json.dump(obj, file, ensure_ascii=False)


def loadData(fp, is_list = False):
    """
        加载json，不存在则创建
    """
    if os.path.exists(fp):
        file = json.load(open(fp, 'r', encoding='utf-8'))
        return file
    else:
        if not is_list:
            empty_dict = {}
            with open(fp, 'w', encoding='utf-8') as file:
                json.dump(empty_dict, file, ensure_ascii=False)
            return empty_dict
        else:
            empty_list = []
            with open(fp, 'w', encoding='utf-8') as file:
                json.dump(empty_list, file, ensure_ascii=False)
            return empty_list


def is_http_url(url):
    """
        检查字符串是否为链接
    """
    regex_ = re.compile(
        r'(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if regex_.findall(url):
        return True
    else:
        return False


async def chain_reply(bot, ev, chain, msg, user_id = 0):
    """
        合并转发
    """
    if ev.detail_type == 'guild':
        await bot.gsend(ev, msg)
        return chain
    if not user_id:
        user_id = ev.self_id
    user_info = await bot.get_stranger_info(user_id=user_id)
    user_name = user_info['nickname']
    data = {
            "type": "node",
            "data": {
                "name": user_name,
                "user_id": str(user_id),
                "content": msg
            }
        }
    chain.append(data)
    return chain


async def get_user_icon(uid) -> BuildImage:
    """
        获取用户头像
    """
    imageUrl = f'https://q1.qlogo.cn/g?b=qq&nk={uid}&src_uin=www.jlwz.cn&s=0'
    async with aiohttp.ClientSession() as session:
        async with session.get(imageUrl) as r:
            content = await r.read()
    iconFile = io.BytesIO(content)
    icon = BuildImage(0, 0, background = iconFile)
    return icon


async def get_net_img(url) -> BuildImage:
    """
        下载网络图片
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            content = await r.read()
    file = io.BytesIO(content)
    icon = BuildImage(0, 0, background = file)
    return icon


async def get_net_img_proxy(url) -> BuildImage:
    """
        下载网络图片（走代理）
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url, proxy = 'http://127.0.0.1:7890') as r:
            content = await r.read()
    file = io.BytesIO(content)
    icon = BuildImage(0, 0, background = file)
    return icon
