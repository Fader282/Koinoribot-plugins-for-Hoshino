import random
import os
import time

import hoshino
from .._R import imgPath
from ..utils import loadData, saveData, pic2b64
from hoshino import Service
from .card_desc import cards
from hoshino.util import FreqLimiter
from hoshino.config import SUPERUSERS
from ..config import SEND_FORWARD

sv = Service('tarot-ba', visible= True, enable_on_default= True, bundle='碧蓝档案塔罗牌', help_='''
碧蓝档案塔罗牌
'''.strip())

flmt = FreqLimiter(8)


@sv.on_fullmatch('塔罗牌ba', '档案塔罗牌', 'ba塔罗牌')
async def blue_archive_tarot(bot, ev):
    if ev.user_id not in SUPERUSERS:
        if not flmt.check(ev.user_id):
            await bot.send(ev, f'冰祈理牌中...({round(flmt.left_time(ev.user_id))})')
            return
    await bot.send(ev, '冰祈洗牌中...')
    user_data = loadData(os.path.join(os.path.dirname(__file__), 'user.json'))
    if str(ev.user_id) in user_data.keys():
        current_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        if user_data[str(ev.user_id)]['time'] == current_time:
            card = user_data[str(ev.user_id)]['card']
            is_turned = user_data[str(ev.user_id)]['is_turned']
            msg = f'今天抽过的牌是{is_turned}的{card}~\n含义是：{cards[card][is_turned][0]}'
        else:
            user_data[str(ev.user_id)]['time'] = current_time
            card = random.choice(list(cards.keys()))
            is_turned = random.choice(['正位', '逆位'])
            user_data[str(ev.user_id)]['card'] = card
            user_data[str(ev.user_id)]['is_turned'] = is_turned
            msg = f'抽到了{is_turned}的{card}~\n含义是：{cards[card][is_turned][0]}'
            saveData(user_data, os.path.join(os.path.dirname(__file__), 'user.json'))
    else:
        card = random.choice(list(cards.keys()))
        is_turned = random.choice(['正位', '逆位'])
        user_data[str(ev.user_id)] = {'time': time.strftime("%Y-%m-%d", time.localtime(time.time())),'card': card,'is_turned': is_turned}
        msg = f'抽到了{is_turned}的{card}~\n含义是：{cards[card][is_turned][0]}'
        saveData(user_data, os.path.join(os.path.dirname(__file__), 'user.json'))

    img_path = os.path.join(imgPath, f'ba_wiki/tarot/{card}-{is_turned}.png')

    if SEND_FORWARD:
        chain = []
        try:
            await chain_reply(bot, ev, chain, msg, user_id=ev.self_id)
            await chain_reply(bot, ev, chain, f'[CQ:image,file=base64://{pic2b64(img_path)}]', ev.self_id)
            await bot.send_group_forward_msg(group_id=ev['group_id'], messages=chain)
        except Exception as e:
            hoshino.logger.error(f'合并转发碧蓝档案塔罗牌出错：{e}')
            await bot.send(ev, msg + '\n' + f'[CQ:image,file=base64://{pic2b64(img_path)}]')
    else:
        await bot.send(ev, msg + '\n' + f'[CQ:image,file=base64://{pic2b64(img_path)}]')

    flmt.start_cd(ev.user_id)


async def chain_reply(bot, ev, chain, msg, user_id = 0):
    """
        合并转发
    """
    data = {
            "type": "node",
            "data": {
                "name": '阿罗娜',
                "user_id": str(user_id),
                "content": msg
            }
        }
    chain.append(data)
    return chain

