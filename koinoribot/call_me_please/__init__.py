import json
import random

import hoshino
import re
from hoshino import Service, priv, util
import ujson
import os
from .util import *
from .._R import get, userPath

sv = Service('请叫我XXX', enable_on_default=True)
path = os.path.join(userPath, "call_me_please/nickname.json")
BANNED_WORD = (
    'rbq', 'RBQ', '憨批', '废物', '死妈', '崽种', '傻逼', '傻逼玩意', '贵物', '🐴',
    '没用东西', '傻B', '傻b', 'SB', 'sb', '煞笔', 'cnm', '爬', 'kkp', '你妈死了', '尼玛死了',
    'nmsl', 'D区', '口区', '我是你爹', 'nmbiss', '弱智', '给爷爬', '杂种爬', '爪巴', '冰祈'
)
random_string = 'ę‘†č„±ę‰€ę‰č¨·å…°ē„å¤§å˛‹å¤©äø»ę•™č‰ŗęÆē„ę¯ē¼ļ¼č¨·å…°äŗŗåÆ¹č‰ŗęÆē„é‰´čµ¸å›å¾—ä»�ę¸é«ć€‚é¸ē¯€č´øę“ē„å¸‘å±•å’ē»¸ęµˇē„ē¹č¨£ļ¼č¨·å…°čæˇę¯�äŗ†č‡Ŗå·±ē„ā€é»„é‡‘å¹´ä»£ā€¯ļ¼åę—¶å¼•čµ·äŗ†ę–‡å–ę„¸čÆ†ē„č§‰é†’å’č‡Ŗäæ�ē„é«ę¶Øć€‚ē„¶č€ļ¼å·´ę´›å…‹é£ˇę ¼ē„ē¹č¨£å’å¤©äø»ę•™ę•™ä¹‰ē„å­åØļ¼äøˇč‡Ŗę‘å¦å®å’č‚å¶ē„ę–°ę•™ē†č®ŗęŖē„¶äø¨åć€‚é™¤äŗ†å¸—å§”ę‰å›ä½č‚–å¸ē”»ä»�å¤–ļ¼č‰ŗęÆå®¶ä»¬å¹¶ę²�ę‰ēę­£ē„ē›®ē„ļ¼ä»–ä»¬ē„äø“äøå°ä½¨ä¹å²å²å¸Æå¨±ć€‚'
no = f"{get('emotion/no.png').cqcode}"
what = f"{get('emotion/问号.png').cqcode}"


@sv.on_suffix('请叫我', '叫我', '请喊我', '喊我', only_to_me=True)
@sv.on_prefix('请叫我', '叫我', '请喊我', '喊我', only_to_me=True)
async def call_me_new_name(bot, ev):
    message = ev.message.extract_plain_text().strip()
    if not message:
        return
    if ev.user_id == 80000000:
        await bot.send(ev, no)
        return
    lenTxt = len(message)
    lenTxt_utf8 = len(message.encode('utf-8'))
    size = int((lenTxt_utf8 - lenTxt)/2 + lenTxt)
    if size > 20:
        await bot.send(ev, f'名字太长，冰祈记不住..' + no)
        return
    for word in BANNED_WORD:
        if word in message:
            await bot.send(ev, f'不可以教坏冰祈..' + no)
            return
    user_dict = load_data(path)
    user_id = str(ev.user_id)
    user_dict = check_user(user_id, user_dict)
    user_dict[user_id]['self'] = message
    await bot.send(ev, f"好~")
    save_data(user_dict, path)


