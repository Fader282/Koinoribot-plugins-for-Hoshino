import random
from itertools import cycle
from random import shuffle

from aiocqhttp import MessageSegment

from hoshino import Service, priv
from hoshino.typing import CQEvent
from .._interact import interact, ActSession
from .util import get_user_name, get_score, text2CQimg


sv = Service('不谢牌游戏', manage_priv=priv.ADMIN)


min_user = 2  # 最低游玩人数


@sv.on_fullmatch('不谢牌', '#不谢牌')
async def no_thanks_game_start(bot, ev):
    if interact.find_session(ev, name='不谢牌'):
        session = interact.find_session(ev, name='不谢牌')
        if session.is_expire():
            session.close()
        else:
            await bot.send(ev, f'上一轮不谢牌还没结束，使用"退出"强制结束游戏喔')
            return

    session = ActSession.from_event('不谢牌', ev, usernum_limit = True, max_user = 5, expire_time=1500)
    interact.add_session(session)

    await bot.send(ev, '游戏已发起,目前有1位玩家,至多要5名玩家,发送"参与不谢牌"加入游戏')


@sv.on_fullmatch('参与不谢牌', '#参与不谢牌')
async def join_no_thanks(bot, ev):
    session = interact.find_session(ev, name='不谢牌')
    if not session: #session未创建
        await bot.send(ev, '当前没有等待中的不谢牌，发送不谢牌发起游戏')
        return #不处理
    if session.is_expire():
        session.close()
        await bot.send(ev, f'当前没有等待中的不谢牌，发送不谢牌发起游戏')
        return

    try:
        interact.join_session(ev, session)
    except ValueError as e:
        await bot.send(ev, str(e))
        return
    await bot.send(ev, f'成功加入,目前有{session.count_user()}位玩家,发送“ntx”进行游戏')



@interact.add_action('不谢牌', ('ntx', ))
async def start_no_thanks(ev: CQEvent, session: ActSession):
    bot = session.bot
    if session.count_user() < min_user:
        await session.send(ev, f'至少要{min_user}个人才能玩不谢牌噢~')
        return

    if not session.state.get('started'):
        session.state['started'] = True
        if len(session.users) == 2:
            card_count = 12
            max_card = 18
            chips = 7
        elif len(session.users) == 3:
            card_count = 18
            max_card = 24
            chips = 9
        else:
            card_count = 27
            max_card = 35
            chips = 11
        _list = [i for i in range(3, max_card)]
        rule = f"""
        从3到{max_card}的{max_card-2}张牌中抽取{card_count}张牌，每张牌只需回答"要"或是"不要"。
不要则交出一枚筹码，要则将这张牌及上面的筹码收下。
当所有牌都被收下，则开始计算牌面点数和。
有连号则只计算最小的一张，且一个筹码减一分，得分最高者输。
        """.strip()
        await session.send(ev, rule)
        if not session.rotate: #user轮流
            shuffle(session.users)
            session.state['rotate'] = cycle(session.users)
        if not session.turn:
            session.state['turn'] = session.rotate.__next__()

        shuffle(_list)
        session.state['cards'] = random.sample(_list, card_count)
        session.state['cur_card'] = session.state['cards'].pop()  # 当前牌
        session.state['cur_chip'] = 0  # 当前筹码
        session.state['usercard'] = {}
        for user in session.users:
            name = await get_user_name(bot, user)
            name = name[: 10]  # 取前10个字符
            session.state['usercard'][str(user)] = {'card': [], 'chip': chips, 'name': name}  # 获得的牌与筹码，用户名称
        try:
            await session.send(ev, f'游戏开始,现在这张牌是：{session.state["cur_card"]}点，现在请{MessageSegment.at(session.state["turn"])}选择"要"或"不要"这张牌')
        except:
            await session.send(ev, f'游戏开始,现在这张牌是：{session.state["cur_card"]}点，现在请{session.state["turn"]}选择"要"或"不要"这张牌')
    else:
        await session.send(ev, '游戏已经开始了')


