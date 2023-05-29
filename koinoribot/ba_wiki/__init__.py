import os
from base64 import b64encode
from nonebot import MessageSegment

import hoshino
from hoshino import Service, priv
from hoshino.config import NICKNAME, SUPERUSERS
from hoshino.util import FreqLimiter
from .student_info import *
from .get_gacha import increase_value, check_mode, get_10_gacha, get_1_gacha, change_mode, gachaPath, studentPath
from .._R import get
from .boss_info import get_boss_info, get_difficulty_id, get_boss_raids_id


sv = Service('碧蓝档案学生wiki')

nick_dict_path = os.path.join(os.path.dirname(__file__), 'db/students_nickname.json')
user_dict_path = os.path.join(os.path.dirname(__file__), 'gacha/userdata.json')
gacha_pool_path = os.path.join(os.path.dirname(__file__), 'db/gacha.json')
boss_nick_dict = json.load(open(os.path.join(os.path.dirname(__file__), 'db/boss_nickname.json'), encoding='utf-8'))
boss_nick_list = []
for i, j in boss_nick_dict.items():
    boss_nick_list = boss_nick_list + j[:]

sorry = get('emotion/shiro_gomen.png').cqcode
pardon = get('emotion/问号.png').cqcode
no = get('emotion/no.png').cqcode
ok = get('emotion/ok.png').cqcode

flmt = FreqLimiter(5)

if not NICKNAME:
    NICKNAME = '阿罗娜'

@sv.on_prefix('档案查询', 'bacx', 'dacx')
async def send_student_info(bot, ev):
    nickname = ev.message.extract_plain_text().strip()
    if not nickname:
        return
    if nickname in boss_nick_list:
        await bot.send(ev, '总力战boss请使用boss查询...' + no)
        return
    _student_id = get_student_id(nickname)
    uid = ev.user_id
    if not priv.check_priv(ev, priv.SUPERUSER):
        if not flmt.check(uid):
            await bot.send(ev, f'请让冰祈休息一下QAQ...({round(flmt.left_time(uid))}s)')
            return
    if str.isdigit(str(_student_id)):
        await bot.send(ev, '正在制作卡片中，请耐心等待~')
        student_card, audio_name, introduction = get_student_info(_student_id)
    else:
        if _student_id[0]:
            await bot.send(ev, f"没有找到这名学生..是在找{_student_id[0]}嘛？" + pardon)
        else:
            await bot.send(ev, f"没有找到这名学生.." + sorry)
        return

    # 卡片
    # 描述
    student_list = json.load(open(os.path.join(database_path, 'students_nickname.json'), encoding="utf-8"))["CHARA_NAME"]
    student_name = f"查询关键词：{'、'.join(student_list[str(_student_id)])}"
    try:
        chain = []
        await chain_reply(bot, ev, chain, student_card)
        await chain_reply(bot, ev, chain, introduction)
        await chain_reply(bot, ev, chain, student_name)
        await bot.send_group_forward_msg(group_id=ev.group_id, messages=chain)
    except Exception as e:
        hoshino.logger.error(f"碧蓝档案wiki,合并转发消息失败：{e}")
        await bot.send(ev, student_card)
    
    flmt.start_cd(uid)


@sv.on_prefix('boss查询')
async def send_boss_info(bot, ev):
    message = ev.message.extract_plain_text().strip()
    if not message:
        await bot.send(ev, '可以查的boss：大蛇/球/黑白/主教/高达/鸡斯拉/hod/goz\n可以用的难度：nm/hd/vh/hc/ex/ins/tm\n如：boss查询 主教 ex')
        return
    boss_and_difficulty = message.split(' ')
    if len(boss_and_difficulty) < 2:
        await bot.send(ev, '这样用喔：boss查询 boss 难度(如：boss查询 Binah hc)')
        return
    boss_raid_id = get_boss_raids_id(boss_and_difficulty[0])
    difficulty_id = get_difficulty_id(boss_and_difficulty[-1])
    if not boss_raid_id:
        await bot.send(ev, '没有这个boss喔...可以用的关键词：大蛇/球/黑白/主教/高达/鸡斯拉/hod/goz')
        return
    if not difficulty_id:
        await bot.send(ev, '没有这个难度喔...可以用的关键词：nm/hd/vh/hc/ex/ins/tm')
        return
    await bot.send(ev, '正在制作boss卡片中，请耐心等待~')
    imageToSend, bossBgm, bossProfile = get_boss_info(boss_raid_id, difficulty_id)
    if imageToSend == '没有这个难度喔..':
        await bot.send(ev, imageToSend + no)
        return
    boss_list = json.load(open(os.path.join(database_path, 'boss_nickname.json'), encoding="utf-8"))
    boss_name = f"查询关键词：{'、'.join(boss_list[str(boss_raid_id)])}"
    try:
        chain = []
        await chain_reply(bot, ev, chain, imageToSend)
        await chain_reply(bot, ev, chain, bossProfile)
        await chain_reply(bot, ev, chain, boss_name)
        await bot.send_group_forward_msg(group_id=ev.group_id, messages=chain)
    except Exception as e:
        hoshino.logger.error(f"碧蓝档案wiki,合并转发消息失败：{e}")
        await bot.send(ev, imageToSend)
    

