import os, random

import hoshino
from .util import shift_time_style
from ..utils import loadData, saveData, is_http_url, chain_reply
from .._R import userPath
import time


dbPath = os.path.join(userPath, 'fishing/db')
sea_path = os.path.join(dbPath, 'sea.json')
count_path = os.path.join(dbPath, 'count.json')
blacklist_path = os.path.join(dbPath, 'black_list.json')


def set_bottle(user_id, group_id, time_stamp, content):
    """
        扔漂流瓶
    """
    sea = loadData(sea_path)
    count = loadData(count_path)
    if not count:
        count = {'count': 0}
    count['count'] += 1
    _id = count['count']
    bottle = {'uid': user_id, 'gid': group_id, 'time': time_stamp, 'caught': 0, 'content': content}
    sea[_id] = bottle
    saveData(sea, sea_path)
    saveData(count, count_path)
    return _id


def check_bottle():
    """
        捡漂流瓶
    """
    sea = loadData(sea_path)
    bottleId_list = list(sea.keys())
    if not bottleId_list:
        return None, None
    get_rand_id = random.choice(bottleId_list)
    hoshino.logger.info(f'捞起了{get_rand_id}号瓶子')
    sea[get_rand_id]['caught'] += 1
    bottle = sea[get_rand_id]
    if random.random() < (sea[get_rand_id]['caught'] / 20):
        del sea[get_rand_id]
    saveData(sea, sea_path)
    return bottle, get_rand_id


async def format_message(bot, ev, bottle: dict, bottle_id):
    """
        格式化漂流瓶内容(合并转发)
    """
    uid = bottle['uid']
    gid = bottle['gid']
    bid = bottle_id
    _time = shift_time_style(bottle['time'])
    caught = bottle['caught']
    content = bottle['content']
    chain = []
    await chain_reply(bot, ev, user_id=uid, chain=chain, msg=f'你捡到了我的漂流瓶~\n内容为：')
    await chain_reply(bot, ev, user_id=uid, chain=chain, msg=content)
    await chain_reply(bot, ev, user_id=uid, chain=chain, msg=f'漂流瓶id：{bid}\n投放地点(群聊)：{gid}\n投放时间：{_time}\n被捡起的次数：{caught}')
    return chain


def format_msg_no_forward(bot, ev, bottle: dict, bottle_id):
    """
        格式化漂流瓶内容(直接发送)
    """
    uid = bottle['uid']
    gid = bottle['gid']
    bid = bottle_id
    _time = shift_time_style(bottle['time'])
    caught = bottle['caught']
    content = bottle['content']
    msg = f'你捡到了{uid}的漂流瓶~\n投放时间：{_time}\n被捡起的次数：{caught}\n内容为：\n{content}'
    return msg


def delete_bottle(_id):
    _id = str(_id)
    sea = loadData(sea_path)
    bottleId_list = list(sea.keys())
    if _id not in bottleId_list:
        return '没有这个瓶子'
    del sea[_id]
    saveData(sea, sea_path)
    return '已成功移除该漂流瓶'


def check_permission(user_id):
    """
        检查是否在黑名单里，以及黑名单时长是否已到
    """
    cur_time = int(time.time())
    black_list = loadData(blacklist_path)
    uid = str(user_id)
    if uid in black_list.keys():
        if cur_time > black_list[uid]:
            del black_list[uid]
            saveData(black_list, blacklist_path)
            return False
        else:
            return True
    else:
        return False


def add_to_blacklist(user_id, _time: int = 86400):
    """
        添加用户至漂流瓶黑名单
        时长可选，默认为1天
    """
    black_list = loadData(blacklist_path)
    uid = str(user_id)
    cur_time = int(time.time())
    expire_time = cur_time + int(_time)
    black_list[uid] = expire_time
    saveData(black_list, blacklist_path)
    timeArray = time.localtime(expire_time)
    otherStyleTime = time.strftime("%m月%d日%H:%M:%S", timeArray)
    return f'已成功将{user_id}添加至黑名单，将于{otherStyleTime}解禁'


def remove_from_blacklist(user_id):
    """
        移除黑名单
    """
    black_list = loadData(blacklist_path)
    uid = str(user_id)
    if uid in black_list:
        del black_list[uid]
        saveData(black_list, blacklist_path)
        return f'已成功将{user_id}移除黑名单'
    else:
        return f'{user_id}不在黑名单里'


def show_blacklist():
    """
        列出黑名单
    """
    black_list = loadData(blacklist_path)
    msg = '黑名单列表：'
    msg2 = ''
    if len(black_list) == 0:
        msg += '\n大家都是好孩子！'
        return msg
    cur_time = int(time.time())
    for user, _time in black_list.items():
        timeArray = time.localtime(_time)
        if cur_time < _time:
            otherStyleTime = time.strftime("%m月%d日%H:%M:%S", timeArray)
            msg2 += f'\nQQ号：{user}\n解禁日期：{otherStyleTime}'
        else:
            continue
    if not msg2:
        msg += '\n大家都是好孩子！'
    else:
        msg += msg2
    return msg


def check_content(content: list):
    text = ''
    image = 0
    at = 0
    for i in content:
        if i['type'] == 'image':
            image += 1
        if i['type'] == 'text':
            text += i['data']['text']
        if i['type'] == 'at':
            at += 1
    if is_http_url(text):
        resp = {'code': -1, 'reason': '含有链接，不可以放进漂流瓶里...'}
    elif not text and image == 0:
        resp = {'code': -1, 'reason': '这是一个空漂流瓶喔...请装入要发送的内容，如：#扔漂流瓶 你好'}
    elif len(text) > 200:
        resp = {'code': -1, 'reason': '字数太多了，漂流瓶里放不下...'}
    elif image > 4:
        resp = {'code': -1, 'reason': '图片太多了，漂流瓶里放不下...'}
    elif at:
        resp = {'code': -1, 'reason': '艾特会在漂流瓶里挥发掉...'}
    else:
        resp = {'code': 1, 'reason': None}
    return resp


def get_bottle_amount():
    sea = loadData(sea_path)
    return len(list(sea.keys()))