import io
import os
import random

import time

from ..build_image import BuildImage
from hoshino import Service
from hoshino.config import SUPERUSERS
from .draw_image import getOneRecord, get30Record
from .util import timeTrans, rating_standardization, loadData, saveData
from .get_info import dbPath, songName2Id, getSongPreview, updateSonglist
from .._R import get, userPath

no = get('emotion/no.png').cqcode
ok = get('emotion/ok.png').cqcode
hundao = get('emotion/昏倒.jpg').cqcode
userCodePath = os.path.join(userPath, 'Arcaea/user_code.json')
rating_dict = loadData(os.path.join(dbPath, 'rating_dict.json'))
songname_dict = loadData(os.path.join(dbPath, 'name_en_dict.json'))
poke_back = ['戳_白.jpg', '戳_混合.jpg', '戳_混合_bb.jpg', '戳_混合_wb.jpg', '戳_混合_ww.jpg',
             '戳_黑.jpg', '戳_混合_R.jpg', '戳_混合_Rbb.jpg', '戳_混合_Rwb.jpg', '戳_混合_Rww.jpg',
             '戳_黑.jpg', '戳_白.jpg', '戳_白.jpg', '戳_黑.jpg', '戳_白.jpg', '戳_黑.jpg']

sv = Service('Arcaea音游插件')


@sv.on_prefix('#a bind')
async def bind_user_code(bot, ev):
    message = ev.message.extract_plain_text().strip()
    if not str.isdigit(message) or len(message) < 9:
        await bot.send(ev, '需要9位好友码才可以绑定' + no)
        return
    user_code_dict = loadData(userCodePath)
    uid = str(ev.user_id)
    if uid not in user_code_dict:
        user_code_dict[uid] = {'user_code': message, 'is_hide': 0}
    else:
        user_code_dict[uid]['user_code'] = message
    saveData(user_code_dict, userCodePath)
    await bot.send(ev, ok)


@sv.on_rex(r'(#a )(hide|show)')
async def hide_user_information(bot, ev):
    match = ev['match']
    match_obj = match.group(2)
    uid = str(ev.user_id)
    user_code_dict = loadData(userCodePath)
    if uid not in user_code_dict:
        await bot.send(ev, '需要先使用"#a bind 好友码"绑定喔' + no)
        return
    if match_obj == 'hide':
        user_code_dict[uid]['is_hide'] = 1
    elif match_obj == 'show':
        user_code_dict[uid]['is_hide'] = 0
    else:
        return
    saveData(user_code_dict, userCodePath)
    await bot.send(ev, ok)


@sv.on_fullmatch('#a r', '#arc recent')
async def get_recent_record(bot, ev):
    uid = str(ev.user_id)
    user_code_dict = loadData(userCodePath)
    if uid not in user_code_dict:
        await bot.send(ev, '需要先使用"#a bind 好友码"绑定喔' + no)
        return
    user_code = user_code_dict[uid]['user_code']
    is_hide = int(user_code_dict[uid]['is_hide'])
    await bot.send(ev, '冰祈咏唱中...')
    resp = await getOneRecord(user_code, is_hide=is_hide)
    await bot.send(ev, resp)


@sv.on_prefix('#a b ', '#a best ')
async def get_best_record(bot, ev):
    uid = str(ev.user_id)
    user_code_dict = loadData(userCodePath)
    if uid not in user_code_dict:
        await bot.send(ev, '需要先使用"#a bind 好友码"绑定喔' + no)
        return
    message = ev.message.extract_plain_text().strip()
    if not message:
        return
    if '#' in message:
        name_and_diff = message.split('#')
    else:
        name_and_diff = [message, 'ftr']
    song_id = songName2Id(name_and_diff[0])
    if not song_id:
        await bot.send(ev, '没有找到这首歌...' + hundao)
        return
    user_code = int(user_code_dict[uid]['user_code'])
    is_hide = int(user_code_dict[uid]['is_hide'])
    await bot.send(ev, '冰祈咏唱中...')
    resp = await getOneRecord(user = user_code, mode = 'best', is_hide=is_hide, song_id=song_id, difficulty=name_and_diff[-1])
    await bot.send(ev, resp)


@sv.on_fullmatch('#a b30', '#a best30')
async def user_best30_records(bot, ev):
    uid = str(ev.user_id)
    user_code_dict = loadData(userCodePath)
    if uid not in user_code_dict:
        await bot.send(ev, '需要先使用"#a bind 好友码"绑定喔' + no)
        return
    user_code = int(user_code_dict[uid]['user_code'])
    is_hide = int(user_code_dict[uid]['is_hide'])
    await bot.send(ev, '可能需要较长时间，冰祈蓄力咏唱中...')
    resp = await get30Record(user = user_code, is_hide=is_hide)
    await bot.send(ev, resp)


@sv.on_fullmatch('#a b40','#a best40')
async def user_best40_records(bot, ev):
    uid = str(ev.user_id)
    user_code_dict = loadData(userCodePath)
    if uid not in user_code_dict:
        await bot.send(ev, '需要先使用"#a bind 好友码"绑定喔' + no)
        return
    user_code = int(user_code_dict[uid]['user_code'])
    is_hide = int(user_code_dict[uid]['is_hide'])
    await bot.send(ev, '可能需要较长时间，冰祈蓄力咏唱中...')
    resp = await get30Record(user = user_code, is_hide=is_hide, is_b40=True)
    await bot.send(ev, resp)