@sv.on_prefix('技能查询', 'jncx')
async def send_skill_info(bot, ev):
    uid = ev.user_id
    nickname = ev.message.extract_plain_text()
    _student_id = get_student_id(nickname)
    if not nickname:
        return
    if not priv.check_priv(ev, priv.SUPERUSER):
        if not flmt.check(uid):
            await bot.send(ev, f'请让冰祈休息一下QAQ...({round(flmt.left_time(uid))}s)')
            return
    if str.isdigit(str(_student_id)):
        await bot.send(ev, '正在制作卡片中，请耐心等待~')
        student_card, weapon_desc, favoritem_desc = get_skill_info(_student_id)
    else:
        if _student_id[0]:
            await bot.send(ev, f"没有找到这名学生..是在找{_student_id[0]}嘛？" + pardon)
        else:
            await bot.send(ev, f"没有找到这名学生.." + sorry)
        return
    try:
        chain = []
        await chain_reply(bot, ev, chain, student_card)
        await chain_reply(bot, ev, chain, weapon_desc)
        if favoritem_desc:
            await chain_reply(bot, ev, chain, favoritem_desc)
        await bot.send_group_forward_msg(group_id=ev.group_id, messages=chain)
        flmt.start_cd(uid)
    except Exception as e:
        hoshino.logger.error(f"碧蓝档案wiki,合并转发消息失败：{e}")
        await bot.send(ev, student_card)


@sv.on_prefix('材料查询', 'clcx')
async def send_material_info(bot, ev):
    uid = ev.user_id
    nickname = ev.message.extract_plain_text()
    if not nickname:
        return
    if not priv.check_priv(ev, priv.SUPERUSER):
        if not flmt.check(uid):
            await bot.send(ev, f'请让冰祈休息一下QAQ...({round(flmt.left_time(uid))}s)')
            return
    _student_id = get_student_id(nickname)
    if str.isdigit(str(_student_id)):
        await bot.send(ev, '正在制作卡片中，请耐心等待~')
        material_card = get_material_info(_student_id)
    else:
        if _student_id[0]:
            await bot.send(ev, f"没有找到这名学生..是在找{_student_id[0]}嘛？" + pardon)
        else:
            await bot.send(ev, f"没有找到这名学生.." + sorry)
        return
    await bot.send(ev, material_card)


@sv.on_fullmatch('学生列表', 'xslb')
async def student_nickname(bot, ev):
    student_list = json.load(open(os.path.join(database_path, 'students_nickname.json'), encoding="utf-8"))[
        "CHARA_NAME"]
    msg = ''
    i = 0
    if not os.path.exists(os.path.join(database_path, 'update.json')):
        with open(os.path.join(database_path, 'update.json'), 'w', encoding='utf-8') as f:
            temp = {'content': ''}
            json.dump(temp, f, ensure_ascii=False, indent=2)
    update_msg = json.load(open(os.path.join(database_path, 'update.json'), 'r', encoding='utf-8'))['content']
    msglist = [update_msg]
    for name_list in student_list.values():
        name = name_list[1:3]
        msg += '、'.join(name)
        msg += '\n'
        i += 1
        if i>=10:
            msglist.append(msg)
            i = 0
            msg = ''
    chain = []
    for msg in msglist:
        node = {
            "type": "node",
            "data": {
                "name": str(NICKNAME),
                "uin": str(ev.self_id),
                "content": [
                    {
                        "type": "text",
                        "data": {
                            "text": msg}}]}
        }
        chain.append(node)
    await bot.send_group_forward_msg(group_id=ev['group_id'], messages=chain)


