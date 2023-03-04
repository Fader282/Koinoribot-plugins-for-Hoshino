import os
import random

import hoshino
from aiocqhttp.exceptions import ActionFailed
from hoshino import Service
from ..GroupFreqLimiter import check_reload_group, set_reload_group
from hoshino.util import FreqLimiter
from hoshino.config import SUPERUSERS

from .. import money, config
from .._R import get, userPath
from .util import shift_time_style, update_serif
from ..utils import chain_reply, saveData

from .get_fish import fishing, buy_bait, free_fish, sell_fish, change_fishrod, compound_bottle, getUserInfo, increase_value, decrease_value
from .serif import cool_time_serif
from .get_bottle import get_bottle_amount, check_bottle, format_message, check_permission, check_content, set_bottle, delete_bottle
from .._interact import interact, ActSession
from .evnet_functions import random_event

'''if not config.DEBUG_MODE:
    SUPERUSERS = [SUPERUSERS[0]]'''

event_list = list(random_event.keys())

sv = Service("冰祈与鱼", enable_on_default=True)

_help = '''
<---冰祈与鱼--->
#钓鱼帮助  🎣打开帮助菜单
#钓鱼/#🎣  🎣开始钓鱼
#买鱼饵 [数量(可选)]  🎣购买鱼饵
#背包/#仓库  🎣查看背包
#卖鱼/#sell [🐟🦐🐡] [数量(可选)]  🎣出售，数量和鱼用空格隔开
#放生/#free [🐟🦐🐡] [数量(可选)]  🎣放生，同上
#钓鱼统计/#钓鱼记录  🎣查看自己的钓鱼记录
🔮为水之心，收集3个可以合成一个漂流瓶
放生足够多的话可以获得特别谢礼
#合成漂流瓶 [数量(可选)]  🎣消耗水之心合成
#扔漂流瓶 [消息]  🎣投放一个漂流瓶
'''.strip()

rod_help = '''
当前鱼竿：
1.普通鱼竿
2.永不空军钓竿(不会空军)
3.海之眷顾钓竿(稀有鱼概率UP)
4.时运钓竿(概率双倍鱼)
发送"#换钓竿+ID"更换钓竿
'''.strip()

event_flag = {}

no = get('emotion/no.png').cqcode
ok = get('emotion/ok.png').cqcode
fish_list = ['🐟', '🦐', '🦀', '🐡', '🐠', '🔮', '✉', '🍙', '水之心']
admin_path = os.path.join(userPath, 'fishing/db/admin.json')
freq = FreqLimiter(config.COOL_TIME)


@sv.on_fullmatch('#钓鱼帮助', '钓鱼帮助')
async def fishing_help(bot, ev):
    if check_reload_group(ev.group_id, _type='boolean'):
        await bot.send(ev, '字太多了，翻看一下消息记录吧QAQ')
        return
    set_reload_group(ev.group_id, _time=600)
    await bot.send(ev, _help)


