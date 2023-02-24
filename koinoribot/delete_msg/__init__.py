import re
import hoshino
from hoshino import Service, log, priv, util
from hoshino.typing import CQEvent
from aiocqhttp.exceptions import ActionFailed
from hoshino.config import NICKNAME
from .._R import get

sv = Service('消息撤回功能')

emmm = f"{get('emotion/无语.png').cqcode}"
no = f"{get('emotion/no.png').cqcode}"

if type(NICKNAME) == str:
    NICKNAME = [NICKNAME]

@sv.on_prefix('撤回')
@sv.on_suffix('撤回')
async def reply_delete(bot, ev):

    ret = re.search(r"\[CQ:reply,id=(-?\d*)\]", str(ev.raw_message))
    if not ret:
        return
    ret_at = re.search(r"\[CQ:at,qq=(\d*)\]", str(ev.raw_message))
    at_id= ret_at.group(1)
    if int(at_id) != ev.self_id:
        return
    gid = ev.group_id
    msg_id = ev.message_id
    timeStamp = ret.group(1)
    try:
        await bot.delete_msg(message_id = int(timeStamp))
    except ActionFailed as e:
        await bot.send_msg(group_id = gid, message = '撤回失败了...可能消息已过期' + no)
        hoshino.logger.error(e)

'''
@sv.on_message('group')
async def replymessage(bot, ev: CQEvent):
    ret = re.search(r"\[CQ:reply,id=(-?\d*)\](.*)", str(ev.message))
    if not ret:
        return
    else:
        selfID = ev.self_id
        groupID = ev.group_id
        msg_id = ev.message_id
        uid = ev.user_id
        time_id = ret.group(1) # 回复的id
        command = ret.group(2).strip() # 回复内容
        flag1 = 0 # 是否是回复
        flag2 = 0 # 是否呼叫bot
        if f"[CQ:at,qq={ev.self_id}]" in command:
            flag1 = 1
        else:
            for name in NICKNAME:
                if name in command:
                    flag1 = 1
                    break
        for del_command in ['撤回']:
            if del_command in command:
                flag2 = 1
        if not (flag1 and flag2):
            return
        try: # 尝试撤回
            tmsg = await bot.get_msg(self_id=ev.self_id, message_id=int(time_id))
            if int(tmsg['sender']['user_id']) == ev.self_id:
                await bot.delete_msg(message_id=int(tmsg['message_id']))
            else:
                await bot.send(ev, '不是冰祈的消息喔')
        except ActionFailed:
            await bot.send(ev, '撤回失败了,可能该消息已过期...' + no)
'''