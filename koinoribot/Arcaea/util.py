from typing import Optional

import aiohttp
import os

import ujson

import hoshino
import time
from ..config import api_url, token

rootPath = os.path.dirname(__file__)

async def getArcInfo(
        url: str,
        params: Optional[dict] = None,
        need_token: bool = False,
        resp_type: str = 'json'):
    """
        从api处获取数据

    :param url: api地址
    :param params: 要发送的json数据
    :param need_token: 是否需要token
    :param resp_type: 预计返回的内容形式[json/byte]
    """
    header = {'Authorization': f'Bearer {token}'} if need_token else {}

    try:
        async with aiohttp.ClientSession(headers = header) as session:
            _params = params if params else {}
            async with session.get(url, params = _params) as r:
                if resp_type == 'json':
                    resp = await r.json()
                else:
                    resp = await r.read()
                return resp
    except Exception as e:
        hoshino.logger.error(f'Arcaea Unlimited Api出错：{e}')
        resp = {'status': -999, 'message': f'{e}'}
        return resp


def saveData(obj, fp):
    """
        保存文件
    """
    with open(fp, 'w', encoding='utf-8') as file:
        file.truncate(0)
        ujson.dump(obj, file, indent=2, ensure_ascii=False)


def loadData(fp):
    """
        加载json，不存在则创建
    """
    if os.path.exists(fp):
        file = ujson.load(open(fp, 'r', encoding='utf-8'))
        return file
    else:
        empty_dict = {}
        with open(fp, 'w', encoding='utf-8') as file:
            ujson.dump(empty_dict, file, indent=2, ensure_ascii=False)
        return empty_dict


def call_count(num: int):
    """
        调用量统计
    """
    countPath = os.path.join(rootPath, 'database/count.json')
    now = int(time.time())
    styled_time = timeTrans(now)
    if not os.path.exists(countPath):
        _dict = {styled_time: 1}
        with open(countPath, 'w', encoding='utf-8') as file:
            ujson.dump(_dict, file, indent=2, ensure_ascii=False)
    else:
        data = loadData(countPath)
        if styled_time not in data:
            data[styled_time] = 1
        else:
            data[styled_time] += 1
        saveData(data, countPath)


def clearType2icon(clear_type: int) -> str:
    """
        通关类型转换->图标
    """
    if clear_type == 0:
        return 'fail'
    if clear_type == 1:
        return 'normal'
    if clear_type == 2:
        return 'full'
    if clear_type == 3:
        return 'pure'
    if clear_type == 4:
        return 'easy'
    if clear_type == 5:
        return 'hard'


def clearType2bar(clear_type: int) -> str:
    """
        通关类型转换->图标
    """
    if clear_type == 0:
        return 'fail'
    elif clear_type in [1, 4, 5]:
        return 'normal'
    elif clear_type == 2:
        return 'full'
    elif clear_type == 3:
        return 'pure'
    else:
        return 'fail'


def score2icon(score: int) -> str:
    """
        得分转评级图标
    """
    if score >= 9900000:
        return 'explus'
    elif score >= 9800000:
        return 'ex'
    elif score >= 9500000:
        return 'aa'
    elif score >= 9200000:
        return 'a'
    elif score >= 8900000:
        return 'b'
    elif score >= 8600000:
        return 'c'
    else:
        return 'd'


def diffTrans(diff: int) -> str:
    """
        难度换算
    """
    if diff <= 18:
        return str(int(diff / 2))
    elif diff == 19:
        return '9+'
    elif diff == 20:
        return '10'
    elif diff == 21:
        return '10+'
    elif diff == 22:
        return '11'
    elif diff == 23:
        return '11+'
    elif diff == 24:
        return '12'
    else:
        return '?'


def ptt2icon(rating: int) -> str:
    if rating >= 1300:
        return 'rating_7'
    elif rating >= 1250:
        return 'rating_6'
    elif rating >= 1200:
        return 'rating_5'
    elif rating >= 1100:
        return 'rating_4'
    elif rating >= 1000:
        return 'rating_3'
    elif rating >= 700:
        return 'rating_2'
    elif rating >= 350:
        return 'rating_1'
    elif rating >= 0:
        return 'rating_0'
    else:
        return 'rating_off'


def timeTrans(_time):
    """
        输入时间戳，返回时间
    """
    #转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    timeArray = time.localtime(int(_time))
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
    return otherStyleTime


def extractItem(songlist: list, key: str):
    """
        从歌曲列表里提取特定键值对
    """
    _dict = {}
    for song in songlist:
        _list = []
        for i in range(len(song['difficulties'])):
            _list.append(song['difficulties'][i][key])
        _dict[song['song_id']] = _list
    saveData(_dict, os.path.join(rootPath, f'database/{key}_dict.json'))


def rating_standardization(rating: int):
    """
        定数规范化
    """
    standard_rating = list(str(rating))
    standard_rating.insert(-1, '.')
    standard_rating = ''.join(standard_rating)
    return standard_rating


if __name__ == '__main__':
    _path = os.path.join(rootPath, 'database/tempsonglist.json')
    songlist = list(loadData(_path))
    extractItem(songlist, 'difficulty')


