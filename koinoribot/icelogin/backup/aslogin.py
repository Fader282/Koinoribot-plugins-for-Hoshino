import random, time
from .config import money
from hoshino.typing import CQEvent

# 务必保证宜做事项与忌做事项数量一致
goodluck = [ '宜 抽卡', '宜 干饭', '宜 摸鱼', '宜 刷圣遗物', 
             '宜 女装', '宜 打音游', '宜 刷b站', '宜 看涩图',
             '宜 逛街', '宜 好好学习', '宜 搓麻将', '宜 打FPS类游戏',
             '宜 点外卖'
]

badluck = [ '忌 抽卡上头', '忌 干饭', '忌 摸鱼', '忌 刷圣遗物', 
            '忌 女装', '忌 打音游', '忌 刷b站', '忌 看涩图', 
            '忌 逛街', '忌 学习', '忌 搓麻将', '忌 打FPS类游戏',
            '忌 点外卖'
]

birth_list = ["0808",
]

member_list = ["冰祈",
]

event_list = [  '0101', '1225', '0214', '0308', '0401', '0405', '0501',
                '0601', '0603', '0701', '0801', '0804', '0910', '1001',
                '1010'
]

event_name_list = [ '元旦节', '圣诞节', '情人节', '妇女节', '愚人节', '清明节', '劳动节',
                    '儿童节', '端午节', '建党节', '建军节', '七夕节', '中秋节', '国庆节',
                    '萌节'
]

week_list = [ "日", "一", "二", "三", "四", "五", "六"]

def hash():
    days = random.randint(10000000, 99999999)
    return days >> 8

def conti_login(days, months, last_login): # 连续登录(?)
    try:
        _last_login = str(last_login)
        _len = len(_last_login)
        _m = ''
        _d = ''
        temp = 0
        for i in range(_len):
            if _last_login[_len - i -1] == '0' and i != 0 and not temp:
                temp = 1
                continue
            if temp:
                _m += _last_login[_len - i -1]
            else:
                _d +=_last_login[_len - i -1]
        _m += '0' if len(_m) == 2 else ''
        _d += '0' if len(_d) == 1 else ''
        _months = int(f'{_m[1]}{_m[0]}')
        _days = int(f'{_d[1]}{_d[0]}')
        if days - _days == 1 and _months == months:
            return 1
        elif days == 1 and months - _months == 1:
            if _days == 31 and _months in [1,3,5,7,8,10,12]:
                return 1
            elif _days == 30 and _months in [4,6,9,11]:
                return 1
            elif _days == 28 | 29 and _months == 2:
                return 1
            else:
                return 0
        elif days == 1 and months == 1:
            return 1 if _days == 31 and _months == 12 else 0
        else:
            return 0
    except:
        return 0
    

def get_day(days, months):
    flag_day = str(days) if days > 9 else f'0{str(days)}'
    flag_month = str(months) if months > 9 else f'0{str(months)}'
    flag = flag_month + flag_day
    i = 0
    msg = ''
    birth_flag = 0
    event_flag = 0
    for birth in birth_list:
        if flag == birth:
            birth_flag = 1
            msg += f'今天是{member_list[i]}的生日！\n额外获得了600颗星星和300枚金币哦~\n'
            break
        i += 1
    i = 0
    for event in event_list:
        if flag == event:
            event_flag == 1
            msg += f'今天是{event_name_list[i]}！\n额外获得了400颗星星和200枚金币哦~\n'
            break
        i += 1

    return birth_flag, event_flag, msg

def feed_back(value):
    if value < 20 and value != 0:
        info = f"运势很差呢,摸摸..."
    elif value < 40:
        info = f"运势欠佳喔,一定会好起来的！"
    elif value < 60:
        info = f"运势普普通通,不好也不坏噢~"
    elif value < 80:
        info = f"运势不错~会有什么好事发生吗?"
    elif value < 90:
        info = f"运势旺盛！今天是个好日子~"
    elif value <= 99:
        info = f"好运爆棚！一定有好事发生吧！"
    elif value == 100:
        info = f"100！！今天说不定能发大财！！"
    elif value == 0:
        info = f"QAQ冰祈...冰祈不素故意的..."
    else:
        info = f"999！！是隐藏的999运势！！！"
    return info

def as_login(uid, username):
    list_len = len(goodluck)
    days = int(time.strftime("%d", time.localtime(time.time())))
    months = int(time.strftime("%m", time.localtime(time.time())))
    week = int(time.strftime("%w", time.localtime(time.time())))
    birth_flag, event_flag, msgg = get_day(days, months)
    last_login = int(money.get_user_money(uid, "last_login"))
    gold = random.randint(100,200) # 签到增加的基础金币
    conti_flag = conti_login(days, months, last_login)
    
    login_flag = 1 if int(f'{months}0{days}') == last_login else 0
    h = int(money.get_user_money(uid, "rp")) if login_flag else hash() # 如果已经签过到，获取今日的人品值，范围0~100
    _h = h
    bingo = random.randrange(101)
    if bingo == 100:
        rp = 999 
    else:
        rp = _h % 101
    info = feed_back(rp)
    luck_choice = list(random.sample(range(0,list_len),2))
    good_value = luck_choice[0]
    bad_value = luck_choice[-1]
    
    msg = f'欢迎回来~今天是{months}月{days}日 星期{week_list[week]}\n' 
    msg += '今天已经签过到了唷~\n' if login_flag == 1 else ''
    if conti_flag and not login_flag:
        money.increase_user_money(uid, "logindays", 1)
    elif not login_flag:
        money.set_user_money(uid, "logindays", 1)
    
    msg += msgg        
    msg += f'今日人品：{rp}\n'
    if rp >= 90 and rp <= 99 and not login_flag:
        luckygold_num = max(1, min(5, rp - 90))
        msg += f'额外获得了{luckygold_num}枚幸运币！\n'
        money.increase_user_money(uid, "luckygold", luckygold_num)
    elif rp == 100 and not login_flag:
        luckygold_num = 10 
        msg += f'额外获得了{luckygold_num}枚幸运币！恭喜~\n'
        money.increase_user_money(uid, "luckygold", luckygold_num)
    elif rp == 999 and not login_flag:
        luckygold_num = 20        
        msg += f'恭喜！请收下这{luckygold_num}枚幸运币！\n'
        money.increase_user_money(uid, "luckygold", luckygold_num)

    if not login_flag:
        msg += f'{info}\n'
    msg += f'\n今日运势:\n{goodluck[good_value]}\n{badluck[bad_value]}\n'
    gold += (rp + 5 * luck_choice[0] - 2 * luck_choice[-1]) 
    if login_flag == 0:
        logindays = money.get_user_money(uid, "logindays")
        num = rp * 5 + birth_flag * 600 + event_flag * 400 + min(500, (logindays // 10) * 50)
        gold += birth_flag * 300 + event_flag * 200 + min(50, max(0, (logindays - 4) * 5))
        money.increase_user_money(uid, "starstone", num)
        money.increase_user_money(uid, 'gold', gold)
        money.set_user_money(uid, "last_login", int(f'{months}0{days}'))
        money.set_user_money(uid, "rp", h)
        msg += f'{username}已经连续签到{logindays}天，额外获得{min(500, (logindays // 10) * 50)}颗星星与{min(50, max(0, (logindays - 4) * 5))}枚硬币~\n'
        msg += f'今日签到获得了{num}颗星星与{gold}枚金币~'
   

    return msg
       
