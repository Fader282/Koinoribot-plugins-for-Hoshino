import io
import os
import asyncio
import random
import re

import ujson
import aiohttp
import hoshino
from hoshino import Service, aiorequests, R
from hoshino.util import FreqLimiter
from hoshino.config import SUPERUSERS, NICKNAME
from ..config import proxies, SAVE_MODE, DELETE_MODE
from .._R import userPath
from ..utils import loadData, chain_reply, get_net_img_proxy

sv = Service('danbooru搜图', enable_on_default=False, help_='搜图图源:danbooru')

path = os.path.join(userPath, 'danbooru')
RULE_PATH = os.path.join(os.path.dirname(__file__), 'rule.json')
danbooruTagUrl = 'https://yande.re/post.json?tags='
danbooruIdUrl = 'https://yande.re/post/'
DEBUG_MODE = 1

flmt = FreqLimiter(12)


async def danbooruImage(session, url, _id, _type):
    imgname = f'{_id}.{_type}'  # rename the image
    async with session.get(url) as r:
        content = await r.read()
        with open(os.path.join(path, imgname), "wb") as f:
            f.write(content)
    return imgname


@sv.on_prefix(('。tag', '#tag', '.tag', '/tag'))
async def danbooru_tag_search(bot, ev):
    gid = ev.group_id
    if ev.user_id not in SUPERUSERS:
        if not flmt.check(ev.user_id):
            await bot.send(ev, f'咏唱冷却中...({round(flmt.left_time(ev.user_id))})')
            return
    tag_info = ev.message.extract_plain_text().strip()

    comp_large = re.compile(r"-l")
    comp_limit = re.compile(r"-m(\d+)")
    comp_mount = re.compile(f"-n(\d+)")

    match_limit = re.search(comp_limit, tag_info)
    match_mount = re.search(comp_mount, tag_info)

    large = True if re.search(comp_large, tag_info) else False
    limit = match_limit.group(1) if match_limit else 100
    mount = match_mount.group(1) if match_mount else 1
    info_list = tag_info.split()
    if int(mount) > 6:
        await bot.send(ev, '不可以贪心...')
        return
    rule_list = loadData(RULE_PATH)
    if info_list[0] not in rule_list.keys():
        addition = '(未添加该tag，将用此tag直接搜索...)'
        tags = info_list[0]
    else:
        addition = ''
        tags = rule_list[info_list[0]]
    chain = []
    await bot.send(ev, f'{NICKNAME}咏唱中...' + addition)
    flmt.start_cd(ev.user_id)
    url = danbooruTagUrl + tags + f'&limit={limit}'
    hoshino.logger.info(url)
    try:
        getDanbooru = await (await aiorequests.get(url = url, proxies = proxies)).json()
        if len(getDanbooru) == 0:
            await bot.send(ev, f'{NICKNAME}没有找到相关的图片...')
            return
        getImg = random.sample(getDanbooru, int(mount))
    except Exception as e:
        await bot.send(ev, '准备咏唱时失败了...')
        hoshino.logger.error(f'danbooru标签搜图【{info_list[0]}】出错！！！！！！{e},{type(e)},{str(e)}')
        return
    for img in getImg:
        try:
            hoshino.logger.info('正在下载图片')
            imageId = img['id']
            if large:
                try:
                    imageUrl = img['file_url'] if 'file_url' in img.keys() else img['sample_url']
                except:
                    hoshino.logger.error('未找到图源')
                    imageUrl = ''
            else:
                try:
                    imageUrl = img['sample_url']
                except:
                    hoshino.logger.error('未找到图源')
                    imageUrl = ''
            fileType = img['file_ext']
            if SAVE_MODE:
                async with aiohttp.ClientSession() as session:
                    imageFile = await danbooruImage(session = session, url = imageUrl, _id = imageId, _type = fileType)
                imageToSend = f'[CQ:image,file=file:///{os.path.join(path, imageFile)}]\nd站图片id：{imageId}'
            else:
                bimg = await get_net_img_proxy(imageUrl)
                imageToSend = f"[CQ:image,file=base64://{bimg.pic2bs4()}]\nd站图片id：{imageId}"
        except Exception as e:
            imageToSend = f'咏唱失败了...{str(e)}'
        await chain_reply(bot, ev, chain, imageToSend, user_id=ev.user_id)
    try:
        msgInfo = await bot.send_group_forward_msg(group_id=ev.group_id, messages = chain)
        if DELETE_MODE:
            try:
                await asyncio.sleep(60)
                await bot.delete_msg(message_id=msgInfo['message_id'])
            except Exception as e:
                hoshino.logger.error(f"danbooru：tag搜图撤回失败：{str(e)}")
                return
    except Exception as e:
        await bot.send(ev, f"咏唱已完成,但是图片召唤失败了...")
        hoshino.logger.error(f"danbooru标签搜图发生错误B：{e}")


