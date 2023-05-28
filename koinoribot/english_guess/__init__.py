import os
import random
import re

from hoshino import Service
from .._interact import interact, ActSession
from .guess_func import get_random_word, get_random_tango, kana_yomi_splt
from ..build_image import BuildImage
from ..utils import loadData
from .digit_guess_func import get_random_int
from .._R import get

sv = Service('猜单词-英日数')

font_bold = 'yz.ttf'
font_digit = 'HYWenHei-85W.ttf'
font_color = (109, 113, 112)
color_pink = (247, 141, 167)
color_red = (201, 38, 66)
color_light_gray = (230, 230, 230)
color_blue = (219, 238, 250)
color_green = (76, 175, 80)
color_orange = (236, 138, 100)
gap = 55
check_list = loadData(os.path.join(os.path.dirname(__file__), f'data/check_list.json'))  # 加载合法单词表

cap_up = {'A':'Ａ', 'B':'Ｂ', 'C':'Ｃ', 'D':'Ｄ', 'E':'Ｅ', 'F':'Ｆ', 'G':'Ｇ',
          'H':'Ｈ', 'I':'Ｉ', 'J':'Ｊ', 'K':'Ｋ', 'L':'Ｌ', 'M':'Ｍ', 'N':'Ｎ',
          'O':'Ｏ', 'P':'Ｐ', 'Q':'Ｑ', 'R':'Ｒ', 'S':'Ｓ', 'T':'Ｔ',
          'U':'Ｕ', 'V':'Ｖ', 'W':'Ｗ', 'X':'Ｘ', 'Y':'Ｙ', 'Z':'Ｚ'}  # 字体原因，改成全角字母


total_times = [0, 0, 0, 6, 6, 6, 6, 6, 6, 6]
digit_times = [0, 0, 6, 6, 6, 6, 6, 6, 6, 6]
tango_times = [0, 0, 0, 6, 6, 6, 8, 10, 12, 15]
expire_time = [0, 0, 0, 300, 300, 300, 400, 500, 600, 750]
hint_time = [0, 0, 0, 4, 4, 4, 6, 8, 10, 12]  # 获取提示需要的次数
temp_path = os.path.join(os.path.dirname(__file__), 'temp')


stare = get('emotion/瞪.jpg').cqcode


@sv.on_prefix('wordle')
async def start_guess_english_game(bot, ev):
    if interact.find_session(ev, name='猜单词游戏'):
        session = interact.find_session(ev, name='猜单词游戏')
        if session.is_expire():
            session.close()
        else:
            await bot.send(ev, f'上一轮猜单词游戏还没结束，现在正在猜{session.state["type"]}喔')
            return
    message = ev.message.extract_plain_text().strip()
    msg_splt = message.split()
    level = '四级'
    word_len = 5
    gid = ev.group_id
    if len(msg_splt) == 1:
        if str.isdigit(msg_splt[0]) and 3 <= int(msg_splt[0]) <= 9:
            word_len = int(msg_splt[0])
        elif msg_splt[0] in ['四级', '六级', '专八', '八级']:
            level = msg_splt[0]
    elif len(msg_splt) == 2:
        if str.isdigit(msg_splt[0]) and 3 <= int(msg_splt[0]) <= 9:
            word_len = int(msg_splt[0])
            if msg_splt[1] in ['四级', '六级', '专八', '八级']:
                level = (msg_splt[1])
        elif str.isdigit(msg_splt[1]) and 3 <= int(msg_splt[1]) <= 9:
            word_len = int(msg_splt[1])
            if msg_splt[0] in ['四级', '六级', '专八', '八级']:
                level = msg_splt[0]
    elif len(msg_splt) >= 3:
        await bot.send(ev, '例如：wordle 四级 5')
        return
    session = ActSession.from_event('猜单词游戏', ev, usernum_limit=False, expire_time=expire_time[word_len])
    interact.add_session(session)
    rand_word = get_random_word(word_len, level)
    get_word = rand_word['word']
    get_pos = rand_word['pos']
    get_trans = rand_word['trans']
    low_word = get_word.lower()
    session.state['type'] = '英语单词'
    session.state['length'] = word_len
    session.state['word'] = rand_word['word']
    session.state['pos'] = rand_word['pos']
    session.state['trans'] = rand_word['trans']
    session.state['word_low'] = rand_word['word'].lower()
    session.state['times'] = 0
    session.state['total_times'] = total_times[word_len]
    session.state['guessed_words'] = []
    bg_path = os.path.join(os.path.dirname(__file__), f'data/imgs/en/{word_len}len.png')
    bg = BuildImage(0, 0, background=bg_path)
    bg.save(os.path.join(temp_path, f'{gid}.png'))
    await bot.send(ev, f"[CQ:image,file=base64://{bg.pic2bs4()}]\n发送'~单词'来猜单词~当前为{level}词库\n限时{expire_time[word_len]}秒\n示例：~banana")


