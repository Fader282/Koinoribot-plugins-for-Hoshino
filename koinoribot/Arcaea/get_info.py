import asyncio
import os
from typing import Union, Optional

from fuzzywuzzy import process

from .util import rootPath, loadData, saveData, extractItem, getArcInfo
from .._R import imgPath
from ..config import api_url
import ujson

dbPath = os.path.join(rootPath, 'database')
srcPath = os.path.join(imgPath, 'Arcaea/src')
iconPath = os.path.join(srcPath, 'icons')
portraitPath = os.path.join(srcPath, 'portraits')
songPath = os.path.join(srcPath, 'songs')
layoutsPath = os.path.join(srcPath, 'layouts')


def songName2Id(song_name: str):
    """
        曲名转曲ID
    """
    songid = ''
    most_fit_name = ''
    fit_rate = 0
    songlist = loadData(os.path.join(dbPath, 'tempsonglist.json'))
    for song in songlist:
        name_list = list(song['alias'])
        name_list.append(song['difficulties'][0]['name_en'])
        name_list.append(song['difficulties'][0]['name_jp'])
        if song_name in name_list:
            songid = song['song_id']
            return songid
        else:
            song_id = process.extractOne(song_name, name_list)
            if song_id[-1] > fit_rate:
                most_fit_name = song['song_id']
                fit_rate = song_id[-1]
    return most_fit_name


def getSongInfo(song_id: str):
    """
        获取歌曲信息

        song_id: 曲目id
    """
    song_info = ''
    songlist = loadData(os.path.join(dbPath, 'tempsonglist.json'))
    for song in songlist:
        song = dict(song)
        if song['song_id'] == song_id:
            song_info = song
            break
    return song_info


async def updateSonglist():
    """
        更新歌曲缓存（不要频繁使用）

    :return: 返回状态码
    """
    url = api_url + 'song/list'
    resp = await getArcInfo(url)
    if resp['status'] == 0:
        song_list = list(resp['content']['songs'])
        saveData(song_list, os.path.join(dbPath, 'tempsonglist.json'))
        extractItem(song_list, 'side')
        extractItem(song_list, 'rating')
        extractItem(song_list, 'name_en')
        extractItem(song_list, 'difficulty')
        updateBydList()

        return 0
    else:
        return resp['status']


def updateBydList():
    file = ujson.load(open(os.path.join(os.path.dirname(__file__), 'database/rating_dict.json'), 'r', encoding='utf-8'))

    byd_list = []

    for i, j in file.items():
        if len(j) == 4:
            byd_list.append(i)

    with open(os.path.join(os.path.dirname(__file__), 'database/byd_list.json'), 'w', encoding='utf-8') as f:
        ujson.dump(byd_list, f, ensure_ascii=False)


async def getIcon(partner: int):
    """
        获取搭档图标（不要频繁使用）

    :param partner: 搭档的id
    :return: 返回图片路径
    """
    icon_path = os.path.join(iconPath, f'{partner}.png')
    if not os.path.exists(icon_path):
        url = api_url + 'assets/icon'
        params = {
            'partner': partner
        }
        resp = await getArcInfo(url, params, resp_type='byte')
        with open(os.path.join(icon_path), 'wb') as file:
            file.write(resp)
    return {'status': 0, 'message': icon_path}


async def getPortrait(partner: int):
    """
        获取搭档立绘（不要频繁使用）

    :param partner: 搭档的id
    :return: 返回图片路径
    """
    portrait_path = os.path.join(portraitPath, f'{partner}.png')
    if not os.path.exists(portrait_path):
        url = api_url + 'assets/char'
        params = {
            'partner': partner
        }
        resp = await getArcInfo(url, params, resp_type='byte')
        with open(os.path.join(portrait_path), 'wb') as file:
            file.write(resp)
    return {'status': 0, 'message': portrait_path}


