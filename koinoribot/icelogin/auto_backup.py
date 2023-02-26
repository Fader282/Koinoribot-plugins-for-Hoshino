import os
import shutil

import time
from hoshino import Service
from hoshino.config import SUPERUSERS
from .._R import userPath

sv = Service('签到数据自动备份')

isOnChecking = False


@sv.scheduled_job('cron', hour=12)
async def auto_back_up_database():
    global isOnChecking
    if isOnChecking:
        return
    isOnChecking = True
    sv.logger.info('开始备份签到数据')
    backup_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    path = os.path.join(userPath, 'user_money.json')
    backup_path = os.path.join(userPath, f'icelogin/backup/user_money-{backup_time}.json')
    shutil.copyfile(path, backup_path)
    sv.logger.info('签到数据备份完成')
    isOnChecking = False


@sv.on_fullmatch('签到备份')
async def back_up_database(bot, ev):
    if ev.user_id not in SUPERUSERS:
        return
    try:
        backup_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        path = os.path.join(userPath, 'user_money.json')
        backup_path = os.path.join(userPath, f'icelogin/backup/user_money-{backup_time}.json')
        shutil.copyfile(path, backup_path)
        await bot.send(ev, 'ok')
    except Exception as e:
        await bot.send(ev, f'失败了:{e}')