@sv.on_prefix('digitle')
async def start_guess_figure(bot ,ev):
    if interact.find_session(ev, name='猜单词游戏'):
        session = interact.find_session(ev, name='猜单词游戏')
        if session.is_expire():
            session.close()
        else:
            await bot.send(ev, f'上一轮猜单词游戏还没结束，现在正在猜{session.state["type"]}喔')
            return
    message = ev.message.extract_plain_text().strip()
    length = 3
    if str.isdigit(message) and 3 <= int(message) <= 9:
        length = int(message)
    gid = ev.group_id

    session = ActSession.from_event('猜单词游戏', ev, usernum_limit=False, expire_time=300)
    interact.add_session(session)

    rand_int = get_random_int(length)
    session.state['type'] = '数字'
    session.state['answer'] = int(rand_int)
    session.state['length'] = length
    session.state['times'] = 0
    session.state['total_times'] = digit_times[length]
    bg_path = os.path.join(os.path.dirname(__file__), f'data/imgs/dgt/{length}len.png')
    bg = BuildImage(0, 0, background=bg_path)
    bg.save(os.path.join(temp_path, f'{gid}.png'))
    await bot.send(ev, f"[CQ:image,file=base64://{bg.pic2bs4()}]\n发送'~数字'来猜数字~\n示例：~114514")


@sv.on_prefix('tangole')
async def start_guess_jpese(bot, ev):
    if interact.find_session(ev, name='猜单词游戏'):
        session = interact.find_session(ev, name='猜单词游戏')
        if session.is_expire():
            session.close()
        else:
            await bot.send(ev, f'上一轮猜单词游戏还没结束，现在正在猜{session.state["type"]}喔')
            return
    message = ev.message.extract_plain_text().strip()
    msg_splt = message.split()
    level = 'all'
    if message and message.lower() in ['n45', 'n3', 'n2', 'n1', 'n4', 'n5']:
        level = message.lower()
    gid = ev.group_id
    trans = {'n45': 'N4N5', 'n3': 'N3', 'n2': 'N2', 'n1': 'N1', 'all': '全体'}
    session = ActSession.from_event('猜单词游戏', ev, usernum_limit=False, expire_time=300)
    interact.add_session(session)
    print('到这里了')
    kana = ''
    yomi = ''
    while True:
        rand_tango = get_random_tango(level)
        kana, yomi = kana_yomi_splt(random.choice(rand_tango['kana']))
        if len(kana) < 3 or len(kana) > 6:
            print(f'选到了{kana}，长度为{len(kana)}，将重新选择')
            continue
        break
    length = len(kana)

    session.state['type'] = '日语单词'
    session.state['jpword'] = rand_tango['jpword']
    session.state['kana'] = kana
    session.state['yomi'] = f'[{yomi}]'
    session.state['mean'] = rand_tango['mean']
    session.state['sample'] = rand_tango['sample']
    session.state['times'] = 0
    session.state['length'] = length
    session.state['total_times'] = 4
    bg_path = os.path.join(os.path.dirname(__file__), f'data/japanese/jp_{length}len.png')
    bg = BuildImage(0, 0, background=bg_path)
    bg.save(os.path.join(temp_path, f'{gid}.png'))
    await bot.send(ev, f"[CQ:image,file=base64://{bg.pic2bs4()}]\n发送'~单词'来猜单词~当前为{trans[level]}日语词库，词义为【{rand_tango['mean']}】\n限时5分钟.")