@sv.on_fullmatch('#钓鱼', '#🎣', '＃钓鱼')
async def go_fishing(bot, ev):
    uid = ev.user_id
    user_info = getUserInfo(uid)
    if not freq.check(uid) and not config.DEBUG_MODE:
        await bot.send(ev, random.choice(cool_time_serif) + f'({int(round(freq.left_time(uid)) / 60)}min)')
        return
    if user_info['fish']['🍙'] == 0:
        await bot.send(ev, '没有鱼饵喔，要买点鱼饵嘛？(或发送#钓鱼帮助)')
        return
    freq.start_cd(uid)
    await bot.send(ev, '你开始了钓鱼...')
    decrease_value(uid, 'fish', '🍙', 1)

    resp = fishing(uid)

    if resp['code'] == 1:
        msg = resp['msg']
        await bot.send(ev, msg, at_sender=True)
        return
    elif resp['code'] == 2:  # 漂流瓶模式
        bottle_amount = get_bottle_amount()
        second_choose = random.randint(1, 1000)
        probability = min(float(bottle_amount / 50), 0.7) * 1000
        if second_choose > probability:
            fish = fish_list[5]
            increase_value(uid, 'fish', fish, 1)
            await bot.send(ev, f'你发现鱼竿有着异于平常的感觉，竟然钓到了一颗水之心🔮~', at_sender=True)
            return
        else:
            bottle = check_bottle()
            if config.DEBUG_MODE:
                hoshino.logger.info(f'漂流瓶内容：{bottle}')
            if bottle is None:
                fish = fish_list[5]
                increase_value(uid, 'fish', fish, 1)
                hoshino.logger.error(f'漂流瓶为空，将替换为水之心')
                await bot.send(ev, f'钓到了一颗水之心🔮~', at_sender=True)
                return
            try:
                await bot.send(ev, f'你的鱼钩碰到了什么，看起来好像是一个漂流瓶！', at_sender=True)
                content = await format_message(bot, ev, bottle)
                await bot.send_group_forward_msg(group_id=ev.group_id, messages=content)
            except ActionFailed:
                increase_value(uid, 'fish', '✉', 1)
                await bot.send(ev, f'你的鱼钩碰到了一个空漂流瓶，似乎还可以回收使用！(漂流瓶+1)')
            return
    elif resp['code'] == 3:  # 随机事件模式
        choose_ev = random.choice(event_list)
        hoshino.logger.info(choose_ev) if config.DEBUG_MODE else None
        session = ActSession.from_event(choose_ev, ev, max_user=1, usernum_limit=True)
        try:
            interact.add_session(session)
        except ValueError:
            hoshino.logger.error('两个人的随机事件冲突了。')
            increase_value(uid, 'fish', '✉', 1)
            await bot.send(ev, '你的鱼钩碰到了一个空漂流瓶！可以使用"#扔漂流瓶+内容"使用它哦！')
            return
        session.state['started'] = True
        event_flag[str(uid)] = choose_ev
        msg = random_event[choose_ev]['msg'] + '\n'.join(random_event[choose_ev]['choice'])
        msg += '\n(发送/+选项ID完成选择~)'
        await bot.send(ev, msg, at_sender = True)
    else:
        return


@sv.on_prefix('#买鱼饵', '#买饭团', '#买🍙', '#购买鱼饵', '#购买', '#购买饭团', '＃买鱼饵', '＃买饭团', '＃买🍙', '＃购买鱼饵', '＃购买', '＃购买饭团')
async def buy_bait_func(bot, ev):
    uid = ev.user_id
    user_info = getUserInfo(uid)
    if user_info['fish']['🍙'] > 150:
        await bot.send(ev, '背包太满，装不下...' + no)
        return
    message = ev.message.extract_plain_text().strip()
    if not message or not str.isdigit(message):
        num = 1
    else:
        num = int(message)
    if num>50:
        await bot.send(ev, '一次只能购买50个鱼饵喔' + no)
        return
    user_gold = money.get_user_money(uid, 'gold')
    if user_gold<num * config.BAIT_PRICE:
        await bot.send(ev, '金币不足喔...' + no)
        return
    buy_bait(uid, num)
    await bot.send(ev, f'已经成功购买{num}个鱼饵啦~(金币-{num * config.BAIT_PRICE})')


@sv.on_fullmatch('#背包', '#仓库', '#我的背包', '#我的仓库', '＃背包', '＃仓库', '＃我的背包', '＃我的仓库')
async def my_fish(bot, ev):
    uid = ev.user_id
    user_info = getUserInfo(uid)
    msg = '背包：\n'
    items = ''
    for i, j in user_info['fish'].items():
        if j == 0:
            continue
        i = '当前可丢漂流瓶' if i == '✉' else i
        i = '当前可用鱼饵🍙' if i == '🍙' else i
        items += f'{i}×{j}\n'
    if not items:
        items = '空空如也...'
    msg += items
    await bot.send(ev, msg.strip('\n'), at_sender=True)


