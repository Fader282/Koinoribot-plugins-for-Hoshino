import re

from hoshino import Service
from hoshino.util import escape
from .translate import sconnect
from .get_voice import get_tts_voice
from .index_dict import get_index, get_speaker
from ..GroupFreqLimiter import check_reload_group, set_reload_group

jp_help = '''
<-----支持的[某角色]一览----->
魔女的夜宴：宁宁、爱瑠
千恋万花：芳乃、茉子、丛雨、小春
Riddle Joker：七海
灵感满溢的甜蜜创想：妃爱、华乃、亚澄、诗樱、天梨、里、广梦、莉莉子
咖啡馆与死神之蝶：夏目、栞那、墨染希、爱衣、凉音
缘〇空：穹妹、目瑛、奈绪、一叶
万华镜：莲华、雾枝、雫、亚璃子、椎、夕莉
茸雪（支持中文）：小茸、唐乐吟
Clover Day's：杏璃、杏铃
苍之彼方的四重奏：明日香、真白
ATRI：亚托莉
想要传达给你的爱恋：星奏、新堂、结衣
可塑性记忆：艾拉
糖调：冰织
五彩斑斓的世界：真红
'''.strip()


sv = Service('模型拟声', help_=jp_help)


@sv.on_rex(r'^(.+)说(.+)$')
async def txt_to_voice_moe(bot, ev):
    msg_match = ev.match
    speaker_name = msg_match.group(1).strip()
    message = msg_match.group(2).strip()
    if not message:
        return
    sp_index = get_index(speaker_name)
    sp_name = get_speaker(speaker_name)
    if not sp_index:
        return
    await bot.send(ev, '正在模拟音声...')
    try:
        resp = jp_translate(message)
    except Exception as e:
        await bot.send(ev, '翻译失败了...' + str(e))
        return
    try:
        cqcode = await get_tts_voice(str(sp_index), resp, sp_name)
    except Exception as e:
        await bot.send(ev, '模拟失败了...' + str(e))
        return
    await bot.send(ev, cqcode)


@sv.on_prefix('拟声帮助')
@sv.on_suffix('拟声帮助')
async def get_moetts_help(bot, ev):
    if check_reload_group(ev.group_id, _type='boolean'):
        await bot.send(ev, '字太多了，翻看一下消息记录吧QAQ')
        return
    set_reload_group(ev.group_id, _time=600)
    await bot.send(ev, jp_help)


def jp_translate(text):
    jap = re.compile(r'[\u3040-\u309F\u30A0-\u30FF]')
    text = escape(text)
    text_jp = text if jap.search(text) else sconnect(text)[0]
    return text_jp

