import os
import time
from nonebot import RequestSession, get_bot
from aiocqhttp.exceptions import ActionFailed
from hoshino import Service
from hoshino.config import SUPERUSERS
import re
from ..config import white_list_group, group_auto_approve, friend_auto_approve, star_cost_mode
from ..utils import saveData, loadData
from .._R import userPath

whitelistPath = os.path.join(userPath, 'koimanage/whitelist.json')
blacklistPath = os.path.join(userPath, 'koimanage/blacklist.json')
requestPath = os.path.join(userPath, 'koimanage/requestlist.json')

sv = Service('冰祈邀请管理', help_='加好友/邀请入群管理', enable_on_default=True)


@sv.on_request('group.invite')
async def handle_group_invite(session: RequestSession):
    bot_auto_approve = group_auto_approve
    bot = session.bot
    ev = session.event
    uid, gid, flag_id = ev['user_id'], ev['group_id'], ev['flag']
    try:
        group_info = await bot.get_group_member_list(group_id=white_list_group, self_id=ev.self_id)
        member_list = [member['user_id'] for member in group_info]
    except ActionFailed:
        member_list = []
    is_msg = '已加入杂谈群' if uid in member_list else '未加入杂谈群'
    in_group_flag = 1 if uid in member_list else 0
    is_msg = '(bot未进入白名单群)' if not member_list else in_group_flag
    await bot.send_private_msg(user_id=SUPERUSERS[0], message=f'[群邀请]收到来自QQ{uid}({is_msg})的邀请请求:群{gid}, flag:{flag_id}')
    add_invite_info(gid, flag_id)
    if bot_auto_approve and in_group_flag:  # 带冷却的自动同意
        now = int(time.time())
        cool_time = loadData(os.path.join(os.path.dirname(__file__), f'group_invite_{ev.self_id}.json'))
        try:
            cool_time = cool_time['time']
        except:
            cool_time = {'time': 0}
        if now >= cool_time + 7200:
            await bot.send_private_msg(user_id=SUPERUSERS[0], message='已自动同意邀请')
            await bot.set_group_add_request(flag = flag_id, sub_type= 'invite', approve = True)
            saveData({'time': now}, os.path.join(os.path.dirname(__file__), f'group_invite_{ev.self_id}.json'))
        return


@sv.on_request('friend')
async def notice_friend_request(session: RequestSession):
    bot_auto_approve = friend_auto_approve
    bot = session.bot
    ev = session.event
    uid = ev['user_id']
    flag_id = ev['flag']
    comment = ev['comment']
    try:
        group_info = await bot.get_group_member_list(group_id=white_list_group, self_id=ev.self_id)
        member_list = [member['user_id'] for member in group_info]
    except ActionFailed:
        member_list = []
    is_msg = '已加入杂谈群' if uid in member_list else '未加入杂谈群'
    is_auto = 1 if uid in member_list else 0
    is_msg = '(bot未进入白名单群)' if not member_list else is_msg
    await bot.send_private_msg(user_id=SUPERUSERS[0], message=f'收到来自QQ{uid}({is_msg})的好友请求:"{comment}", flag:{flag_id}')
    if bot_auto_approve and is_auto:
        now = int(time.time())
        cool_time = loadData(os.path.join(os.path.dirname(__file__), f'friend_request_{ev.self_id}.json'))
        cool_time = cool_time['time']
        if now >= cool_time + 7200:  # 两个小时同意一次
            await bot.set_friend_add_request(flag = str(flag_id), approve = True)
            await bot.send_private_msg(user_id=SUPERUSERS[0], message=f'已自动同意QQ{uid}({is_msg})的好友请求')
            saveData({'time': now}, os.path.join(os.path.dirname(__file__), f'friend_request_{ev.self_id}.json'))
        else:
            return


bot = get_bot()


@bot.on_message('private')
async def solve_group_invite(ctx):
    session = ctx.session
    if int(ctx['sender']['user_id']) != SUPERUSERS[0]:
        return
    message = ctx['message']
    if 'addw' in str(message):
        match_ = re.match(r'(addw)(\d+)', str(message))
        if match_ is not None:
            match_gid = match_.group(2)
        else:
            return
        white_list = loadData(whitelistPath, is_list=True)
        if int(match_gid) in white_list:
            await bot.send_private_msg(user_id=SUPERUSERS[0], message=f'群{match_gid}已在白名单中')
            return
        white_list.append(int(match_gid))
        saveData(white_list, whitelistPath)
        await bot.send_private_msg(user_id=SUPERUSERS[0], message=f'已将群{match_gid}加入白名单')
        return
    if 'remw' in str(message):
        match_ = re.match(r'(remw)(\d+)', str(message))
        if match_ is not None:
            match_gid = match_.group(2)
        else:
            return
        white_list = loadData(whitelistPath, is_list=True)
        try:
            white_list.remove(int(match_gid))
        except ValueError:
            await bot.send_private_msg(user_id=SUPERUSERS[0], message=f'群{match_gid}不在白名单里')
            return
        saveData(white_list, whitelistPath)
        await bot.send_private_msg(user_id=SUPERUSERS[0], message=f'已将群{match_gid}移除白名单')
    match_ = re.match(r'(tyg)(\d+)', str(message))
    if match_ is not None:
        match_flag = match_.group(2)
    else:
        return
    try:
        await bot.set_group_add_request(flag = str(match_flag), sub_type= 'invite', approve = True)
        request_dict = loadData(requestPath)
        if match_flag in request_dict.keys():
            request_gid = request_dict[match_flag]
            white_list = loadData(whitelistPath, is_list=True)
            if int(request_gid) not in white_list:
                white_list.append(int(request_gid))
                saveData(white_list, whitelistPath)
                add_msg = f'(已将群{request_gid}加入白名单)'
            else:
                add_msg = f'(群{request_gid}已在白名单中)'
        else:
            add_msg = '(未找到该群聊，白名单添加失败，请手动添加)'
        await bot.send_private_msg(user_id=SUPERUSERS[0], message='已同意邀请' + add_msg)
    except Exception as e:
        await bot.send_private_msg(user_id=SUPERUSERS[0], message=f'群聊邀请flag:"{match_flag}"处理失败，错误：{e}')

    if star_cost_mode:
        curr_star = money.get_money(ctx['sender']['user_id'], 'starstone')
        if curr_star < 6300:
            await session.reject(reason='星星不足噢，至少需要63组星星~')
        else:
            await session.approve()
            money.change_money(ctx['sender']['user_id'], 'starstone', -6300)


@bot.on_message('private')
async def handle_friend_request(ctx):
    if int(ctx['sender']['user_id']) != SUPERUSERS[0]:
        return
    message = ctx['message']
    match_ = re.match(r'(tyf)(\d+)', str(message))
    if match_ is not None:
        match_flag = match_.group(2)
    else:
        return
    try:
        await bot.set_friend_add_request(flag = str(match_flag), approve = True)
        await bot.send_private_msg(user_id=SUPERUSERS[0], message='已同意好友请求')
    except Exception as e:
        await bot.send_private_msg(user_id=SUPERUSERS[0], message=f'好友请求flag:"{match_flag}"处理失败，错误：{e}')


def add_invite_info(gid, flag):
    request_manager = loadData(requestPath)
    gid, flag= str(gid), str(flag)
    request_manager[flag] = gid
    saveData(request_manager, requestPath)

