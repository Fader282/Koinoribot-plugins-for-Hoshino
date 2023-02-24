from datetime import timedelta, datetime
import time

# 对群使用的冷却器，比较时间戳来判断是否冷却完成。

reload_group = {} # dict[group, time]

def set_reload_group(group_id, _time):
    reload_group[group_id] = time.time() + _time

def check_reload_group(group_id, _type = 'number'): # number返回剩余时长，boolean返回布尔表达式
    if group_id in reload_group and time.time() > reload_group[group_id]:
        del reload_group[group_id]  # 冷却时间过期
        if _type == 'boolean':
            return False
        else:
            return 0
    if _type == 'boolean':
        return bool(group_id in reload_group)
    else:
        remain = reload_group[group_id] - time.time()
        return round(int(remain))
'''
@sv.on_fullmatch('开始指令-text')
async def start_on_test(bot, ev):
    gid = ev.group_id
    if check_reload_group(gid, _type = 'boolean'):
        await bot.send(ev, f'冷却中...({check_reload_group(gid)}s)')
    else:
        set_reload_group(group_id = gid, _time = 30)
        await bot.send(ev, '该群冷却已开始！')
'''
