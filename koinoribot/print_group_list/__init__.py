import hoshino
from hoshino import Service
from hoshino.config import SUPERUSERS


sv = Service('查看冰祈所在所有群', visible=False)


@sv.on_fullmatch('打印群列表')
async def print_group_all(bot, ev):
    if ev.user_id not in SUPERUSERS:
        return 
    group_info = await bot.get_group_list(no_cache = True)
    group_list = [group['group_id'] for group in group_info]
    hoshino.logger.info(group_list)
    await bot.send('已将群列表输出至控制台')