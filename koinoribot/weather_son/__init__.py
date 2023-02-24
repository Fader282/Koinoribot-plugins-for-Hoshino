import hoshino
from hoshino import Service, priv, R, util
from hoshino.typing import CQEvent
import random
from hoshino.util import FreqLimiter
from aiocqhttp.message import MessageSegment
from . import GroupFreqLimiter as freq

sv_help = '''
看看谁是那位幸运的天弃之子
'''.strip()

sv = Service('谁是天弃之子', visible=True, enable_on_default=True, help_=sv_help)

judge_point = ['♠A', '♠10', '♠J', '♠Q', '♠K',
               '♥A', '♥2', '♥3', '♥4', '♥5', '♥6', '♥7', '♥8', '♥9', '♥10', '♥J', '♥Q', '♥K',
               '♣A', '♣2', '♣3', '♣4', '♣5', '♣6', '♣7', '♣8', '♣9', '♣10', '♣J', '♣Q', '♣K',
               '♦A', '♦2', '♦3', '♦4', '♦5', '♦6', '♦7', '♦8', '♦9', '♦10', '♦J', '♦Q', '♦K', ]


emmm = f"{R.img('无语.png').cqcode}"
_time = 30  # 冷却时间(秒)


@sv.on_fullmatch('天弃之子')
async def weather_son_punish(bot, ev):
    gid = ev.group_id
    sid = ev.self_id
    uid = ev.user_id
    self_info = await bot.get_group_member_info(user_id=sid, group_id=gid, no_cache=True)
    role = self_info['role']
    if sid == 2530075673:
        group_info = await bot.get_group_member_list(group_id=gid)
        member_list = [member['user_id'] for member in group_info]
        if 3625681236 in member_list:
            return
    if role == 'member':
        await bot.send(ev, '冰祈不是管理员啦' + emmm)
        return
    if freq.check_reload_group(group_id=gid, _type='boolean'):  # 整个群的冷却
        await bot.send(ev, f'唤雷咏唱冷却中...({freq.check_reload_group(gid)}s)')
        return
    await bot.send(ev, f'冰祈咏唱中...')
    freq.set_reload_group(group_id=gid, _time=_time)
    group_info = await bot.get_group_member_list(group_id=gid)
    member_list = [member['user_id'] for member in group_info]
    member_list.remove(sid)
    son = int(random.choice(member_list))
    son_info = await bot.get_group_member_info(user_id=son, group_id=gid, no_cache=True)
    user_info = await bot.get_group_member_info(user_id=uid, group_id=gid, no_cache=True)
    son_nickname = son_info['nickname']
    user_nickname = user_info['nickname']
    son_role = son_info['role']
    time = random.randrange(1, 181)  # 随机禁言秒数
    if role == 'admin':
        if_success = random.randrange(101)
        if son_role == 'member':
            if if_success<80:  # 判定成功类
                judgement = random.randrange(101)
                if judgement<10:  # 触发者被劈
                    if user_info['role'] == 'owner':
                        await bot.set_group_ban(group_id=gid, user_id=uid, duration=time)
                        try:
                            await bot.send(ev, f"一道闪电从天而降，劈到了{son_nickname}，但{son_nickname}以一己之力将闪电送回了{MessageSegment.at(uid)}的身上!")
                        except:
                            await bot.send(ev, f"一道闪电从天而降，劈到了{son_nickname}，但{son_nickname}以一己之力将闪电送回了{user_nickname}的身上!")
                        return
                    else:
                        await bot.send(ev, f"一道闪电从天而降，劈到了{son_nickname}，但{son_nickname}掌握了雷电之法，驱散了闪电!")
                        return
                if judgement<80:  # 倒霉蛋被劈
                    await bot.set_group_ban(group_id=gid, user_id=son, duration=time)
                    await bot.send(ev, f"一道闪电从天而降，劈中了{son_nickname}!")
                    return
                elif judgement<90:  # 倒霉蛋被劈
                    await bot.set_group_ban(group_id=gid, user_id=son, duration=time)
                    try:
                        await bot.send(ev, f"一道闪电从天而降，{son_nickname}幸运地避开了!但是{MessageSegment.at(uid)}对其进行了改判,为♠{random.randrange(2, 10)}!")
                    except:
                        await bot.send(ev, f"一道闪电从天而降，{son_nickname}幸运地避开了!但是{user_info}对其进行了改判,为♠{random.randrange(2, 10)}!")
                    return
                else:  # 两个都被劈
                    if user_info['role'] == 'owner':
                        await bot.set_group_ban(group_id=gid, user_id=son, duration=time)
                        await bot.set_group_ban(group_id=gid, user_id=uid, duration=time * 2)
                        try:
                            await bot.send(ev, f"两道闪电从天而降，劈中了{MessageSegment.at(son)}的同时也劈中了{MessageSegment.at(uid)}!")
                        except:
                            await bot.send(ev, f"两道闪电从天而降，劈中了{son_nickname}的同时也劈中了{user_nickname}!")
                        return
                    else:
                        await bot.send(ev, f"一道闪电从天而降，劈到了{son_nickname}，但{son_nickname}竟拥有雷系属性，免疫了闪电!")
                        return
            else:  # 没劈到，无事发生
                judgement = random.randrange(101)
                if judgement<80:
                    await bot.send(ev, f"一道闪电从天而降，但是{son_nickname}幸运地避开了!")
                    return
                else:
                    son_2 = int(random.choice(member_list))
                    son_info_2 = await bot.get_group_member_info(user_id=son, group_id=gid, no_cache=True)
                    son_nickname_2 = son_info['nickname']
                    await bot.set_group_ban(group_id=gid, user_id=son, duration=time)
                    try:
                        await bot.send(ev, f"一道闪电从天而降，{son_nickname}幸运地避开了!{MessageSegment.at(uid)}对其进行了改判,但为{random.choice(judge_point)}!")
                    except:
                        await bot.send(ev, f"一道闪电从天而降，{son_nickname}幸运地避开了!{user_nickname}对其进行了改判,但为{random.choice(judge_point)}!")
                    return
        if son_role == 'admin':
            await bot.send(ev, f"一道闪电从天而降，但{son_nickname}以管理之力驱散了闪电!")
            return
        if son_role == 'owner':
            await bot.send(ev, f"一道闪电从天而降，但{son_nickname}以群主之力将闪电送回了天上!")
            freq.set_reload_group(group_id=gid, _time=_time * 5)
            return
    if role == 'owner':  # 冰祈是群主，乱杀
        judgement = random.randrange(101)
        if judgement<15:  # 触发者被劈
            await bot.set_group_ban(group_id=gid, user_id=uid, duration=time)
            try:
                await bot.send(ev, f"一道闪电从天而降，劈到了{son_nickname}，但{son_nickname}以一己之力将闪电送回了{MessageSegment.at(uid)}的身上!")
            except:
                await bot.send(ev, f"一道闪电从天而降，劈到了{son_nickname}，但{son_nickname}以一己之力将闪电送回了{user_nickname}的身上!")
            return
        if judgement<75:  # 倒霉蛋被劈
            await bot.set_group_ban(group_id=gid, user_id=son, duration=time)
            await bot.send(ev, f"一道闪电从天而降，劈中了{son_nickname}!")
            return
        elif judgement<85:  # 倒霉蛋被劈
            await bot.set_group_ban(group_id=gid, user_id=son, duration=time)
            try:
                await bot.send(ev, f"一道闪电从天而降，{son_nickname}幸运地避开了!但是{MessageSegment.at(uid)}对其进行了改判,为♠{random.randrange(2, 10)}!")
            except:
                await bot.send(ev, f"一道闪电从天而降，{son_nickname}幸运地避开了!但是{user_nickname}对其进行了改判,为♠{random.randrange(2, 10)}!")
            return
        else:  # 两个都被劈
            await bot.set_group_ban(group_id=gid, user_id=son, duration=time)
            await bot.set_group_ban(group_id=gid, user_id=uid, duration=time * 2)
            try:
                await bot.send(ev, f"两道闪电从天而降，劈中了{MessageSegment.at(son)}的同时也劈中了{MessageSegment.at(uid)}!")
            except:
                await bot.send(ev, f"两道闪电从天而降，劈中了{son_nickname}的同时也劈中了{user_nickname}!")
            return
