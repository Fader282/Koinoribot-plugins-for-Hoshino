from hoshino import Service, util, priv
from hoshino.typing import CQEvent
from .choicer import Choicer
import re
import hoshino
from .._R import get

sv_help = '''
今天我要变成少女!
今天你是什么少女
'''.strip()

sv = Service(
    name = '今天也是少女',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '通用', #属于哪一类
    help_ = sv_help #帮助文本
    )

sorry = f"{get('emotion/shiro_gomen.png').cqcode}"

@sv.on_fullmatch(["帮助今天也是少女"])
async def bangzhu(bot, ev):
    await bot.send(ev, sv_help, at_sender=True)

inst = Choicer(util.load_config(__file__))

@sv.on_fullmatch('今天我是什么少女')
async def my_shoujo(bot, ev: CQEvent):
    uid = ev.user_id
    name = ev.sender['card'] or ev.sender['nickname']
    msg = inst.format_msg(uid, name)
    await bot.send(ev, msg)


@sv.on_prefix('今天你是什么少女')
@sv.on_prefix('今天他是什么少女')
@sv.on_prefix('今天她是什么少女')
@sv.on_prefix('今天它是什么少女')
@sv.on_suffix('今天你是什么少女')
@sv.on_suffix('今天他是什么少女')
@sv.on_suffix('今天她是什么少女')
@sv.on_suffix('今天它是什么少女')
async def other_shoujo(bot, ev: CQEvent):
    arr = []
    try:
        match = re.search(r'(?:\[CQ:at,qq=(\d+)\])', ev.raw_message)
        creep_id = match.group(1)
        arr.append(int(creep_id))
    except:
        await bot.send(ev, '要艾特到对方才知道是什么少女喔~')
        return
#    for i in ev.message:
#        if i['type'] == 'at' and i['data']['qq'] != 'all':
#            arr.append(int(i['data']['qq']))
    gid = ev.group_id
    bot_id = ev.self_id
    for uid in arr:
        info = await bot.get_group_member_info(
                group_id=gid,
                user_id=uid,
                no_cache=True
        )
        name = info['card'] or info['nickname']
        msg = inst.format_msg(uid, name)
        if uid == bot_id:
            msg = '冰祈身高143，毛色是白色，有呆毛，银白色双马尾，ACUP，红瞳，长着大大的茸耳，生日8月6日，害羞与文静属性，是一只耳廓狐娘>ω<'
            msg += get('emotion/shiro05.png').cqcode
        try:
            await bot.send(ev, msg)
        except Exception as e:
            hoshino.logger.error(f'---今天也是少女-功能发送失败，可能被风控:{e}')
            await bot.send(ev, f'变身结果发送失败，冰祈可能被风控...' + sorry)