@sv.on_fullmatch('#a 调用量')
async def call_count_statistics(bot, ev):
    if ev.user_id != SUPERUSERS[0]:
        return
    call_count_data = loadData(os.path.join(dbPath, 'count.json'))
    now = timeTrans(time.time())
    if now not in call_count_data:
        await bot.send(ev, '今天还没有人调用过AUA')
        return
    _call_count = call_count_data[now]
    await bot.send(ev, f'今日AUA调用量：{_call_count}')


@sv.on_rex(r'(#a choice)( )?(.+)?')
async def random_choice_song(bot, ev):
    match = ev.match
    match_obj = match.group(3)
    diff_flag = -1
    level_flag = 0
    songname_dict = loadData(os.path.join(dbPath, 'name_en_dict.json'))
    diff_list = ['past', 'present', 'future', 'beyond']
    if not match_obj:
        songid_list = list(rating_dict.keys())
        random_songid = random.choice(songid_list)
        random_diff = random.randint(0, len(rating_dict[random_songid]) - 1)
        random_rating = rating_dict[random_songid][random_diff]
        rating = list(str(random_rating))
        rating.insert(-1, '.')
        rating = ''.join(rating)
        song_name = songname_dict[random_songid][0]
        await bot.send(ev, f'冰祈选择的曲目：{song_name}\n难度：{diff_list[random_diff]}\n定数：{rating}')
        return
    match_obj = match_obj.strip()
    if match_obj in ['pst', 'past']:
        diff_flag = 0
    elif match_obj in ['prs', 'present']:
        diff_flag = 1
    elif match_obj in ['ftr', 'future']:
        diff_flag = 2
    elif match_obj in ['byd', 'byn', 'beyond']:
        diff_flag = 3
    elif str(match_obj) in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']:
        level_flag = int(match_obj) * 2
    elif match_obj == '9+':
        level_flag = 19
    elif match_obj == '10+':
        level_flag = 21
    elif str(match_obj) == '12':
        expression_pic = get(f'poke_emo/{random.choice(poke_back)}').cqcode
        await bot.send(ev, '你莫得选择' + expression_pic)
        return
    else:
        await bot.send(ev, '没有这种难度' + no)
        return

    if 0 < diff_flag < 3:
        songid_list = list(rating_dict.keys())
        random_songid = random.choice(songid_list)
        random_rating = rating_dict[random_songid][diff_flag]
        rating = rating_standardization(random_rating)
        song_name = songname_dict[random_songid][0]
        await bot.send(ev, f'冰祈选择的曲目：{song_name}\n难度：{diff_list[diff_flag]}\n定数：{rating}')
        return
    if diff_flag == 3:
        bydlist = loadData(os.path.join(dbPath, 'byd_list.json'))
        random_songid = random.choice(bydlist)
        random_rating = rating_dict[random_songid][3]
        rating = rating_standardization(random_rating)
        song_name = songname_dict[random_songid][0]
        await bot.send(ev, f'冰祈选择的曲目：{song_name}\n难度：{diff_list[diff_flag]}\n定数：{rating}')
        return

    if level_flag > 0:
        difficulty_list = loadData(os.path.join(dbPath, 'difficulty_dict.json'))
        song_list = []
        for i, j in difficulty_list.items():
            print(j)
            if level_flag in j:
                _diff = j.index(level_flag)
                song_list.append((i, _diff))
        random_song = random.choice(song_list)
        song_id = random_song[0]
        song_diff = random_song[-1]
        song_rating = rating_dict[song_id][song_diff]
        rating = rating_standardization(song_rating)
        song_name = songname_dict[song_id][0]
        await bot.send(ev, f'冰祈选择的曲目：{song_name}\n难度：{diff_list[song_diff]}\n定数：{rating}')


@sv.on_prefix('#a ra')
async def get_song_rating(bot, ev):
    message = ev.message.extract_plain_text().strip()
    if not message:
        return
    song_id = songName2Id(message)
    song_name = songname_dict[song_id][0]
    song_rating_list = rating_dict[song_id]
    msg = f'歌曲 {song_name} 定数:\npst: {rating_standardization(song_rating_list[0])}\nprs: {rating_standardization(song_rating_list[1])}\nftr: {rating_standardization(song_rating_list[2])}'
    if len(song_rating_list) == 4:
        msg += f'\nbyd: {rating_standardization(song_rating_list[3])}'
    await bot.send(ev, msg)


@sv.on_prefix('#a chart')
@sv.on_prefix('#a prev')
async def get_song_preview(bot, ev):
    message = ev.message.extract_plain_text().strip()
    _list = message.split('#')
    songname = _list[0].strip()
    if not songname:
        return
    if len(_list) == 1:
        difficulty = 'ftr'
    else:
        difficulty = _list[-1]
    song_id = songName2Id(songname)
    if not song_id:
        await bot.send(ev, '没有找到这首歌...' + hundao)
        return
    await bot.send(ev, '冰祈咏唱中...')
    response = await getSongPreview(song_id=song_id, difficulty=difficulty)
    prev_pic = BuildImage(0, 0, background=io.BytesIO(response))
    imageToSend = f"[CQ:image,file=base64://{prev_pic.pic2bs4()}]"
    await bot.send(ev, imageToSend)


@sv.on_fullmatch('#a 更新')
async def update_arcaea_prober(bot, ev):
    await bot.send(ev, '正在更新中，请稍等...')
    await updateSonglist()
    await bot.send(ev, '更新已完成~')