@sv.on_prefix('~', '～', '&')
async def guess_english_game(bot, ev):
    gid = ev.group_id
    session = interact.find_session(ev, name='猜单词游戏')
    if not session:
        return
    if session.state['type'] == '英语单词':
        word = session.state['word']
        word_low = session.state['word_low']
        pos = session.state['pos']
        trans = session.state['trans']
        length = session.state['length']
        times = session.state['times']
        if session.is_expire():
            session.close()
            pic = ''
            if os.path.exists(os.path.join(temp_path, f'{gid}.png')):
                pic = BuildImage(0, 0, background=os.path.join(temp_path, f'{gid}.png'))
            await bot.send(ev, f'[CQ:image,file=base64://{pic.pic2bs4()}]时间已过，正确答案是{word}，{pos}{trans}')
            return
        message = ev.message.extract_plain_text().strip()
        message = message.lower()
        if len(message) != length and message not in ['提示', '退出', '结束']:
            await bot.send(ev, f'要猜的单词长度为{length}喔')
            return
        if message not in check_list[length]:
            if message in ['退出', '结束']:
                await bot.send(ev, f'已退出~\n这个单词是{word}\n{pos}{trans}')
                session.close()
                return
            if message == '提示':
                if session.state['times'] < 4:
                    await bot.send(ev, f"{5 - session.state['times']}次才能获取提示喔")
                    return
                else:
                    await bot.send(ev, f'这个单词的意思是：{trans}')
                    return

            await bot.send(ev, f'这个单词不对喔')
            return
        correct_pos = []
        is_in_word = []

        pic = BuildImage(0, 0, background=os.path.join(temp_path, f'{gid}.png'))
        for i in range(length):
            alphabet = BuildImage(0, 0, plain_text=cap_up[message[i].upper()], font=font_bold, font_size=28, font_color=font_color, is_alpha=True)
            if message[i] == word_low[i]:  # 如果单词位置正确

                word_but_list = list(word_low)  # 转列表，把特定位置的字母转换为*
                word_but_list[i] = '*'
                word_low = ''.join(word_but_list)

                correct_pos.append(message[i])
                pic.rectangle((15 + i * gap, 15 + times * gap, 54 + i * gap, 54 + times * gap), fill = color_blue)
            elif message[i] in word_low:
                word_low.replace(message[i], '*', 1)  # 只替换一个
                is_in_word.append(message[i])
                pic.rectangle((15 + i * gap, 15 + times * gap, 54 + i * gap, 54 + times * gap), fill = color_light_gray)
            pic.paste(alphabet, (35 + i * gap - int(alphabet.w / 2), 32 + times * gap - int(alphabet.h / 2)), alpha=True)
        if len(correct_pos) == length:
            try:
                await bot.send(ev, f'[CQ:image,file=base64://{pic.pic2bs4()}]\n你猜出了这个单词！\n{word}\n{pos}{trans}')
            except Exception as e:
                await bot.send(ev, f'你猜出了这个单词！\n{word}\n{pos}{trans}')
            session.close()
            return
        else:
            session.state['times'] += 1
            if session.state['times'] == session.state['total_times']:
                session.close()
                try:
                    await bot.send(ev, f'[CQ:image,file=base64://{pic.pic2bs4()}]\n次数用完了，没有人猜对...\n{word}\n{pos}{trans}')
                except Exception as e:
                    await bot.send(ev, f'次数用完了，没有人猜对...\n{word}\n{pos}{trans}')
                return
            else:
                pic.save(os.path.join(temp_path, f'{gid}.png'))
                try:
                    await bot.send(ev, f'[CQ:image,file=base64://{pic.pic2bs4()}]')
                except Exception as e:
                    await bot.send(ev, f'[{",".join(is_in_word)}]位置正确，[{",".join(is_in_word)}]在单词中但位置不对。')
        return


    elif session.state['type'] == '数字':
        answer = session.state['answer']  # int
        answer_str = str(answer)  # str
        length = session.state['length']
        times = session.state['times']
        if session.is_expire():
            session.close()
            pic = ''
            if os.path.exists(os.path.join(temp_path, f'{gid}.png')):
                pic = BuildImage(0, 0, background=os.path.join(temp_path, f'{gid}.png'))
            await bot.send(ev, f'[CQ:image,file=base64://{pic.pic2bs4()}]时间已过，正确答案是{answer}')
            return
        message = ev.message.extract_plain_text().strip()
        if not str.isdigit(message):
            if message == '退出':
                await bot.send(ev, f'已退出~\n这个数字是{answer}')
                session.close()
                return
            if message == '提示':
                await bot.send(ev, '猜数字真的有提示的必要嘛?' + stare)
                return
            await bot.send(ev, f'需要输入正整数喔')
            return
        if len(message) != length:
            await bot.send(ev, f'要猜的数字为{length}位数喔')
            return
        correct_pos = []
        is_in_word = []
        pic = BuildImage(0, 0, background=os.path.join(temp_path, f'{gid}.png'))
        if int(message) > int(answer):
            digit_color = color_red
        elif int(message) < int(answer):
            digit_color = color_green
        else:
            digit_color = font_color
        for i in range(length):
            digit = BuildImage(0, 0, plain_text=str(message[i]), font=font_bold, font_size=30, font_color=digit_color, is_alpha=True)
            print(message, answer)
            if message[i] == answer_str[i]:

                answer_but_list = list(answer_str)  # 转列表，把特定位置的字母转换为*
                answer_but_list[i] = '*'
                answer_str = ''.join(answer_but_list)

                correct_pos.append(message[i])
                pic.rectangle((15 + i * gap, 15 + times * gap, 54 + i * gap, 54 + times * gap), fill = color_blue)
            elif message[i] in str(answer):

                answer_str.replace(message[i], '*', 1)

                is_in_word.append(message[i])
                pic.rectangle((15 + i * gap, 15 + times * gap, 54 + i * gap, 54 + times * gap), fill = color_light_gray)
            pic.paste(digit, (34 + i * gap - int(digit.w / 2), 32 + times * gap - int(digit.h / 2)), alpha=True)
        if len(correct_pos) == length:
            try:
                await bot.send(ev, f'[CQ:image,file=base64://{pic.pic2bs4()}]\n你猜出了这个数字！\n它是{answer}')
            except Exception as e:
                await bot.send(ev, f'你猜出了这个数字！\n它是{answer}')
            session.close()
            return
        else:
            session.state['times'] += 1
            if session.state['times'] == session.state['total_times']:
                session.close()
                try:
                    await bot.send(ev, f'[CQ:image,file=base64://{pic.pic2bs4()}]\n次数用完了，没有人猜对...\n它是{answer}')
                except Exception as e:
                    await bot.send(ev, f'次数用完了，没有人猜对...\n它是{answer}')
                return
            else:
                pic.save(os.path.join(temp_path, f'{gid}.png'))
                try:
                    await bot.send(ev, f'[CQ:image,file=base64://{pic.pic2bs4()}]')
                except Exception as e:
                    await bot.send(ev, f'[{",".join(is_in_word)}]位置正确，[{",".join(is_in_word)}]在数字中但位置不对。')
        return


    elif session.state['type'] == '日语单词':
        kana = session.state['kana']
        jpword = session.state['jpword']
        yomi = session.state['yomi']
        mean = session.state['mean']
        sample = f"\n{session.state['sample']}" if session.state['sample'] else ''
        length = session.state['length']
        times = session.state['times']
        if session.is_expire():
            session.close()
            pic = ''
            if os.path.exists(os.path.join(temp_path, f'{gid}.png')):
                pic = BuildImage(0, 0, background=os.path.join(temp_path, f'{gid}.png'))
            await bot.send(ev, f'[CQ:image,file=base64://{pic.pic2bs4()}]时间已过，正确答案是{kana}\n{yomi}{mean}\n{sample}')
            return
        message = ev.message.extract_plain_text().strip()
        rematch = re.findall(r'([\u3040-\u3098]+)', message)
        if len(rematch) != 1:
            if message == '退出':
                await bot.send(ev, f'已退出~\n正确答案是{kana}\n{yomi}{mean}\n{sample}')
                session.close()
                return
            elif message == '提示':
                await bot.send(ev, f'这个单词的意思是：{mean}')
                return
            await bot.send(ev, '需要输入平假名喔')
            return
        if len(rematch[0]) != length:
            await bot.send(ev, f'要猜的单词为{length}个纯假名喔')
            return
        correct_pos = []
        is_in_word = []
        pic = BuildImage(0, 0, background=os.path.join(temp_path, f'{gid}.png'))
        for i in range(length):
            hinagara = BuildImage(0, 0, plain_text=message[i], font=font_bold, font_size=28, font_color=font_color, is_alpha=True)
            if message[i] == kana[i]:
                correct_pos.append(message[i])
                pic.rectangle((15 + i * gap, 15 + times * gap, 54 + i * gap, 54 + times * gap), fill = color_blue)
            elif message[i] in kana:
                is_in_word.append(message[i])
                pic.rectangle((15 + i * gap, 15 + times * gap, 54 + i * gap, 54 + times * gap), fill = color_light_gray)
            pic.paste(hinagara, (35 + i * gap - int(hinagara.w / 2), 33 + times * gap - int(hinagara.h / 2)), alpha=True)
        if len(correct_pos) == length:
            try:
                await bot.send(ev, f'[CQ:image,file=base64://{pic.pic2bs4()}]\n你拼出了这个单词！\n{jpword}({kana})\n{yomi}{mean}{sample}')
            except Exception as e:
                await bot.send(ev, f'你拼出了这个单词！\n{jpword}({kana})\n{yomi}{mean}{sample}')
            session.close()
            return
        else:
            session.state['times'] += 1
            if session.state['times'] == session.state['total_times']:
                session.close()
                try:
                    await bot.send(ev, f'[CQ:image,file=base64://{pic.pic2bs4()}]\n次数用完了，没有人答对...\n\n{jpword}({kana})\n{yomi}{mean}{sample}')
                except Exception as e:
                    await bot.send(ev, f'次数用完了，没有人答对...\n\n{jpword}({kana})\n{yomi}{mean}{sample}')
                return
            else:
                pic.save(os.path.join(temp_path, f'{gid}.png'))
                try:
                    await bot.send(ev, f'[CQ:image,file=base64://{pic.pic2bs4()}]')
                except Exception as e:
                    await bot.send(ev, f'[{",".join(is_in_word)}]位置正确，[{",".join(is_in_word)}]在单词中但位置不对。')
        return