import asyncio
import os

import aiohttp
import requests

proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'https://127.0.0.1:7890'
}


api_url = 'https://netease-cloud-music-api-fader282.vercel.app/'
song_url = 'http://music.163.com/song/media/outer/url?id=.mp3'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42'
}


async def get_respond(url, json_format=True):
    response = requests.get(url=url, headers=headers)
    if json_format:
        return response.json()
    else:
        return response


async def get_song_result(keyword):
    """
        获取音乐详细信息
    """
    voice_url = api_url + f'cloudsearch?keywords={keyword}&type=1'
    content = await get_respond(voice_url)
    result = content['result']['songs']

    # result[num]['id']
    return result


async def get_song(song_id):
    song_url = f'http://music.163.com/song/media/outer/url?id={song_id}.mp3'
    async with aiohttp.ClientSession() as session:
        async with session.get(song_url, headers=headers) as r:
            content = await r.read()
            return content


def format_songlist(songlist: list):
    msg = ''
    for num in range(min(9, len(songlist))):
        msg += f"{num + 1}. {songlist[num]['name']} - {songlist[num]['ar'][0]['name']}\n"

    # result[num]['id']
    return msg.strip('\n')


if __name__ == '__main__':
    mp3_path = os.path.join(os.path.dirname(__file__), 'song.mp3')
    amr_path = os.path.join(os.path.dirname(__file__), 'output.amr')
    song_response = asyncio.get_event_loop().run_until_complete(get_song_result('clear morning'))
    format_resp = format_songlist(song_response)
    print(song_response)
    print(format_resp)