@sv.on_prefix('#buy')
async def buy_stone(bot, ev):
    message = ev.message.extract_plain_text().strip()
    if not message:
        return
    if not str.isdigit(message):
        await bot.send(ev, no)
        return
    for i in ['114514', '1919810']:
        if i in message:
            await bot.send(ev, '这么臭的青辉石有什么购买的必要吗' + no)
            return
    uid = str(ev.user_id)
    user_dict = json.load(open(user_dict_path, encoding='utf-8'))
    if uid not in user_dict:
        if int(message) > 10000000:
            await bot.send(ev, '不可以贪心' + no)
            return
        else:
            increase_value(ev.user_id, 'stone', int(message))
            await bot.send(ev, ok)
            return
    else:
        if user_dict[uid]['stone'] + int(message) > 10000000:
            await bot.send(ev, '不可以贪心' + no)
            return
        else:
            increase_value(ev.user_id, 'stone', int(message))
            await bot.send(ev, ok)
            return


@sv.on_prefix('档案十连', '档案10连', 'ba十连', 'ba10连')
async def gacha_10_times(bot, ev):
    uid = ev.user_id
    mode = check_mode(uid)
    if not priv.check_priv(ev, priv.SUPERUSER):
        if not flmt.check(uid):
            await bot.send(ev, f'请让冰祈休息一下QAQ...({round(flmt.left_time(uid))}s)')
            return
    flmt.start_cd(uid)
    result = get_10_gacha(uid, mode)
    if not result:
        await bot.send(ev, '青辉石不够喔' + no)
        return
    else:
        await bot.send(ev, result)


@sv.on_prefix('档案单抽', '档案1连', '档案一连', '档案一抽', 'ba单抽')
async def gacha_1_time(bot, ev):
    uid = ev.user_id
    mode = check_mode(uid)
    if not priv.check_priv(ev, priv.SUPERUSER):
        if not flmt.check(uid):
            await bot.send(ev, f'请让冰祈休息一下QAQ...({round(flmt.left_time(uid))}s)')
            return
    flmt.start_cd(uid)
    result = get_1_gacha(uid, mode)
    if not result:
        await bot.send(ev, '青辉石不够喔' + no)
        return
    else:
        await bot.send(ev, result)


@sv.on_prefix('当前up')
async def show_current_pickup(bot, ev):
    gacha_pool = json.load(open(gachaPath, encoding='utf-8'))
    student_data = json.load(open(studentPath, encoding='utf-8'))
    cur_gacha_pool = json.load(open(gachaPath, encoding='utf-8'))
    cur_pickup = cur_gacha_pool['pickup']
    msg = ['当前UP池有：(ID.角色)']
    for i in range(len(cur_pickup)):
        base_info = get_item(student_data, 'Id', int(cur_pickup[i]))
        msg.append(f'{i + 1}.{base_info["Name"]}')
    await bot.send(ev, '\n'.join(msg))


@sv.on_prefix('切换卡池', '换池', '换卡池')
async def change_pickup(bot, ev):
    gacha_pool = json.load(open(gachaPath, encoding='utf-8'))
    uid = ev.user_id
    message = ev.message.extract_plain_text().strip()
    if not message:
        return
    if not str.isdigit(message):
        if message in ['普池', '常驻', '常驻池', 'normal', 'Normal']:
            change_mode(uid, mode = 99)
            await bot.send(ev, '已经换回常驻卡池啦' + ok)
        else:
            await bot.send(ev, '只可以输入卡池ID或"常驻"喔' + no)
            return
    else:
        if int(message) > len(gacha_pool['pickup']):
            await bot.send(ev, '找不到这个ID的卡池，用"当前up"来查看可用的卡池ID' + no)
            return
        else:
            change_mode(uid, mode = int(message) - 1)
            await bot.send(ev, f'切换到{message}号卡池啦' + ok)


@sv.on_prefix('档案语音')
async def archive_voice(bot, ev):
    message = ev.message.extract_plain_text().strip()
    uid = ev.user_id
    if not message:
        return
    _student_id = get_student_id(message)
    if str.isdigit(str(_student_id)):
        await bot.send(ev, '正在放置回声机...')
        await bot.send(ev, '(作者还没有写完这个功能)(小声)' + sorry)
    else:
        if _student_id[0]:
            await bot.send(ev, f"没有找到这名学生..是在找{_student_id[0]}嘛？" + pardon)
        else:
            await bot.send(ev, f"没有找到这名学生.." + sorry)
        return


@sv.on_prefix('更新数据库')
async def update_database(bot, ev):
    if ev.user_id not in SUPERUSERS:
        return
    await bot.send(ev, '正在更新碧蓝档案数据库中，请稍等...')
    try:
        update_db()
        await bot.send(ev, '更新已完成~')
    except Exception as e:
        await bot.send(ev, f'更新失败...({e})')


async def chain_reply(bot, ev, chain, msg):
    data = {
            "type": "node",
            "data": {
                "name": "阿罗娜",
                "uin": str(ev.self_id),
                "content": msg
            }
        }
    chain.append(data)
    return chain