@sv.on_prefix('#放生', '#free', '＃放生', '＃free')
async def free_func(bot, ev):
    message = ev.message.extract_plain_text().strip()
    msg_split = message.split()
    fish = ''
    num = 0
    if len(msg_split) == 2:
        if msg_split[0] not in ['🐟', '🦐', '🦀', '🐡', '🐠']:
            return
        if not str.isdigit(msg_split[-1]):
            return
        fish = msg_split[0]
        num = int(msg_split[-1])
    elif len(msg_split) == 1:
        if msg_split[0] not in ['🐟', '🦐', '🦀', '🐡', '🐠']:
            return
        fish = msg_split[0]
        num = 1
    else:
        return
    uid = ev.user_id
    result = free_fish(uid, fish, num)
    await bot.send(ev, result, at_sender=True)


@sv.on_prefix('#卖鱼', '#sell', '#出售', '＃卖鱼', '＃sell', '＃出售')
async def free_func(bot, ev):
    message = ev.message.extract_plain_text().strip()
    msg_split = message.split()
    fish = ''
    num = 0
    if len(msg_split) == 2:
        if msg_split[0] not in ['🍙', '🐟', '🦐', '🦀', '🐡', '🐠', '🔮']:
            return
        if not str.isdigit(msg_split[-1]):
            return
        fish = msg_split[0]
        num = int(msg_split[-1])
    elif len(msg_split) == 1:
        if msg_split[0] not in ['🍙', '🐟', '🦐', '🦀', '🐡', '🐠', '🔮']:
            return
        fish = msg_split[0]
        num = 1
    else:
        return
    uid = ev.user_id
    result = sell_fish(uid, fish, num)
    await bot.send(ev, result, at_sender=True)


@sv.on_fullmatch('#钓鱼统计', '#钓鱼记录', '＃钓鱼统计', '＃钓鱼记录')
async def statistic_of_fish(bot, ev):
    uid = ev.user_id
    user_info = getUserInfo(uid)
    free_msg = f"已放生{user_info['statis']['free']}条鱼" if user_info['statis']['free'] else '还没有放生过鱼'
    sell_msg = f"已卖出{user_info['statis']['sell']}金币的鱼" if user_info['statis']['sell'] else '还没有出售过鱼'
    total_msg = f"总共钓上了{user_info['statis']['total_fish']}条鱼" if user_info['statis']['total_fish'] else '还没有钓上过鱼'
    await bot.send(ev, f'钓鱼统计：\n{free_msg}\n{sell_msg}\n{total_msg}', at_sender=True)


@sv.on_prefix('#换鱼竿', '＃换鱼竿')
async def change_rod_func(bot, ev):
    message = ev.message.extract_plain_text().strip()
    if not message:
        await bot.send(ev, rod_help)
        return
    if not str.isdigit(message):
        return
    _id = int(message)
    uid = ev.user_id
    result = change_fishrod(uid, _id)
    await bot.send(ev, result['msg'])


@sv.on_prefix('#扔漂流瓶', '#丢漂流瓶', '＃扔漂流瓶')
async def driftbottle_throw(bot, ev):
    message = ev.message
    uid = ev.user_id
    if check_permission(uid):
        await bot.send(ev, '河神拒绝了你的漂流瓶...' + no)
        return
    user_info = getUserInfo(uid)
    if not user_info['fish']['✉']:
        await bot.send(ev, '背包里没有漂流瓶喔' + no)
        return
    resp = check_content(message)
    if resp['code']<0:
        await bot.send(ev, resp['reason'])
        return
    gid = ev.group_id
    _time = ev.time
    decrease_value(uid, 'fish', '✉', 1)
    resp = set_bottle(uid, gid, _time, message)
    await bot.send(ev, '你将漂流瓶放入了水中，目送它漂向诗与远方...')
    chain = []
    await chain_reply(bot, ev, user_id=uid, chain=chain,msg=
                      f'QQ{uid}投放了一个漂流瓶。\n群聊：{gid}\n时间:{shift_time_style(_time)}\n漂流瓶ID:{resp}\n内容为：')
    await chain_reply(bot, ev, user_id=uid, chain=chain, msg=message)
    await bot.send_group_forward_msg(group_id=config.ADMIN_GROUP, messages=chain)


