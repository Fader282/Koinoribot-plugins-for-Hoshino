import os

from hoshino import Service
from .._interact import interact, ActSession
from .guess_func import get_random_word
from ..build_image import BuildImage
from ..utils import loadData

sv = Service('猜单词-英语')

font_bold = 'yz.ttf'
font_color = (109, 113, 112)
color_pink = (245, 200, 211)
color_light_gray = (230, 230, 230)
color_blue = (202, 231, 250)
gap = 55
check_list = loadData(os.path.join(os.path.dirname(__file__), f'data/check_list_8.json'))

cap_up = {'A':'Ａ', 'B':'Ｂ', 'C':'Ｃ', 'D':'Ｄ', 'E':'Ｅ', 'F':'Ｆ', 'G':'Ｇ',
          'H':'Ｈ', 'I':'Ｉ', 'J':'Ｊ', 'K':'Ｋ', 'L':'Ｌ', 'M':'Ｍ', 'N':'Ｎ',
          'O':'Ｏ', 'P':'Ｐ', 'Q':'Ｑ', 'R':'Ｒ', 'S':'Ｓ', 'T':'Ｔ',
          'U':'Ｕ', 'V':'Ｖ', 'W':'Ｗ', 'X':'Ｘ', 'Y':'Ｙ', 'Z':'Ｚ'}


total_times = [0, 0, 0, 6, 6, 6, 8, 10, 12, 15]
expire_time = [0, 0, 0, 300, 300, 300, 400, 500, 600, 750]
temp_path = os.path.join(os.path.dirname(__file__), 'temp')


@sv.on_prefix('wordle')
async def start_guess_english_game(bot, ev):
    if interact.find_session(ev, name='英语猜单词'):
        await bot.send(ev, '英语猜单词 正在进行中')
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
    session = ActSession.from_event('英语猜单词', ev, usernum_limit=False, expire_time=expire_time[word_len])
    interact.add_session(session)
    rand_word = get_random_word(word_len, level)
    get_word = rand_word['word']
    get_pos = rand_word['pos']
    get_trans = rand_word['trans']
    low_word = get_word.lower()
    session.state['length'] = word_len
    session.state['word'] = rand_word['word']
    session.state['pos'] = rand_word['pos']
    session.state['trans'] = rand_word['trans']
    session.state['word_low'] = rand_word['word'].lower()
    session.state['times'] = 0
    session.state['total_times'] = total_times[word_len]
    session.state['guessed_words'] = []
    bg_path = os.path.join(os.path.dirname(__file__), f'data/{word_len}len.png')
    bg = BuildImage(0, 0, background=bg_path)
    bg.save(os.path.join(temp_path, f'{gid}.png'))
    await bot.send(ev, f"[CQ:image,file=base64://{bg.pic2bs4()}]\n发送'~单词'来猜单词~\n限时{expire_time[word_len]}秒，蓝色为字母位置正确，灰色为字母正确位置不对")


@sv.on_prefix('~', '～')
async def guess_english_game(bot, ev):
    gid = ev.group_id
    session = interact.find_session(ev, name='英语猜单词')
    if not session:
        return
    word = session.state['word']
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
    if message not in check_list:
        if message == '退出':
            await bot.send(ev, f'已退出~\n这个单词是{word}\n{pos}{trans}')
            session.close()
            return
        await bot.send(ev, f'这个单词不是四六级/专八词汇喔')
        return
    if len(message) != length:
        await bot.send(ev, f'要猜的单词长度为{length}喔')
        return
    correct_pos = []
    is_in_word = []
    pic = BuildImage(0, 0, background=os.path.join(temp_path, f'{gid}.png'))
    for i in range(length):
        alphabet = BuildImage(0, 0, plain_text=cap_up[message[i].upper()], font=font_bold, font_size=28, font_color=font_color, is_alpha=True)
        print(alphabet.w, alphabet.h)
        if message[i] == session.state['word_low'][i]:
            correct_pos.append(message[i])
            pic.rectangle((15 + i * gap, 15 + times * gap, 54 + i * gap, 54 + times * gap), fill = color_blue)
        elif message[i] in session.state['word_low'] and message[i] not in correct_pos:
            is_in_word.append(message[i])
            pic.rectangle((15 + i * gap, 15 + times * gap, 54 + i * gap, 54 + times * gap), fill = color_light_gray)
        pic.paste(alphabet, (35 + i * gap - int(alphabet.w / 2), 32 + times * gap - int(alphabet.h / 2)), alpha=True)
    session.state['times'] += 1
    if len(correct_pos) == length:
        try:
            await bot.send(ev, f'[CQ:image,file=base64://{pic.pic2bs4()}]\n你猜出了这个单词！\n{word}\n{pos}{trans}')
        except Exception as e:
            await bot.send(ev, f'你猜出了这个单词！\n{word}\n{pos}{trans}')
        session.close()
        return
    else:
        if session.state['times'] == session.state['total_times']:
            session.close()
            try:
                await bot.send(ev, f'[CQ:image,file=base64://{pic.pic2bs4()}]\n很遗憾没有人猜对...\n{word}\n{pos}{trans}')
            except Exception as e:
                await bot.send(ev, '很遗憾没有人猜对...\n{word}\n{pos}{trans}')
            return
        else:
            pic.save(os.path.join(temp_path, f'{gid}.png'))
            try:
                await bot.send(ev, f'[CQ:image,file=base64://{pic.pic2bs4()}]')
            except Exception as e:
                await bot.send(ev, f'[{",".join(is_in_word)}]位置正确，[{",".join(is_in_word)}]在单词中但位置不对。')




