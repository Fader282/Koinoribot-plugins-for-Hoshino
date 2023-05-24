from hoshino import Service
from ..money import reduce_user_money


sv = Service('叔叔我啊')


@sv.on_prefix('说喜欢', only_to_me=True)
async def koinori_said(bot, ev):
    uid = ev.user_id
    message = ev.message.extract_plain_text().strip()
    name = message
    if message in ['我', '咱', '俺']:
        gid = ev.group_id
        user_info = await bot.get_group_member_info(group_id=gid, user_id=uid, no_cache=True)
        if user_info['card']:
            name = user_info['card']
        elif user_info['nickname']:
            name = user_info['nickname']
        else:
            name = '你'
    if str.isdigit(message):
        stranger_info = await bot.get_stranger_info(user_id=int(message), no_cache=True)
        if stranger_info['nickname']: name = stranger_info['nickname']
    await bot.send(ev, f'冰祈我啊，最喜欢{name}了❤')
    reduce_user_money(uid, 'starstone', 50)