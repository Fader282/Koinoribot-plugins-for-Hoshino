import os

import openai
from ..config import OPEN_API, OPEN_ORG, proxies
from ..utils import loadData, saveData
from .._R import userPath
from hoshino import Service
from hoshino.config import SUPERUSERS
from .neko_mode import messages

sv = Service('ChatGPT-api版')

openai.api_key = OPEN_API
openai.organization = OPEN_ORG
openai.proxy = proxies
white_list_path = os.path.join(userPath, 'openai_api/whitelist.json')


@sv.on_prefix('#chat')
async def get_chat_response(bot, ev):
    white_list = loadData(white_list_path, is_list=True)
    if ev.group_id not in white_list:
        return
    message = ev.message.extract_plain_text().strip()
    if not message:
        return
    await bot.send(ev, '收到，正在呼叫chatGPT...')
    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": str(message)
                }
            ],
        )
        res_content = res.choices[0]['message']['content'].strip()
        await bot.send(ev, res_content, at_sender=True)
    except Exception as e:
        await bot.send(ev, '冰祈搞砸了，只带回来这个:' + str(e))


@sv.on_prefix('#nya')
async def chatgpt_catgirl_mode(bot, ev):
    white_list = loadData(white_list_path, is_list=True)
    if ev.group_id not in white_list:
        return
    message = ev.message.extract_plain_text().strip()
    if not message:
        return
    msg_list = []
    msg_list += messages
    msg_list.append({
        "role": "user",
        "content": str(message)
    })
    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=msg_list
        )
        res_content = res.choices[0]['message']['content'].strip()
        await bot.send(ev, res_content, at_sender=True)
    except Exception as e:
        await bot.send(ev, '冰祈搞砸了，只带回来这个:' + str(e))


@sv.on_prefix('chat添加白名单')
async def add_white_list_group(bot, ev):
    if ev.user_id not in SUPERUSERS:
        return
    message = ev.message.extract_plain_text().strip()
    if not str.isdigit(message):
        return
    group_id = int(message)
    white_list = loadData(white_list_path)
    if group_id not in white_list:
        white_list.append(group_id)
        saveData(white_list, white_list_path)
        await bot.send(ev, f'已将群{group_id}加入白名单')
    else:
        await bot.send(ev, f'群{group_id}已在白名单中')