async def getSongPic(song_id: str, difficulty: int = 2):
    """
        获取曲绘（不要频繁使用）

    :param song_id: 曲子的id
    :param difficulty: 难度，默认2 (ftr)，限定数字
    :return: 返回图片路径
    """
    difflist = ['0', '1', 'base', '3']
    song_pic_path = os.path.join(songPath, f'{song_id}/{difflist[difficulty]}.jpg')
    if not os.path.exists(os.path.join(songPath, song_id)):
        os.mkdir(os.path.join(songPath, song_id))

    if os.path.exists(os.path.join(songPath, f'{song_id}/{difflist[difficulty]}.jpg')):
        return {'status': 0, 'message': song_pic_path}
    else:
        url = api_url + 'assets/song'
        params = {
            'songid': song_id,
            'difficulty': difficulty
        }
        resp = await getArcInfo(url, params, resp_type='byte')
        with open(os.path.join(song_pic_path), 'wb') as file:
            file.write(resp)
    return {'status': 0, 'message': song_pic_path}


async def getUserInfo(
        user: Union[str, int],
        recent: Optional[int] = None,
        with_song_info: Optional[str] = 'false'):
    """
        获取玩家信息

    :param user: 玩家名称(str)，或玩家好友码(int)
    :param recent: 是否返回最近游玩成绩，范围0-7
    :param with_song_info: 是否返回最近游玩的歌曲信息[true/false]，数量由recent决定
    :return: 返回玩家的json数据
    """
    params = {
        'user': user
    }
    if recent:
        params['recent'] = recent
    if with_song_info:
        params['withsonginfo'] = with_song_info
    url = api_url + 'user/info'
    response = await getArcInfo(url = url, params = params, need_token = True)
    return response


async def getUserBest(
        user: Union[str, int],
        song: str,
        difficulty: Union[str, int] = 'ftr',
        with_recent: Optional[str] = None,
        with_song_info: Optional[str] = None):
    """
        获取用户某首歌成绩
    :param user: 玩家名称(str)，或玩家好友码(int, str)
    :param song: 曲id
    :param difficulty: 难度[0/1/2/3][pst/prs/ftr/byd]
    :param with_recent: 是否返回最近游玩该曲成绩[true/false]
    :param with_song_info: 是否返回曲目信息[true/false]
    """
    params = {
        'user': user,
        'songname': song,
        'difficulty': difficulty
    }
    if with_recent:
        params['withrecent'] = with_recent
    if with_song_info:
        params['withsonginfo'] = with_song_info

    url = api_url + 'user/best'

    response = await getArcInfo(url, params=params, need_token = True)
    return response


async def getUserBest30(
        user: Union[str, int],
        overflow: Optional[int] = 0,
        with_recent: Optional[str] = None,
        with_song_info: Optional[str] = None):
    """
        获取用户best30成绩
    :param user: 玩家名称(str)，或玩家好友码(int)
    :param overflow: 延申查询成绩数量，范围0-10
    :param with_recent: 是否返回最近游玩该曲成绩[true/false]
    :param with_song_info: 是否返回曲目信息[true/false]
    """
    params = {
        'user': user
    }
    if overflow:
        params['overflow'] = overflow
    if with_recent:
        params['withrecent'] = with_recent
    if with_song_info:
        params['withsonginfo'] = with_song_info

    url = api_url + 'user/best30'

    resp = await getArcInfo(url, params, need_token = True)
    return resp


async def getSongPreview(song_id: str,
                         difficulty: Optional[Union[int, str]]):
    """
        获取谱面预览

    :param song_id: 曲id
    :param difficulty: 难度，支持0/pst/past
    """
    params = {
        'songid': song_id
    }
    if difficulty:
        params['difficulty'] = difficulty

    url = api_url + 'assets/preview'
    resp = await getArcInfo(url, params, resp_type = 'byte', need_token = True)
    return resp


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    #name = songName2Id('最强')
    #print(name)
    #result = loop.run_until_complete(SongName2Id('病女'))
    result = loop.run_until_complete(
        getSongPic(song_id='山茶花', difficulty=2))
    #saveData(result, os.path.join(rootPath, 'user_best_30.json'))
    print(result)
    # \xff\xd8\xff\xe1\x14\xd4Exif\x00\x00MM\x00*\x00\x00\x00\x08\x00
