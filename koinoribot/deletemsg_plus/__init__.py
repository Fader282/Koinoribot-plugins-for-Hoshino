import re
import hoshino
from hoshino import Service, log, priv, util
from hoshino.typing import CQEvent
from aiocqhttp.exceptions import ActionFailed
from hoshino.config import NICKNAME
from .._R import get

sv = Service('recall_plus')

emmm = f"{get('emotion/无语.png').cqcode}"
no = f"{get('emotion/no.png').cqcode}"

@sv.on_prefix('撤回plus')
@sv.on_suffix('撤回plus')
async def reply_delete(bot, ev):

    ret = re.search(r"\[CQ:reply,id=(-?\d*)\]", str(ev.raw_message))
    if not ret:
        return
    ret_at = re.findall(r"\[CQ:at,qq=(\d*)\]", str(ev.raw_message))
    if str(ev.self_id) not in ret_at:
        return
    sid = ev.self_id
    selfInfo = await bot.get_group_member_info(group_id = ev.group_id, user_id = sid, no_cache = True)
    if selfInfo['role'] == 'member':
        return
    gid = ev.group_id
    msg_id = ev.message_id
    timeStamp = ret.group(1)
    try:
        await bot.delete_msg(message_id = int(timeStamp))
    except ActionFailed as e:
        await bot.send_msg(group_id = gid, message = '撤回失败了(消息过期或权限不足)' + no)
        hoshino.logger.error(e)