from base64 import b64encode

from nonebot import MessageSegment

import hoshino
from .._interact import ActSession, interact
from hoshino import Service
from .get_netease import get_song_result, get_song, format_songlist

sv = Service('网易云音乐转音频', enable_on_default=True)


@sv.on_prefix('#amr')
async def get_netease_to_amr(bot, ev):
    message = ev.message.extract_plain_text().strip()
    if not message:
        return
    if interact.find_session(ev, name='网抑云点歌'):  # 过期了就关闭
        session = interact.find_session(ev, name='网抑云点歌')
        if session.is_expire():
            session.close()
    session = ActSession.from_event('网抑云点歌', ev, max_user=1, usernum_limit=True, expire_time=120)
    try:
        interact.add_session(session)
    except ValueError:
        await bot.send(ev, '冰祈忙不过来QAQ')
        return
    try:
        song_response = await get_song_result(message)
        format_resp = format_songlist(song_response)
        await bot.send(ev, format_resp + '\n请发送"#+id"点歌~(如#1)')
    except Exception as e:
        hoshino.logger.error(f'点歌插件，在发送曲目列表环节出错：{e}， {str(e)}')
        session.close()
        return

    session.state['started'] = True
    session.state['songs'] = song_response


@sv.on_rex(r'(#|＃)(\d)')
async def choose_music_trigger(bot, ev):
    uid = ev.user_id
    evmatch = ev.match
    num = evmatch.group(2)
    num = int(num)
    if not num:
        return
    session = interact.find_session(ev, name='网抑云点歌')
    if not session:
        return
    if uid != session.creator:
        return
    songlist = session.state['songs']
    session.close()
    try:
        mp3_song = await get_song(songlist[num - 1]["id"])
        audios = 'base64://' + b64encode(mp3_song).decode()
        await bot.send(ev, MessageSegment.record(audios))
    except Exception as e:
        await bot.send(ev, '唱片走丢了...换一首好嘛？QAQ')
        hoshino.logger.error(f'网抑云点歌报错：{e}, {str(e)}')
