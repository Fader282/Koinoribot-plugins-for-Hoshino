from hoshino import Service
from hoshino.typing import CQEvent
from hoshino.util import DailyNumberLimiter
from . import my_mahjong as mj
from . import image
from hoshino.config import NICKNAME
from ..utils import chain_reply

sv = Service('今日役满', bundle='其他', help_='[今日役满] 看看今天的役满是？')

lmt = DailyNumberLimiter(5)

if type(NICKNAME) == str:
    NICKNAME = [NICKNAME]


@sv.on_fullmatch('随机役满')
async def mahjong_yakuman(bot, ev: CQEvent):
    mj.yi_zhong = []
    uid = ev.user_id
    if not lmt.check(uid):
        await bot.send(ev, '今天已经做过役满了哦', at_sender=True)
        return
    lmt.increase(uid)
    a = mj.random_yiman()
    final = mj.redraw(a)
    final_image = f'[CQ:image,file=base64://{image.image_to_base64(image.text_to_image(final.strip())).decode()}]'
    info = mj.recipe(mj.yi_zhong)
    name = ev.sender['card'] or ev.sender['nickname']
    chain = []
    first = f'来看看{name}做出的役满是：\n{final_image}'
    chain = await chain_reply(bot,ev,chain,first)
    second = f'包含的役满有：\n{info}'
    chain = await chain_reply(bot,ev,chain,second)
    await bot.send_group_forward_msg(group_id=ev['group_id'], messages=chain)