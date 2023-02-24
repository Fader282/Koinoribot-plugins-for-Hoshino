import os
import json

#用于用户金钱控制
#get_user_money(user_id, key) return int    获取某种资源用户有多少
#set_user_money(user_id, key, value)        直接设置用户某种资源为多少
#increase_user_money(user_id, key, value)   增加用户某种资源多少
#reduce_user_money(user_id, key, value)     减少用户某种资源多少（含数值校验）
#increase_all_user_money(key, value         增加全部用户某种资源多少
#translatename(name)                        将货币昵称转换成关键字
#tran_kira(uid, key, num)                   将羽毛石转换成某个其他物资（请先用translatename(name) 转换为关键字）


path = os.path.join(os.path.dirname(__file__), 'user_money.json')
config = {                       #初始物资
    "default": {
        "gold" : 300,            #金币
        "luckygold": 0,          #幸运币
        "starstone": 12500,      #星星
        "kirastone": 0,          #羽毛石
        "last_login": 0,         #最后签到日期   防止单日多次签到
        "rp": 0,                 #记录运势rp值   只是防止单日多次抽签rp改变，不做其他用途
        "logindays":0,           #记录连续签到次数
        "exgacha":0,
    }
}

keyword_list = [                 #避免错误设置
    "gold",
    "luckygold",
    "starstone",
    "kirastone",
    "last_login",
    "rp",
    "logindays",
    "exgacha"
]


user_money = {}

key_list = ["gold", "luckygold", "starstone", "kirastone"] # 钱包里的货币：金币，幸运币，星星

name_list = {
    "starstone":["starstone", "星星", "星石", "星",
                "stars", "爱星", "艾星"],
    "luckygold":["luckygold", "lucky", "幸运",
                "幸运币"],
    "gold":["gold", "金币", "金子", "黄金"
                 ],
    "exgacha":["井券", "兑换券", "exgacha"],
    "kirastone":["羽毛石"]
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
            for k,v in d.items():
                user_money[k] = v
        return 1
    except:
        return 0
load_user_money()

def get_user_money(user_id, key):
    try:
        if not key in keyword_list:
            return None
        user_id = str(user_id)
        if user_id not in user_money:
            user_money[user_id] = {}
            for k, v in config['default'].items():
                user_money[user_id][k] = v
        if key in user_money[user_id]:
            return user_money[user_id][key]
        else:
            return None
    except:
        return None

def set_user_money(user_id, key, value):
    try:
        if not key in keyword_list:
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
         
def increase_user_money(user_id, key, value):
    try:
        if not key in keyword_list:
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
          
def reduce_user_money(user_id, key, value):
    try:
        if not key in keyword_list:
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
        if not key in keyword_list:
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