@interact.add_action('不谢牌', ('不要', ))
async def defuse_card(ev: CQEvent, session:ActSession):
    bot = session.bot
    if not session.state.get('started'):
        await session.send(ev, '请先发送“开始”进行游戏')
        return

    if ev.user_id != session.state.get('turn'):
        await session.send(ev, '不可以替其他人决定喔')
        return

    if not session.state['usercard'][str(session.state['turn'])].get('chip'):
        session.state['usercard'][str(session.state['turn'])]['card'].append(session.state['cur_card'])
        session.state['usercard'][str(session.state['turn'])]['chip'] += session.state['cur_chip']
        await bot.send(ev, f'{MessageSegment.at(session.state["turn"])}你已经没有筹码了，必须收下这张牌和{session.state["cur_chip"]}枚筹码')

        await new_card_or_end(ev, session)    # auto return

    session.state['usercard'][str(session.state["turn"])]['chip'] -= 1
    session.state['turn'] = session.rotate.__next__()
    session.state['cur_chip'] += 1

    if not session.state['usercard'][str(session.state['turn'])].get('chip'):
        session.state['usercard'][str(session.state['turn'])]['card'].append(session.state['cur_card'])
        session.state['usercard'][str(session.state['turn'])]['chip'] += session.state['cur_chip']
        await bot.send(ev, f'{MessageSegment.at(session.state["turn"])}你已经没有筹码了，必须收下这张牌和{session.state["cur_chip"]}枚筹码')

        await new_card_or_end(ev, session)
    else:
        await bot.send(ev, f'牌上已有{session.state["cur_chip"]}枚筹码，请{MessageSegment.at(session.state["turn"])}选择"要"或"不要"这张{session.state["cur_card"]}点牌')
        return


@interact.add_action('不谢牌', ('要', ))
async def accept_card(ev: CQEvent, session: ActSession):
    bot = session.bot
    if not session.state.get('started'):
        await bot.send(ev, '请先发送“开始”进行游戏')
        return

    if ev.user_id != session.state.get('turn'):
        await session.send(ev, '不可以替其他人决定喔')
        return

    session.state['usercard'][str(session.state['turn'])]['card'].append(session.state['cur_card'])
    session.state['usercard'][str(session.state['turn'])]['chip'] += session.state['cur_chip']
    session.state['cur_chip'] = 0

    await new_card_or_end(ev, session)


@interact.add_action('不谢牌', ('结束', '退出'))
async def accept_card(ev: CQEvent, session: ActSession):
    session.close()
    await session.send(ev, '不谢牌游戏已强制结束，感谢游玩！')
    return


async def end_no_thanks_game(ev, session):  # session指定不谢牌
    bot = session.bot
    result = {}
    cqimg = await get_cur_score(ev, session)
    msg = '当前牌已抽完，最终得分如下：'
    extra = ''
    lose_user = 0
    other_lose = []
    lose_score = -99
    for user in session.users:
        vaild, score = get_score(session.state['usercard'][str(user)]['card'])
        str_vaild = [str(i) for i in vaild]
        calc_msg = '+'.join(str_vaild) + '-' + str(session.state['usercard'][str(user)]['chip']) + '=' + str(score - session.state['usercard'][str(user)]['chip'])
        msg += f'\n{calc_msg}'
        if score > lose_score:
            lose_user = user
            lose_score = score
        elif score == lose_score:
            other_lose.append(user)
    if len(other_lose) >= 1:
        extra += f'{MessageSegment.at(lose_user)}和{"、".join(other_lose)}输掉了游戏'
    elif len(other_lose) == len(session.users) - 1:
        extra = '所有人达成平局'
    else:
        extra = f'{MessageSegment.at(lose_user)}输掉了游戏'
    session.close()
    await bot.send(ev, f'{cqimg}{msg}\n{extra}')


async def get_cur_score(ev, session):
    """
        获取当前局势，转为图片
    """
    print(session.state['usercard'])
    msg = '当前牌桌：'
    for user in session.users:
        vaild, score = get_score(session.state['usercard'][str(user)]['card'])
        final_score = score - session.state['usercard'][str(user)]['chip']
        session.state['usercard'][str(user)]['card'].sort()
        user_card_str = str(session.state['usercard'][str(user)]['card']).replace("[", "").replace("]", "")
        user_msg = f"\n{session.state['usercard'][str(user)]['name']}的筹码数：{session.state['usercard'][str(user)]['chip']}" \
                   f"\n收下的牌：{user_card_str}" \
                   f"\n当前分数：{final_score}"
        msg += user_msg
    cqimg = text2CQimg(msg)
    return cqimg


async def new_card_or_end(ev, session):
    """
        发新的牌，或者结束游戏
    """
    bot = session.bot
    if not session.state['cards']:  # 结算
        await end_no_thanks_game(ev, session)
    else:
        cqimg = await get_cur_score(ev, session)
        session.state['cur_chip'] = 0
        session.state['cur_card'] = session.state['cards'].pop()  # 当前牌
        session.state['turn'] = session.rotate.__next__()
        await bot.send(ev, f'{cqimg}新的一张牌是：{session.state["cur_card"]}点，请{MessageSegment.at(session.state["turn"])}选择是否要这张牌')
        return