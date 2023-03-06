import asyncio

import os
import aiohttp
import time

import hoshino
from hoshino import Service
from hoshino.config import NICKNAME, SUPERUSERS
from hoshino.typing import CQEvent
from hoshino.util import FreqLimiter, DailyNumberLimiter
from .. import GroupFreqLimiter as freq
from .._R import get, userPath
from ..utils import chain_reply, get_net_img
from ..config import AUTO_SAVE, AUTO_DELETE, DELETE_TIME

url_iw = 'https://iw233.cn/API/Random.php'
url_loli = 'https://www.loliapi.com/acg'
path = os.path.join(userPath, "sinaimg")
white_path = os.path.join(os.path.dirname(__file__), 'whitelist.json')
_max = 99
_time = 30  # 单张图的冷却
_time_3 = 60
_nlmt = DailyNumberLimiter(_max)
_flmt = FreqLimiter(_time)
_flmt_3 = FreqLimiter(_time_3)


sv = Service('随机壁纸', visible= False, enable_on_default= False, bundle='美图', help_='''
随机壁纸(极密)
'''.strip())

if type(NICKNAME) == str:
    NICKNAME = [NICKNAME]


async def creep_img(session, url):  # 异步爬取
    current_time = time.strftime("%Y-%m-%d-%H%M%S", time.localtime())
    imgname = f'{current_time}.jpg'
    async with session.get(url) as r:
        content = await r.read()
        with open(os.path.join(path, imgname), "wb") as f:
            f.write(content)
        return imgname


@sv.on_rex(r'(来|來|莱)(点|點|份|張|张|丶)(涩|色|美|黄)(图|圖)(?P<kw>pc|cat)?')
async def random_wallpaper(bot, ev: CQEvent):
    gid = ev['group_id']
    match_msg = ev.match
    if ev.user_id not in SUPERUSERS:
        if freq.check_reload_group(group_id = gid, _type = 'boolean'):  # 整个群的冷却
            await bot.send(ev, f'冰祈冷却中...({freq.check_reload_group(gid)}s)')
            return
    await bot.send(ev, '冰祈咏唱中...')
    freq.set_reload_group(group_id = gid, _time = _time)
    msg_kw = match_msg.group('kw')
    url_iw = 'https://iw233.cn/API/Random.php'
    if msg_kw == 'pc':
        url_iw = 'https://iw233.cn/api.php?sort=pc'
    if msg_kw == 'cat':
        url_iw = 'https://iw233.cn/api.php?sort=cat'
    if AUTO_SAVE:
        try:
            async with aiohttp.ClientSession() as session:
                img = await creep_img(session, url = url_iw)
        except Exception as e:
            await bot.send(ev, f"咏唱失败了...{get('emotion/shiro_gomen.png').cqcode}")
            hoshino.logger.error(f"随机壁纸发生错误A：{e}")
            return
        image_file = f"file:///{os.path.join(path, img)}"
        final_image = f'[CQ:image,file={image_file}]'
    else:
        bimg = await get_net_img(url_iw)
        final_image = f"[CQ:image,file=base64://{bimg.pic2bs4()}]"
    try:
        msgInfo = await bot.send(ev, final_image)
        if AUTO_DELETE:
            try:
                await asyncio.sleep(DELETE_TIME)
                await bot.delete_msg(message_id=msgInfo['message_id'])
            except Exception as e:
                hoshino.logger.error(f"随机壁纸单张撤回失败：{str(e)}")
    except Exception as e:
        await bot.send(ev, f"咏唱已完成,但是图片召唤失败了...{get('emotion/shiro_gomen.png').cqcode}")
        hoshino.logger.error(f"随机壁纸发生错误B：{e}")


'''@sv.on_rex(r'(清除|清空)(缓存)')
async def wallpaper_temp_initial(bot, ev):
    if ev.user_id not in SUPERUSERS:
        return
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        shutil.rmtree(path)
        os.mkdir(path)
    await bot.send(ev, '清空缓存成功!')'''


@sv.on_fullmatch('美图三连')
async def triple_wallpaper(bot, ev):
    chain = []
    uid = ev['user_id']
    gid = ev['group_id']
    if freq.check_reload_group(group_id = gid, _type = 'boolean'):  # 整个群的冷却
        await bot.send(ev, f"冰祈..冷却中...({freq.check_reload_group(gid)}s){get('emotion/昏倒.png').cqcode}")
        return
    await bot.send(ev, '冰祈蓄力咏唱中...')
    freq.set_reload_group(group_id = gid, _time = _time_3)
    for i in range(3):
        try:
            await asyncio.sleep(1)
            if AUTO_SAVE:
                async with aiohttp.ClientSession() as session:
                    img = await creep_img(session, url = url_iw)
                image_file = f"file:///{os.path.join(path,img)}"
                final_image = f'[CQ:image,file={image_file}]'
            else:
                bimg = await get_net_img(url_iw)
                final_image = f"[CQ:image,file=base64://{bimg.pic2bs4()}]"
            chain = await chain_reply(bot, ev, chain, final_image, uid)
        except Exception as e:
            num = i + 1
            chain = await chain_reply(bot, ev, chain, f"第{num}张图片召唤失败了...{get('emotion/shiro_gomen.png').cqcode}, uid")
            hoshino.logger.error(f"随机壁纸发生错误C：{e}")
            continue
    try:
        msgInfo = await bot.send_group_forward_msg(group_id=gid, messages=chain)
        try:
            await asyncio.sleep(DELETE_TIME)
            await bot.delete_msg(message_id=msgInfo['message_id'])
        except Exception as e:
            hoshino.logger.error(f"随机壁纸单张撤回失败：{str(e)}")
    except Exception as e:
        await bot.send(ev, f"咏唱已完成,但是图片召唤失败了...{get('emotion/shiro_gomen.png').cqcode}")
        hoshino.logger.error(f"随机三连壁纸发生错误：{e}")

''' # 十连我服务器受不了
@sv.on_fullmatch('美图十连')
async def triple_wallpaper(bot, ev):
    chain = []
    uid = ev['user_id']
    if not _flmt_10.check(uid):
        await bot.send(ev, f"冰祈..冷却中...({round(_flmt_10.left_time(uid))}s){R.img('昏倒.png').cqcode}")
        return
    await bot.send(ev, '冰祈全力咏唱中...')
    for i in range(10):
        try:
            await asyncio.sleep(1)
            img = creep_img(url_iw)
            image_file = f"file:///{os.path.join(path,img)}"
            final_image = f'[CQ:image,file={image_file}]'
            chain = await chain_reply(bot, ev, chain, final_image)
        except Exception as e:
            num = i + 1
            chain = await chain_reply(bot, ev, chain, f"第{num}张图片召唤失败了...{R.img('shiro_gomen.png').cqcode}")
            hoshino.logger.error(f"随机壁纸发生错误：{e}")
            continue
    await bot.send_group_forward_msg(group_id=ev['group_id'], messages=chain)
    _flmt_10.start_cd(uid)
'''