import os
import random
from hoshino import Service
import requests
from .._R import imgPath


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                  " AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/75.0.3770.142 Safari/537.36"
}

waifuUrl = 'https://www.thiswaifudoesnotexist.net/'
sv = Service('随机老婆头像', enable_on_default=True)


@sv.on_fullmatch('随机waifu')
async def random_waifu_generator(bot, ev):
    await bot.send(ev, '冰祈咏唱中...')
    rand_num = random.randint(1, 100000)
    image_name = 'example-%d.jpg' % rand_num
    file_name = os.path.join(imgPath, f'random_waifu/{image_name}')
    if not os.path.exists(file_name):
        img = requests.get(waifuUrl + image_name, timeout=6, headers=headers)
        with open(file_name, 'wb') as f:
            for chunk in img.iter_content(chunk_size=1024 ** 3):
                f.write(chunk)
    get_image = f'file:///{file_name}'
    await bot.send(ev, f'[CQ:image,file={get_image}]')
