from aiocqhttp.message import escape
from hoshino import Service
from hoshino.typing import CQEvent
import random, os, asyncio, math, ujson
import hoshino
from .._R import userPath

sv = Service('日语学习', help_='''
背日语单词的小插件
'''.strip())

WAIT_TIME = 180 # 等待时间
path_dict = os.path.join(os.path.dirname(__file__), 'dictionary_R.json')
path_count = os.path.join(os.path.dirname(__file__), 'winner_counter.json')
name_dict = os.path.join(userPath, 'call_me_please\\nickname.json')


class UserData:
    def __init__(self):
        self.user_data = {}
        self.content = {}

    def load_dictionary(self, path_dict):
        with open(path_dict, 'r', encoding = 'utf-8') as f:
            self.content = ujson.load(f)

    def load_winner_times(self, uid, path_count):
        try:
            if not os.path.exists(path_count):
                return 'NULL'
            with open(path_count, 'r', encoding='utf8') as f:
                self.user_data = ujson.load(f)
            uid = str(uid)
            if uid not in self.user_data.keys():
                self.user_data[uid] = 0
            return self.user_data[uid]
        except:
            return 'Error'

class Judger:
    def __init__(self):
        self.on = {}
        self.winner = {}

    def turn_on(self, gid):
        self.on[gid] = True

    def turn_off(self, gid):
        self.on[gid] = False
        self.winner[gid] = ''

    def get_on_off_status(self, gid):
        return self.on[gid] if self.on.get(gid) is not None else False

    def get_winner(self, gid):
        return self.winner[gid] if self.winner.get(gid) is not None else ''

    def record_winner(self, gid, uid):
        self.winner[gid] = str(uid)

class QA:
    def __init__(self):
        self.question = ''
        self.answer = ''

    def get_current_question(self, current_question):
        self.question = current_question

    def get_current_answer(self, current_answer):
        self.answer = current_answer


judger = Judger()
data = UserData()
qa_data = QA()
data.load_dictionary(path_dict)


@sv.on_fullmatch('背日语')
async def benkyou(bot, ev):
    try:
        if judger.get_on_off_status(ev.group_id):
            await bot.send(ev, '上轮问答还未结束喔，结束上轮问答请输入"结束"')
            return
        judger.turn_on(ev.group_id)
        question = random.choice(list(data.content))
        answer = data.content[question].strip('～')
        qa_data.get_current_question(question)
        qa_data.get_current_answer(answer)
        length = len(answer)
        ask_msg_first = f'"{question}"的日语是(共{length}个假名)?'
        await bot.send(ev, ask_msg_first)
        await asyncio.sleep(60)
        if judger.get_on_off_status(ev.group_id):
            judger.turn_off(ev.group_id)
            await bot.send(ev, f"一分钟已到，还没有正确答案出现呢...正确答案是'{qa_data.answer}'")
    except Exception as e:
        judger.turn_off(ev.group_id)
        await bot.send(ev, '发生了预料之外的错误:\n' + str(e))


@sv.on_message('group')
async def input_answer_session(bot, ev):
    try:
        if judger.get_on_off_status(ev.group_id):
            uid = ev.user_id
            gid = ev.group_id
            answer = qa_data.answer
            with open(name_dict, 'r+', encoding='utf-8') as f:
                user_dict = ujson.load(f)
            user_id = str(uid)
            if user_id not in user_dict.keys():
                name = ev.sender['nickname']
            else:
                name = user_dict[user_id]['self']
            user_answer = ev.message.extract_plain_text()
            if user_answer == answer and judger.get_winner(gid) == '':
                judger.record_winner(gid, uid)
                if_use_hint = 0
                msg = f'{name}回答正确！'
                await bot.send(ev, msg)
                judger.turn_off(ev.group_id)
            if user_answer == '提示':
                half_length = math.ceil(len(answer) / 2)
                hint = ''
                for i in range(half_length):
                    hint += answer[i]
                msg = f'前{half_length}个假名为：{hint}'
                await bot.send(ev, msg)
                return
    except Exception as e:
        await bot.send(ev, '发生了错误，快点修啊:\n' + str(e))


@sv.on_fullmatch('看答案')
async def get_answer(bot, ev):
    if judger.get_on_off_status(ev.group_id):
        msg = f'没有正确的答案出现呢...\n正确答案是“{qa_data.answer}”'
        judger.turn_off(ev.group_id)
        await bot.send(ev, msg)
    else:
        return


@sv.on_fullmatch('结束')
async def get_owari(bot, ev):
    if judger.get_on_off_status(ev.group_id):
        msg = f'已结束问答，正确答案是“{qa_data.answer}”'
        judger.turn_off(ev.group_id)
        await bot.send(ev, msg)
    else:
        return