@sv.on_fullmatch('#捡漂流瓶', '#捞漂流瓶', '＃捡漂流瓶')  # 仅做测试用
async def driftbottle_get(bot, ev):
    gid = ev.group_id
    uid = ev.user_id
    if int(uid) not in SUPERUSERS:
        return
    bottle = check_bottle()
    if not bottle:
        await bot.send(ev, '没有漂流瓶可以捞')
        return
    content = await format_message(bot, ev, bottle)
    await bot.send_group_forward_msg(group_id=ev.group_id, messages=content)


@sv.on_prefix('#合成漂流瓶', '＃合成漂流瓶')
async def driftbottle_compound(bot, ev):
    uid = ev.user_id
    message = ev.message.extract_plain_text().strip()
    if not message or not str.isdigit(message):
        amount = 1
    else:
        amount = int(message)
    user_info = getUserInfo(uid)
    result = compound_bottle(uid, amount)
    await bot.send(ev, result['msg'])


@sv.on_prefix('#删除')
async def driftbottle_remove(bot, ev):
    gid = ev.group_id
    if gid != config.ADMIN_GROUP:
        return
    uid = ev.user_id
    message = ev.message.extract_plain_text().strip()
    if not (message and str.isdigit(message)):
        return
    if int(uid) not in SUPERUSERS:
        return
    resp = delete_bottle(message)
    await bot.send(ev, resp)


@sv.on_fullmatch('#清空')
async def driftbottle_truncate(bot, ev):
    uid = ev.user_id
    if int(uid) != SUPERUSERS[0]:
        return
    saveData({}, os.path.join(os.path.dirname(__file__), 'db/sea.json'))
    await bot.send(ev, ok)


@sv.on_fullmatch('#漂流瓶数量')
async def driftbottle_count(bot, ev):
    bottle_amount = get_bottle_amount()
    if not bottle_amount:
        await bot.send(ev, '目前水中没有漂流瓶...')
        return
    await bot.send(ev, f'当前一共有{get_bottle_amount()}个漂流瓶~')


@sv.on_prefix('#add')
async def add_items(bot, ev):
    return
    message = ev.message.extract_plain_text().strip()
    uid = ev.user_id
    if uid not in SUPERUSERS:
        return
    if not message:
        return
    fish_n_num = message.split()
    receive_id = fish_n_num[0]
    if not str.isdigit(receive_id):
        return
    if fish_n_num[1] not in ['🐟', '🦐', '🦀', '🐡', '🐠', '🔮', '✉']:
        return
    if len(fish_n_num) == 2:
        increase_value(receive_id, 'fish', fish_n_num[1], 1)
        await bot.send(ev, 'ok')
    elif len(fish_n_num) == 3:
        item_num = int(fish_n_num[-1])
        increase_value(receive_id, 'fish', fish_n_num[1], item_num)
        await bot.send(ev, 'ok')
    else:
        await bot.send(ev, "syntax:#add QQ_number fish_type (amount[optional])")
        return


@sv.on_prefix('#更新serif')
async def update_func(bot, ev):
    update_serif()
    await bot.send(ev, ok)



# <--------随机事件集-------->


@sv.on_fullmatch('/1', '/2', '/3', '/4')
async def random_event_trigger(bot, ev):
    uid = ev.user_id
    try:
        event_name = event_flag[str(uid)]
    except:
        hoshino.logger.info('随机事件未触发,事件标志未立起') if config.DEBUG_MODE else None
        return
    if not event_name:
        hoshino.logger.info('随机事件未触发,事件标志未设置') if config.DEBUG_MODE else None
        return
    session = interact.find_session(ev, name=event_name)
    if not session.state.get('started'):
        hoshino.logger.info('随机事件未触发,session未部署') if config.DEBUG_MODE else None
        return
    if uid != session.creator:
        hoshino.logger.info('非触发者的选择') if config.DEBUG_MODE else None
        return
    message = ev.raw_message
    _index = int(message.strip('/')) - 1
    if _index > len(random_event[event_name]['result']):
        hoshino.logger.info('序号超过选项数量') if config.DEBUG_MODE else None
        return
    event_flag[str(uid)] = ''
    session.close()
    await random_event[event_name]['result'][_index](bot, ev, uid)