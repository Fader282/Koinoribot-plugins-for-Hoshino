import os
import random

from hoshino import Service
from ..utils import loadData, saveData


sv = Service('今天也是超人')


@sv.on_fullmatch('我的超能力')
async def my_ability(bot, ev):
    ab_dict = loadData(os.path.join(os.path.dirname(__file__), 'ability.json'))
    ability = random.choice(ab_dict['ability'])
    harm = random.choice(ab_dict['harm'])
    await bot.send(ev, f'你的超能力是：\n{ability}\n但副作用是：\n{harm}')
