import os
import random
import re

from ..utils import loadData, saveData


check_list = loadData(os.path.join(os.path.dirname(__file__), f'data/check_list_8.json'))
level_trans = {'四级': 'cet_4', '六级': 'cet_6', '专八': 'level_8', '八级': 'level_8'}
level_trans_jp = {'n5': 'n45', 'n4': 'n45', 'n3': 'n3', 'n2': 'n2', 'n1': 'n1', 'all': 'all', 'n45': 'n45'}



def load_dict(level: str = '四级', word_len: int = 5):
    if level not in ['四级', '六级', '专八', '八级']:
        raise ValueError(f"'level' got an error value: {level}")
    folder = level_trans[level]
    dictionary = loadData(os.path.join(os.path.dirname(__file__), f'data/{folder}/word_{word_len}len.json'))
    return dictionary


def load_jp_dict(level: str = 'all'):
    level = level.lower()
    if level not in ['n45', 'n3', 'n2', 'n1', 'n4', 'n5']:
        level = 'all'
    dictionary = loadData(os.path.join(os.path.dirname(__file__), f'data/japanese/{level}/{level}_list.json'))
    return dictionary


def guess_game(word_len: int, level: str = '四级'):
    """
        猜英语单词的游戏（命令提示符版）
    """
    word = ['_' for i in range(word_len)]
    dictionary = load_dict(level, word_len)
    rand_word = random.choice(dictionary)
    get_word = rand_word['word']
    get_pos = rand_word['pos']
    get_trans = rand_word['trans']
    low_word = get_word.lower()
    active = True
    while active:
        is_in_word = []
        correct_pos = []
        user_guess = get_input(word_len)
        print(user_guess)
        for i in range(word_len):
            if user_guess[i] == low_word[i]:
                correct_pos.append(user_guess[i])
                word[i] = user_guess[i]
            if user_guess[i] in low_word and user_guess[i] not in correct_pos:
                is_in_word.append(user_guess[i])
        if len(correct_pos) == 5:
            active = False
            print(f'你猜出了这个单词！\n{get_word}\n{get_pos} {get_trans}')
        else:
            hint = f"[{'、'.join(is_in_word)}]在正确答案中但位置不对" if is_in_word else ''
            print(f"{format_word(word)}\n{hint}")


    # print(format_word(word))


def get_random_word(word_len: int, level: str = '四级'):
    dictionary = load_dict(level, word_len)
    rand_word = random.choice(dictionary)
    return rand_word


def get_random_tango(level: str = 'all'):
    dictionary = load_jp_dict(level)
    rand_tango = random.choice(dictionary)
    return rand_tango


def get_input(word_len: int):
    active = True
    uinput = ''
    while active:
        uinput = input('请猜一猜这个单词：').lower()
        if len(uinput) != word_len:
            print(f'长度不对，要猜的单词只有{word_len}个字母')
            continue
        if uinput not in check_list:
            print(f'这个单词是四六级/专八词汇吗')
            continue
        else:
            active = False
    return uinput


def kana_yomi_splt(word: str):
    """
        将假名与读音分开
    """
    rematch = re.findall(r'([\u30a1-\u30f6\u3041-\u3093\uFF00-\uFFFF\u4e00-\u9fa5]+)([⓪①②③④⑤⑥⑦⑧⑨⑩]+(或[⓪①②③④⑤⑥⑦⑧⑨⑩]+)?)?', word)
    kana = rematch[0][0]
    yomi = rematch[0][1]
    return kana, yomi


def format_word(word: list):
    string = ''.join(word)
    return string


if __name__ == '__main__':
    guess_game(7)