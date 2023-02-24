import os
import json

import hoshino
from ._R import userPath

path = os.path.join(userPath, 'icelogin/user_money.json')
bg_path = os.path.join(os.path.dirname(__file__), 'icelogin/user_background.json')
config = {  # 初始物资
    "default": {
        "gold": 200,  # 金币
        "luckygold": 0,  # 幸运币
        "starstone": 12500,  # 星星
        "kirastone": 0,  # 羽毛石
        "last_login": 0,  # 最后签到日期   防止单日多次签到
        "rp": 0,  # 记录运势rp值   只是防止单日多次抽签rp改变，不做其他用途
        "logindays": 0,  # 记录连续签到次数
        "exgacha": 0,
        "goodluck": 0,  # 宜做事项索引
        "badluck": 0,  # 忌做事项索引
    }
}

keyword_list = [  # 避免错误设置
    "gold",
    "luckygold",
    "starstone",
    "kirastone",
    "last_login",
    "rp",
    "logindays",
    "exgacha",
    "goodluck",
    "badluck"
]

user_money = {}

key_list = ["gold", "luckygold", "starstone", "kirastone"]  # 钱包里的货币：金币，幸运币，星星

name_list = {
    "starstone": ["starstone", "星星", "星石", "星",
                  "stars", "爱星", "艾星"],
    "luckygold": ["luckygold", "lucky", "幸运",
                  "幸运币"],
    "gold": ["gold", "金币", "金子", "黄金"
             ],
    "exgacha": ["井券", "兑换券", "exgacha"],
    "kirastone": ["羽毛石"]
}


def translatename(name):
    for key in name_list.keys():
        if name in name_list[key]:
            return key
    else:
        return ''


def load_user_money():
    try:
        if not os.path.exists(path):
            return 0
        with open(path, encoding='utf8') as f:
            d = json.load(f)
            for k, v in d.items():
                user_money[k] = v
        return 1
    except:
        return 0


load_user_money()


def get_user_money(user_id, key):  # 自带初始化的读取钱包功能
    load_user_money()
    try:
        if key not in keyword_list:
            return None
        user_id = str(user_id)
        if user_id not in user_money:
            user_money[user_id] = {}
            for k, v in config['default'].items():
                user_money[user_id][k] = v
            with open(path, 'w', encoding='utf8') as f:
                json.dump(user_money, f, ensure_ascii=False, indent=2)
        if key in user_money[user_id]:
            return user_money[user_id][key]
        else:
            return None
    except:
        return None


def set_user_money(user_id, key, value):  # 自带初始化的设置货币功能
    try:
        if key not in keyword_list:
            return 0
        user_id = str(user_id)
        if user_id not in user_money:
            user_money[user_id] = {}
            for k, v in config['default'].items():
                user_money[user_id][k] = v
        user_money[user_id][key] = value
        with open(path, 'w', encoding='utf8') as f:
            json.dump(user_money, f, ensure_ascii=False, indent=2)
        return 1
    except:
        return 0


def increase_user_money(user_id, key, value):  # 自带初始化的增加货币功能
    if int(user_id) == 80000000:
        return

    try:
        if key not in keyword_list:
            return 0
        user_id = str(user_id)
        if user_id not in user_money:
            user_money[user_id] = {}
            for k, v in config['default'].items():
                user_money[user_id][k] = v
        if key not in user_money[user_id].keys():
            user_money[user_id][key] = config['default'][key] + value
        else:
            now_money = int(get_user_money(user_id, key)) + value
            user_money[user_id][key] = now_money
        with open(path, 'w', encoding='utf8') as f:
            json.dump(user_money, f, ensure_ascii=False, indent=2)
        return 1
    except:
        return 0


def reduce_user_money(user_id, key, value):  # 自带初始化的减少货币功能
    if int(user_id) == 80000000:
        return

    try:
        if key not in keyword_list:
            return 0
        user_id = str(user_id)
        if user_id not in user_money:
            user_money[user_id] = {}
            for k, v in config['default'].items():
                user_money[user_id][k] = v
        if key not in user_money[user_id].keys():
            user_money[user_id][key] = config['default'][key]
            return 0
        else:
            now_money = int(get_user_money(user_id, key)) - value
        if now_money < 0:
            return 0
        user_money[user_id][key] = now_money
        with open(path, 'w', encoding='utf8') as f:
            json.dump(user_money, f, ensure_ascii=False, indent=2)
        return 1
    except:
        return 0


def increase_all_user_money(key, value):
    try:
        if key not in keyword_list:
            return 0
        for user_id in user_money.keys():
            if key not in user_money[user_id].keys():
                user_money[user_id][key] = config['default'][key]
            user_money[user_id][key] += value
        with open(path, 'w', encoding='utf8') as f:
            json.dump(user_money, f, ensure_ascii=False, indent=2)
        return 1
    except:
        return 0


def tran_kira(uid, key, num):
    if key == 'gold':
        value = num * 10
    elif key == 'starstone':
        value = num * 10
    elif key == 'luckygold':
        value = num // 50
        num = value * 50
    else:
        value = 0
        num = 0
    increase_user_money(uid, key, value)
    reduce_user_money(uid, 'kirastone', num)
    return num, value


def load_user_background():
    if not os.path.exists(bg_path):
        empty_dict = {}
        with open(bg_path, 'w', encoding='utf-8') as f:
            json.dump(empty_dict, f, ensure_ascii=False, indent=2)
        return {}
    else:
        try:
            user_dict = json.load(open(bg_path, encoding='utf-8'))
        except:
            hoshino.logger.error('用户背景图片配置加载失败。')
            user_dict = {}
        return user_dict


user_bg = load_user_background()


def get_user_background(uid):
    if int(uid) == 80000000:
        return {'default': '', 'custom': '', 'mode': 0}
    user_bg = load_user_background()
    return user_bg[str(uid)] if str(uid) in user_bg else {'default': '', 'custom': '', 'mode': 0}


def set_user_background(uid: int, bg: str, kind: str = 'default'):
    if uid == 80000000:
        return
    try:
        user_id = str(uid)
        if user_id not in user_bg:
            user_bg[user_id] = {'default': '', 'custom': '', 'mode': 0}
        user_bg[user_id][kind] = bg
        with open(bg_path, 'w', encoding='utf8') as f:
            json.dump(user_bg, f, ensure_ascii=False, indent=2)
        return 1
    except:
        return 0


def set_user_bg_mode(uid: int, mode: int):
    """
    :param: mode:0-默认，1-hoshi，2-自定义
    """
    if uid == 80000000:
        return
    try:
        user_id = str(uid)
        if user_id not in user_bg:
            user_bg[user_id] = {'default': '', 'custom': '', 'mode': 0}
        user_bg[user_id]['mode'] = mode
        with open(bg_path, 'w', encoding='utf8') as f:
            json.dump(user_bg, f, ensure_ascii=False, indent=2)
        return 1
    except:
        return 0


def check_mode(uid):
    if str(uid) not in user_bg:
        set_user_bg_mode(uid, 0)
        return
    if user_bg[str(uid)]['custom']:
        set_user_bg_mode(uid, 2)
    elif 'hoshi' in user_bg[str(uid)]['default']:
        set_user_bg_mode(uid, 1)
    elif user_bg[str(uid)]['default']:
        set_user_bg_mode(uid, 0)
    else:
        set_user_background(uid, 'Background3.jpg')
        set_user_bg_mode(uid, 0)
