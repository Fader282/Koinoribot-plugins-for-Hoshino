import ujson
import os

from hoshino import Service
from .aslogin_v3 import as_login_v3, get_purse, dl_save_image, del_custom_bg
from .. import money
from hoshino.util import FreqLimiter
from hoshino import priv

from ..call_me_please.util import *
from .._R import get, userPath

path = os.path.join(userPath, 'call_me_please/nickname.json')
flmt = FreqLimiter(60)
flmt_purse = FreqLimiter(30)
cost_num = 0  # 自定义图片需要的金币数

no = f"{get('emotion/no.png').cqcode}"

sv = Service('冰祈小签到')
'''简单的签到插件 生成签到卡片
'''

key_list = ["金币", "幸运币", "星星"]


@sv.on_fullmatch('签到', '冰祈签到', '#签到')
async def as_login_bonus(bot, ev):
    uid = ev['user_id']
    if not priv.check_priv(ev, priv.SUPERUSER):
        if not flmt.check(uid):
            await bot.send(ev, f'已经领过签到卡片啦，稍微等一下再来领喔~({round(flmt.left_time(uid))}s)')
            return
    nameList = load_data(path)
    if str(uid) in nameList.keys():
        if nameList[str(uid)]['self']:
            username = nameList[str(uid)]['self']
            nick_flag = 1
        elif nameList[str(uid)]['other']:
            username = nameList[str(uid)]['other']
            nick_flag = 1
        else:
            username = ev.sender['nickname']
            nick_flag = 0
    else:
        username = ev.sender['nickname']
        nick_flag = 0
    qqname = ev.sender['nickname']
    if uid == 80000000:
        qqname = '请不要匿名使用bot'
    imageToSend = await as_login_v3(uid = uid, username = username, qqname = qqname, nick_flag = nick_flag)
    await bot.send(ev, imageToSend)
#    else:
#        msg = as_login(uid, username)
#        await bot.send(ev,
    #        f'[CQ:image,file=base64://{image.image_to_base64(image.text_to_image(msg.strip())).decode()}]')
    flmt.start_cd(uid)


@sv.on_fullmatch('我的钱包', '#我的钱包')
async def money_get(bot, ev):
    uid = ev['user_id']
    if not priv.check_priv(ev, priv.SUPERUSER):
        if not flmt_purse.check(uid):
            await bot.send(ev, f'已经领过钱包卡片啦，稍微等一下再来领喔~({round(flmt_purse.left_time(uid))}s)')
            return
    qqname = ev.sender['nickname']
    if uid == 80000000:
        qqname = '匿名者'
    purse_card = await get_purse(uid = uid, user_name = qqname)
    await bot.send(ev, purse_card)
    flmt_purse.start_cd(uid)


@sv.on_prefix('上传签到图片', '#上传签到图片')
async def upload_bg(bot, ev):
    uid = ev['user_id']
    message = ev.message
    fetch_flag = 0
    for raw_dict in message:
        if raw_dict['type'] == 'image':
            imageUrl = raw_dict['data']['url']
            fetch_flag = 1
    if fetch_flag == 0:
        await bot.send(ev, '请附带图片~')
        return
    await dl_save_image(imageUrl, uid)
    user_gold = money.get_user_money(uid, 'gold')
    if cost_num == 0:
        msg = ""
    else:
        msg = f'(将扣除{cost_num}金币)'
    if user_gold > cost_num:
        await bot.send(ev, f'已上传图片~' + msg)
        money.reduce_user_money(uid, 'gold', cost_num)
    else:
        await bot.send(ev, '金币不足...' + no)


@sv.on_prefix('清除签到图片', '删除签到图片', '#清除签到图片', '#删除签到图片')
async def remove_cstm_bg(bot, ev):
    uid = ev['user_id']
    del_custom_bg(uid)
    await bot.send(ev, '已恢复默认背景~')


