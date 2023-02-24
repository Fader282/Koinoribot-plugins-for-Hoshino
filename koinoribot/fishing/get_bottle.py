import os, random
from .util import shift_time_style
from ..utils import loadData, saveData, is_http_url, chain_reply
from .._R import userPath


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
        return None
    get_rand_id = random.choice(bottleId_list)
    sea[get_rand_id]['caught'] += 1
    bottle = sea[get_rand_id]
    if random.random() < (sea[get_rand_id]['caught'] / 10):
        del sea[get_rand_id]
    saveData(sea, sea_path)
    return bottle


async def format_message(bot, ev, bottle: dict):
    uid = bottle['uid']
    gid = bottle['gid']
    _time = shift_time_style(bottle['time'])
    caught = bottle['caught']
    content = bottle['content']
    chain = []
    await chain_reply(bot, ev, user_id=uid, chain=chain, msg=f'你捡到了我的漂流瓶~\n内容为：')
    await chain_reply(bot, ev, user_id=uid, chain=chain, msg=content)
    await chain_reply(bot, ev, user_id=uid, chain=chain, msg=f'投放地点(群聊)：{gid}\n投放时间：{_time}\n被捡起的次数：{caught}')
    return chain


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
    black_list = loadData(blacklist_path, is_list=True)
    uid = str(user_id)
    return bool(uid in black_list)


def add_to_blacklist(user_id):
    black_list = loadData(blacklist_path, is_list=True)
    uid = str(user_id)
    if uid not in black_list:
        black_list.append(uid)
        saveData(black_list, blacklist_path)


def remove_from_blacklist(user_id):
    black_list = loadData(blacklist_path, is_list=True)
    uid = str(user_id)
    if uid in black_list:
        black_list.remove(uid)
        saveData(black_list, blacklist_path)


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