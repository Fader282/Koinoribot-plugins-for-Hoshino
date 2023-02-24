import requests, json
from hoshino import Service
from hoshino.typing import CQEvent
import hoshino

from .. import money
from ..config import tianxing_apikey as apikey

sv = Service('彩虹屁生成器', enable_on_default=True, visible=True, help_='''
每天一句彩虹屁，对优秀的自己比个大拇指~
'''.strip())


def get_rainbow_p(apikey):
    url = 'http://api.tianapi.com/caihongpi/index?key=' + apikey
    r = requests.get(url)
    content = r.json()
    if content['code'] == 200:
        chp = content['newslist']
        return chp[0]['content']
    elif content['code'] == 150:
        alert = '今天冰祈已经夸累了QAQ'
        return alert


@sv.on_fullmatch(('夸我'))
async def send_rainbow_p(bot, ev: CQEvent):
    uid = ev.user_id
    name = ev.sender['nickname']
    cost_flag = 0
    try:
        rainbow_p = get_rainbow_p(apikey)
        rainbow_p = rainbow_p.replace('XXX', name)
        cost_flag = 1
    except Exception as e:
        hoshino.logger.error(f'彩虹p错误：{str(e)}, 请检查')
        rainbow_p = f'该功能好像被玩坏了...'
        cost_flag = 0
    if cost_flag:
        money.reduce_user_money(uid, "gold", 2)
    await bot.send(ev, rainbow_p, at_sender=True)