'''@sv.on_prefix(('danid', '#danid', '.danid', '/dandid'))
async def danbooru_id_search(bot, ev):
    gid = ev.group_id
    if ev.user_id in SUPERUSERS:
        if not flmt.check(ev.user_id):
            await bot.send(ev, f'咏唱冷却中...({round(flmt.left_time(ev.user_id))})')
            return
    id_info = ev.message.extract_plain_text().strip()
    if not id_info.isdigit():
        return
    await bot.send(ev, f'{NICKNAME}咏唱中...')
    try:
        url = danbooruIdUrl + f'{id_info}.json'
        getBooru = await (await aiorequests.get(url = url, proxies = proxies)).json()
        imageId = getBooru['id']
        imageUrl = getBooru['file_url']
        fileType = getBooru['file_ext']
    except Exception as e:
        await bot.send(ev, '准备咏唱时失败了..请检查id输入是否正确...')
        hoshino.logger.error(f'danbooruID搜图出错{e}')
        return
    if SAVE_MODE:
        try:
            async with aiohttp.ClientSession() as session:
                imageFile = await danbooruImage(session = session, url = imageUrl, _id = imageId, _type = fileType)
        except Exception as e:
            await bot.send(ev, f"咏唱失败了...{R.img('shiro_gomen.png').cqcode}")
            hoshino.logger.error(f"danbooruID搜图发生错误A：{e}")
            return
        imageToSend = f'[CQ:image,file=file:///{os.path.join(path, imageFile)}]'
    else:
        bimg = await get_net_img(imageUrl)
        imageToSend = f"[CQ:image,file=base64://{bimg.pic2bs4()}]"
    try:
        msgInfo = await bot.send(ev, imageToSend)
        flmt.start_cd(ev.user_id)
        if DELETE_MODE:
            try:
                await asyncio.sleep(60)
                await bot.delete_msg(message_id=msgInfo['message_id'])
            except Exception as e:
                hoshino.logger.error(f"danbooru：tag搜图撤回失败：{str(e)}")
                return
    except Exception as e:
        await bot.send(ev, f"咏唱已完成,但是图片召唤失败了...{R.img('shiro_gomen.png').cqcode}")
        hoshino.logger.error(f"danbooruID搜图发生错误B：{e}")'''


@sv.on_fullmatch(('标签列表', 'tag列表'))
async def tag_list(bot, ev):
    rule_list = loadData(RULE_PATH)
    tag_ = []
    chain = []
    for i in rule_list.keys():
        tag_.append(i)
    chain = await chain_reply(bot = bot, ev = ev, chain = chain, msg = '当前标签列表：' + '\n', user_id=ev.user_id)
    chain = await chain_reply(bot = bot, ev = ev, chain = chain, msg = '\n'.join(tag_), user_id=ev.user_id)
    await bot.send_group_forward_msg(group_id=ev.group_id, messages=chain)


@sv.on_prefix(('添加tag', 'tag添加', '添加标签', '标签添加'))
async def add_tag(bot, ev):
    uid = ev.user_id
    if uid not in SUPERUSERS:
        return
    rule_list = loadData(RULE_PATH)
    message = ev.message.extract_plain_text().strip()
    tagInfo = message.split('/')
    if len(tagInfo) != 2:
        return
    for key, value in rule_list.items():
        if tagInfo[0] in key:
            await bot.send(ev, f'已存在的标签:{key}')
            return
        elif tagInfo[1] in value:
            await bot.send(ev, f'已存在的标签:{value}')
            return
    rule_list[tagInfo[0]] = tagInfo[1]
    with open(RULE_PATH, 'r+', encoding='utf-8') as f:
        ujson.dump(rule_list, f, ensure_ascii=False, indent = 4)
    msg = f'已添加tag：{tagInfo[1]},搜索词：{tagInfo[0]}'
    await bot.send(ev, msg)


@sv.on_prefix(('删除tag', 'tag删除', '删除标签', '标签删除'))
async def remove_tag(bot, ev):
    uid = ev.user_id
    if uid not in SUPERUSERS:
        return
    message = ev.message.extract_plain_text().strip()
    rule_list = loadData(RULE_PATH)
    if message not in rule_list.keys():
        await bot.send(ev, '该tag不在列表里~')
        return
    del rule_list[message]
    with open(RULE_PATH, 'r+', encoding = 'utf-8') as f:
        f.truncate(0)
        ujson.dump(rule_list, f, ensure_ascii = False, indent = 4)
    await bot.send(ev, f'已删除tag:{message}')