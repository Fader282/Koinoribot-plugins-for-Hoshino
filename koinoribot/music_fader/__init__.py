import asyncio
import os
from base64 import b64encode

import aiohttp
import requests

from nonebot import MessageSegment

from hoshino import Service
from ..config import proxies

api_url = 'https://netease-cloud-music-api-fader282.vercel.app/'
song_url = 'http://music.163.com/song/media/outer/url?id=.mp3'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42'
}


sv = Service('网易云音乐转音频', enable_on_default=True)


@sv.on_prefix('#amr')
async def get_netease_to_amr(bot, ev):
    mp3_path = os.path.join(os.path.dirname(__file__), f'{ev.user_id}.mp3')
    amr_path = os.path.join(os.path.dirname(__file__), f'{ev.user_id}.amr')
    message = ev.message.extract_plain_text()
    song_response = await get_song_result(message)
    result = song_response['result']
    songs = result['songs']
    song = songs[0]
    mp3_song = await get_song(song["id"], ev.user_id)
    audios = 'base64://' + b64encode(mp3_song).decode()
    await bot.send(ev, MessageSegment.record(audios))


async def get_respond(url, json_format=True):
    response = requests.get(url=url, headers=headers, proxies=proxies)
    if json_format:
        return response.json()
    else:
        return response


async def get_song_result(keyword):
    voice_url = api_url + f'cloudsearch?keywords={keyword}&type=1'
    content = await get_respond(voice_url)
    return content


async def get_song(song_id, name):
    song_url = f'http://music.163.com/song/media/outer/url?id={song_id}.mp3'
    async with aiohttp.ClientSession() as session:
        async with session.get(song_url, headers=headers) as r:
            content = await r.read()
            return content


if __name__ == '__main__':
    mp3_path = os.path.join(os.path.dirname(__file__), 'song.mp3')
    amr_path = os.path.join(os.path.dirname(__file__), 'output.amr')
    song_response = asyncio.get_event_loop().run_until_complete(get_song_result('clear morning'))
    result = song_response['result']
    songs = result['songs']
    print(songs)
    song = songs[0]
    print(song['id'])
    for i in songs[:10]:
        print(f'歌名:{i["name"]},ID:{i["id"]}, 歌手id:{i["ar"][0]["id"]}')
    asyncio.get_event_loop().run_until_complete(get_song(song["id"]))
    # asyncio.get_event_loop().run_until_complete(mp3_to_amr(mp3_path, amr_path))