@sv.on_prefix('请叫他', '叫他', '冰祈请叫他', '请叫她', '叫她', '冰祈请叫她', '请叫它', '叫它', '冰祈请叫它')
async def call_ta_new_name(bot, ev):
    match = re.search(r'(?:\[CQ:at,qq=(\d+|all)\])', ev.raw_message)
    user_id = match.group(1)  # 这里的user_id是被艾特人的qq号，报错则可能没有at到
    if user_id == 'all':
        await bot.send(ev, f'不可以随意艾特全体成员喔' + what)
        return
    user_id = int(user_id)
    if user_id == 80000000:
        await bot.send(ev, no)
        return
    message = ev.message.extract_plain_text().strip()
    if not message:
        return
    lenTxt = len(message)
    lenTxt_utf8 = len(message.encode('utf-8'))
    size = int((lenTxt_utf8 - lenTxt)/2 + lenTxt)
    if user_id == ev.self_id:
        await bot.send(ev, f'冰祈就是冰祈喔' + what)
        return
    if size > 20:
        await bot.send(ev, f'名字太长，冰祈记不住..' + no)
        return
    for word in BANNED_WORD:
        if word in message:
            await bot.send(ev, f'不可以教坏冰祈..' + no)
            return
    user_dict = load_data(path)
    user_dict = check_user(str(user_id), user_dict)
    if not user_dict[str(user_id)]['switch']:
        await bot.send(ev, '不可以改TA的昵称..' + no)
        return
    if user_dict[str(user_id)]['self']:
        await bot.send(ev, 'TA已经有昵称了~')
        return
    user_dict[str(user_id)]['other'] = message
    await bot.send(ev, f"好~")
    save_data(user_dict, path)


@sv.on_rex(r'(清除|删除)(昵称)')
async def dont_call_me(bot, ev):
    if ev.user_id == 80000000:
        await bot.send(ev, no)
        return
    user_dict = load_data(path)
    user_id = str(ev.user_id)
    user_dict = check_user(user_id, user_dict)
    user_dict[user_id]['other'] = ''
    user_dict[user_id]['self'] = ''
    await bot.send(ev, '已恢复称呼~')
    save_data(user_dict, path)


@sv.on_rex(r'(禁止|允许)(被动改名)')
async def call_me_switch(bot, ev):
    if ev.user_id == 80000000:
        await bot.send(ev, no)
        return
    match = ev['match']
    match_obj = str(match.group(1))
    user_dict = load_data(path)
    user_id = str(ev.user_id)
    user_dict = check_user(user_id, user_dict)
    if match_obj == '禁止':
        user_dict[user_id]['switch'] = 0
    elif match_obj == '允许':
        user_dict[user_id]['switch'] = 1
    await bot.send(ev, '好~')
    save_data(user_dict, path)


@sv.on_rex(r'(.+)?(冰祈)?(我)(是)(谁|哪个|哪位|什么|啥)(.+)?')
async def call_me_now(bot, ev):
    if ev.user_id == 80000000:
        sample_num = random.randint(5, 11)
        sp_name = ''.join(random.sample(random_string, sample_num))
        await bot.send(ev, sp_name)
        return
    user_dict = load_data(path)
    user_id = str(ev.user_id)
    user_dict = check_user(user_id, user_dict)
    if user_dict[user_id]['self']:
        name = user_dict[user_id]['self']
    elif user_dict[user_id]['other']:
        name = user_dict[user_id]['other']
    else:
        name = ev.sender['nickname']
    await bot.send(ev, f'是{name}~')
    save_data(user_dict, path)


@sv.on_rex(r'(.+)?(冰祈)?(他|它|她|TA|你)(是)(谁|哪个|哪位|什么|啥)(.+)?')
async def call_ta_now(bot, ev):
    user_dict = load_data(path)
    match = re.search(r'(?:\[CQ:at,qq=(\d+|all)\])', ev.raw_message)
    user_id = match.group(1)  # 这里的user_id是被艾特人的qq号，报错则可能没有艾特到
    if not user_id:
        return
    if user_id == 'all':
        await bot.send(ev, f'不可以随意艾特全体成员喔' + what)
        return
    if int(user_id) == ev.self_id:
        await bot.send(ev, f'是冰祈~')
        return
    if int(user_id) == 80000000:
        sample_num = random.randint(5, 11)
        sp_name = ''.join(random.sample(random_string, sample_num))
        await bot.send(ev, sp_name)
        return
    user_dict = check_user(user_id, user_dict)
    if user_dict[user_id]['self']:
        name = user_dict[user_id]['self']
    elif user_dict[user_id]['other']:
        name = user_dict[user_id]['other']
    else:
        strange_info = await bot.get_stranger_info(user_id = user_id, no_cache = True)
        name = strange_info['nickname']
    await bot.send(ev, f'是{name}~')
    save_data(user_dict, path)
