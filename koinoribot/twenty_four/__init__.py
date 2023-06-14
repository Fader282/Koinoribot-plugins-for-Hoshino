import os.path
import random
import re

from hoshino import Service
from ..utils import loadData
from .._interact import ActSession, interact
from .util import format_expression
from nonebot import MessageSegment


sv = Service('24点小游戏')


@sv.on_fullmatch('24点')
async def xxivgame_start(bot, ev):
    if interact.find_session(ev, name='24点游戏'):
        session = interact.find_session(ev, name='24点游戏')
        if session.is_expire():
            session.close()
        else:
            await bot.send(ev, f'已有24点游戏，当前的4个数是：{"".join(session.state["question"])}')
            return

    # 新建session
    session = ActSession.from_event('24点游戏', ev, usernum_limit=False, expire_time=300)
    interact.add_session(session)

    # 设置问题
    _dict = loadData(os.path.join(os.path.dirname(__file__), 'answer.json'))
    _list = list(_dict.keys())
    que_str = random.choice(_list)
    session.state['question'] = que_str.split()  # list
    session.state['question'].sort()
    session.state['hint'] = _dict[que_str]
    await bot.send(ev, f"当前题目：{que_str}\n使用 算式 来回答结果\n可以使用+-*/和()\n例：(1+2)*3/4 即可回答")
    return


@sv.on_message()
async def xxivgame_manage(bot, ev):
    if not interact.find_session(ev, name='24点游戏'):
        return
    session = interact.find_session(ev, name='24点游戏')
    if session.is_expire():
        session.close()
        await bot.send(ev, '24点游戏时间到~')
        return
    submit = ev.message.extract_plain_text().strip()
    if submit == '24点提示':
        await bot.send(ev, f'可以得到24点的式子：{session.state["hint"]}')
        return
    format_ = format_expression(submit)
    try:
        answer = eval(format_)  # 数
    except Exception as e:
        return
    answer = round(answer, 2)
    match = re.findall(r'(\d+)', submit)
    match.sort()
    question = session.state['question']
    question.sort()
    if match != question:
        await bot.send(ev, '必须要用到题目里的四个数喔')
        return
    uid = ev.user_id
    if answer == 24:
        session.close()
        await bot.send(ev, f'{format_}={answer}，{MessageSegment.at(uid)}回答正确~')
        return
    else:
        await bot.send(ev, f'{format_}={answer}，答案不对喔...')

