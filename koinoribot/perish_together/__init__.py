import random
import re

from hoshino import Service

from .._R import get

sv_help = '''
同归于尽吧！
'''.strip()

sv = Service('perish_together', visible=True, enable_on_default=True, help_=sv_help)

no = f"{get('emotion/no.png').cqcode}"
emmm = f"{get('emotion/无语.png').cqcode}"


@sv.on_prefix('同归于尽')
@sv.on_suffix('同归于尽')
async def perish_together_function(bot, ev):
    uid = ev.user_id
    gid = ev.group_id
    sid = ev.self_id
    if sid == 2530075673:
        group_info = await bot.get_group_member_list(group_id = gid)
        member_list = [member['user_id'] for member in group_info]
        if 3625681236 in member_list:
            return
    timeAddFlag = 0
    multi_list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                  2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                  3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                  4, 4, 4, 4, 4, 4, 4, 4, 4,
                  5, 5, 5, 5, 5, 5,
                  6, 6, 6, 6,
                  7, 7, 7,
                  8, 8,
                  9,
                  10]
    self_info = await bot.get_group_member_info(user_id=sid, group_id=gid)
    role = self_info['role']  # bot自己的权限
    if role == 'member':
        await bot.send(ev, '冰祈不是管理员啦...' + emmm)
        return
    user_info = await bot.get_group_member_info(user_id=uid, group_id=gid)
    user_role = user_info['role']  # 自己的权限
    try:
        match = re.search(r'(?:\[CQ:at,qq=(\d+)\])', ev.raw_message)
        opposite_uid = int(match.group(1))  # 如果艾特全体，则这里无法处理，刻意报错
    except:
        await bot.send(ev, '要艾特到对方才可以同归于尽~')
        return
    if int(opposite_uid) == uid:
        await bot.send(ev, '自己不可以和自己玩同归于尽喔' + emmm)
        return
    opposite_info = await bot.get_group_member_info(user_id=opposite_uid, group_id=gid, no_cache=True)
    opposite_role = opposite_info['role']  # 艾特对方的权限
    nowTime = ev.time
    if nowTime < opposite_info['shut_up_timestamp']:
        timeAdd = opposite_info['shut_up_timestamp'] - nowTime
        timeAddFlag = 1
    else:
        timeAdd = 0
        timeAddFlag = 0
    if role == 'admin':
        if user_role == 'admin':
            await bot.send(ev, '管理员不可以玩同归于尽哦' + no)
            return
        if user_role == 'owner':
            await bot.send(ev, '群主不可以玩同归于尽哦' + no)
            return
        if opposite_role != 'member':
            await bot.send(ev, '对方不可以参与同归于尽' + no)
            return
        opposite_time = random.randrange(1, 181)
        multi = random.choice(multi_list)
        user_time = opposite_time * multi
        final_random = random.randrange(1001)  # 最终的随机选择，自己没事或者对方没事
        if final_random < 50:
            if timeAddFlag:
                await bot.set_group_ban(group_id=gid, user_id=opposite_uid, duration=timeAdd + opposite_time)
                await bot.send(ev, f'对方追加了{timeAdd}s的禁言，而幸运的你未受到反弹。', at_sender=True)
            else:
                await bot.set_group_ban(group_id=gid, user_id=opposite_uid, duration=opposite_time)
                await bot.send(ev, f'对方受到了{opposite_time}s的禁言，而幸运的你未受到反弹。', at_sender=True)
        elif final_random < 950:
            if timeAddFlag:
                await bot.set_group_ban(group_id=gid, user_id=opposite_uid, duration=timeAdd + opposite_time)
                await bot.set_group_ban(group_id=gid, user_id=uid, duration=user_time)
                await bot.send(ev, f'对方追加了{opposite_time}s的禁言，而你受到了{multi}倍反弹。', at_sender=True)
            else:
                await bot.set_group_ban(group_id=gid, user_id=opposite_uid, duration=opposite_time)
                await bot.set_group_ban(group_id=gid, user_id=uid, duration=user_time)
                await bot.send(ev, f'对方受到了{opposite_time}s的禁言，而你受到了{multi}倍反弹。', at_sender=True)
        else:
            await bot.set_group_ban(group_id=gid, user_id=uid, duration=user_time)
            await bot.send(ev, f'对方幸运地闪开了，而你受到了{user_time}s的禁言', at_sender=True)
        return
    if role == 'owner':
        if opposite_role == 'owner':
            await bot.send(ev, '对方不可以参与同归于尽' + no)
            return
        opposite_time = random.randrange(1, 181)
        multi = random.choice(multi_list)
        user_time = opposite_time * multi
        final_random = random.randrange(1001)  # 最终的随机选择，自己没事或者对方没事
        if final_random < 50:
            if timeAddFlag:
                await bot.set_group_ban(group_id=gid, user_id=opposite_uid, duration=timeAdd + opposite_time)
                await bot.send(ev, f'对方追加了{timeAdd}s的禁言，而幸运的你未受到反弹。', at_sender=True)
            else:
                await bot.set_group_ban(group_id=gid, user_id=opposite_uid, duration=opposite_time)
                await bot.send(ev, f'对方受到了{opposite_time}s的禁言，而幸运的你未受到反弹。', at_sender=True)
        elif final_random < 950:
            if timeAddFlag:
                await bot.set_group_ban(group_id=gid, user_id=opposite_uid, duration=timeAdd + opposite_time)
                await bot.set_group_ban(group_id=gid, user_id=uid, duration=user_time)
                await bot.send(ev, f'对方追加了{opposite_time}s的禁言，而你受到了{multi}倍反弹。', at_sender=True)
            else:
                await bot.set_group_ban(group_id=gid, user_id=opposite_uid, duration=opposite_time)
                await bot.set_group_ban(group_id=gid, user_id=uid, duration=user_time)
                await bot.send(ev, f'对方受到了{opposite_time}s的禁言，而你受到了{multi}倍反弹。', at_sender=True)
        else:
            await bot.set_group_ban(group_id=gid, user_id=uid, duration=user_time)
            await bot.send(ev, f'对方幸运地闪开了，而你受到了{user_time}s的禁言', at_sender=True)
