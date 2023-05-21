import asyncio
import io
import random
import time
from datetime import datetime
import os
import aiohttp
from .. import money
from ..build_image import BuildImage
import hoshino
from .color_convert import lab2rgb
from .._R import imgPath


debug_mode = 0  # 调试模式
add_watermark = 0  # 调试模式是否添加水印
debug_login_flag = 0  # 处于调试模式时签到标志
save_image_mode = 0  # 将签到卡片保存到本地
debug_background = 'Background2.jpg'  # 用于调试模式的图片

random_string = 'ę‘†č„±ę‰€ę‰č¨·å…°ē„å¤§å˛‹å¤©äø»ę•™č‰ŗęÆē„ę¯ē¼ļ¼č¨·å…°äŗŗåÆ¹č‰ŗęÆē„é‰´čµ¸å›å¾—ä»�ę¸é«ć€‚é¸ē¯€č´øę“ē„å¸‘å±•å’ē»¸ęµˇē„ē¹č¨£ļ¼č¨·å…°čæˇę¯�äŗ†č‡Ŗå·±ē„ā€é»„é‡‘å¹´ä»£ā€¯ļ¼åę—¶å¼•čµ·äŗ†ę–‡å–ę„¸čÆ†ē„č§‰é†’å’č‡Ŗäæ�ē„é«ę¶Øć€‚ē„¶č€ļ¼å·´ę´›å…‹é£ˇę ¼ē„ē¹č¨£å’å¤©äø»ę•™ę•™ä¹‰ē„ååØļ¼äøˇč‡Ŗę‘å¦å®å’č‚å¶ē„ę–°ę•™ē†č®ŗęŖē„¶äø¨åć€‚é™¤äŗ†å¸—å§”ę‰å›ä½č‚–å¸ē”»ä»�å¤–ļ¼č‰ŗęÆå®¶ä»¬å¹¶ę²�ę‰ēę£ē„ē›®ē„ļ¼ä»–ä»¬ē„äø“äøå°ä½¨ä¹å²å²å¸Æå¨±ć€‚'

backgroundList = ['Background1.jpg', 'Background2.jpg', 'Background3.jpg', 'Background4.jpg', 'Background5.jpg',
                  'Background6.jpg', 'Background7.jpg', 'Background8.jpg', 'Background9.jpg', 'Background10.jpg',
                  'Background11.jpg', 'Background12.jpg', 'Background13.jpg', 'Background14.jpg']

hoshi_bg_list = ['Background-hoshi-1.jpg', 'Background-hoshi-2.jpg', 'Background-hoshi-3.jpg', 'Background-hoshi-4.jpg',
                 'Background-hoshi-5.jpg']

extra_bg_list = ['Background_extra.jpg']

goodluck = ['宜 抽卡', '宜 干饭', '宜 摸鱼', '宜 刷副本',
            '宜 女装', '宜 打游戏', '宜 刷b站', '宜 看涩图',
            '宜 逛街', '宜 好好学习', '宜 搓麻将', '宜 工作',
            '宜 点外卖', '宜 水群', '宜 听音乐', '宜 背单词',
            '宜 做作业', '宜 刷抖音', '宜 睡觉', '宜 刷剧'
            ]

badluck = ['忌 抽卡上头', '忌 躺平', '忌 摸鱼', '忌 刷副本',
           '忌 女装', '忌 打游戏', '忌 刷b站', '忌 看涩图',
           '忌 逛街', '忌 学习', '忌 搓麻将', '忌 摆烂',
           '忌 点外卖', '忌 水群', '忌 听音乐', '忌 背单词',
           '忌 做作业', '忌 刷抖音', '忌 睡懒觉', '忌 刷剧', '忌 无'
           ]

birth_list = ["0808"
              ]

member_list = ["冰祈"
               ]

event_list = ['0101', '0122', '0205', '0214', '0308', '0401', '0405', '0501',
              '0601', '0622', '0701', '0801', '0822', '0929', '1001',
              '1010', '1011', '1101', '1111', '1224', '1225'
              ]

event_name_list = ['元旦节', '春节', '元宵节', '情人节', '妇女节', '愚人节', '清明节', '劳动节',
                   '儿童节', '端午节', '建党节', '建军节', '七夕节', '中秋节', '国庆节',
                   '萌节', '萝莉节', '万圣节', '光棍节', '平安夜', '圣诞节'
                   ]

week_list = ["日", "一", "二", "三", "四", "五", "六"]

srcpath = os.path.join(imgPath, 'icelogin/src')


async def creep_img(session, url, uid):  # 异步爬取
    imgname = f'{uid}.jpg'
    async with session.get(url) as r:
        content = await r.read()
        return content


def _hash():
    days = random.randint(10000000, 99999999)
    return days >> 8


def check_str_len(string: str):
    lenTxt = len(string)
    lenTxt_utf8 = len(string.encode('utf-8'))
    size = int((lenTxt_utf8 - lenTxt)/2 + lenTxt)
    return size


def luck_choice(which):  # 获取宜忌索引
    good_list_length = len(goodluck)
    bad_list_length = len(badluck)
    good_choice = random.choice(range(0, good_list_length))
    bad_choice = random.choice(range(0, bad_list_length))
    if which == 0:
        return good_choice
    elif which == 1:
        return bad_choice
    else:
        return 0


def feed_back(value):
    if value == 0:
        info = f"QAQ冰祈...冰祈不是故意的..."
    elif value < 20:
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
    else:
        info = f"999！！是隐藏的999运势！！！"
    return info


async def as_login_v3(uid, username, qqname, nick_flag):
    # === 初始化 ===
    list_len = len(goodluck)  # 黄历表长度
    festival_msg = ''  # 节日提示
    birthday_msg = ''  # 生日提示
    login_flag_msg = ''  # 已经签到的提示
    date_msg = ''  # 日期提示
    name_msg = ''  # 姓名提示
    good_luck_msg = ''  # 运势提示 宜
    bad_luck_msg = ''  # 运势提示 忌
    extra_msg = ''  # 首次签到的提示
    rp_colormap = (0, 0, 0)  # 人品色板
    luckygold_msg = ''  # 总收益中幸运币提示
    total_get_msg = ''  # 今日签到总收益提示

    # 延迟6小时
    current_time = time.localtime(time.time()-21600)
    days = int(time.strftime("%d", current_time))  # 日期-日
    months = int(time.strftime("%m", current_time))  # 日期-月
    week = int(time.strftime("%w", current_time))  # 日期-礼拜

    last_login = int(money.get_user_money(uid, "last_login"))  # 是否最近签到
    gold = 50  # 签到增加的基础金币
    if not debug_mode:
        login_flag = 1 if int(f'{months}0{days}') == last_login else 0  # 是否已签到
    else:
        login_flag = debug_login_flag

#    birth_flag, event_flag = get_day(days, months, login_flag)  # 节日标志
    # === 节日事件与生日事件 === birth_flag, event_fag ===
    flag_day = str(days) if days > 9 else f'0{str(days)}'
    flag_month = str(months) if months > 9 else f'0{str(months)}'
    flag = flag_month + flag_day
    i = 0
    birth_flag = 0
    event_flag = 0
    for birth in birth_list:
        if flag == birth:
            birth_flag = 1
            birthday_msg = f'{member_list[i]}的生日'
            if login_flag == 0:
                extra_msg += f'☆ 星星+600 (生日)\n☆ 金币+300 (生日)\n'
            break
        i += 1
    i = 0
    for event in event_list:
        if flag == event:
            event_flag = 1
            festival_msg = f'{event_name_list[i]}'
            if login_flag == 0:
                extra_msg += f'☆ 星星+400 (节日)\n☆ 金币+200 (节日)\n'
            break
        i += 1

    if not login_flag:
        money.increase_user_money(uid, "logindays", 1)  # 签到天数

    # === 今日人品值 ===
    h = int(money.get_user_money(uid, "rp")) if login_flag else _hash()  # 如果已经签过到，获取今日的人品值，范围0~100
    _h = h
    rp = _h % 101

    info = feed_back(rp)  # 人品吐槽

    # === 获取今日宜忌 ===
    good_todo_index = int(money.get_user_money(uid, "goodluck")) if login_flag else luck_choice(0)
    bad_todo_index = int(money.get_user_money(uid, "badluck")) if login_flag else luck_choice(1)
    if good_todo_index == bad_todo_index:  # 避免相等
        bad_todo_index += 1
    good_luck_msg = goodluck[good_todo_index]  # 宜忌
    bad_luck_msg = badluck[bad_todo_index]  # 宜忌

    # === 幸运币 ===
    if 90 <= rp <= 99 and not login_flag:
        luckygold_num = max(1, min(5, rp - 90))
        extra_msg += f'☆ 幸运币+{luckygold_num} (人品)\n'  # 幸运币
        luckygold_msg += f'☆ 幸运币+{luckygold_num}\n'
        money.increase_user_money(uid, "luckygold", luckygold_num)
    elif rp == 100 and not login_flag:
        luckygold_num = 10
        extra_msg += f'☆ 幸运币+{luckygold_num} (人品)\n'  # 幸运币
        luckygold_msg += f'☆ 幸运币+{luckygold_num}\n'
        money.increase_user_money(uid, "luckygold", luckygold_num)
    elif rp == 999 and not login_flag:
        luckygold_num = 20
        extra_msg += f'☆ 幸运币+{luckygold_num} (人品)\n'  # 幸运币
        luckygold_msg += f'☆ 幸运币+{luckygold_num}\n'
        money.increase_user_money(uid, "luckygold", luckygold_num)

    gold += rp
    logindays = money.get_user_money(uid, "logindays")
    star_add = min(500, (logindays // 10) * 50)
    gold_add = min(100, max(0, (logindays // 10) * 5))

    # === 日期+签到天数 ===
    date_msg = f'{months}月{days}日星期{week_list[week]}   已签到{logindays}天'

    # === 签到金额到账 ===
    if login_flag == 0:
        rdint = random.randint(1, 11)
        if money.get_user_background(uid)['mode'] != 2:
            if int(rdint) >= 8:  # 是否使用hoshi背景
                money.set_user_background(uid, random.choice(hoshi_bg_list))
                money.set_user_bg_mode(uid, 1)
            else:
                money.set_user_background(uid, random.choice(backgroundList))
                money.set_user_bg_mode(uid, 0)
        num = rp * 5 + birth_flag * 600 + event_flag * 400 + star_add
        gold += birth_flag * 300 + event_flag * 200 + gold_add
        money.increase_user_money(uid, "starstone", num)  # 星星
        money.increase_user_money(uid, 'gold', gold)  # 金币
        money.set_user_money(uid, "last_login", int(f'{months}0{days}'))
        money.set_user_money(uid, "rp", h)
        money.set_user_money(uid, "goodluck", good_todo_index)
        money.set_user_money(uid, "badluck", bad_todo_index)


        # === 总计获得与累计签到额外奖励提示 ===
        total_get_msg = f'☆ 星星+{num}\n☆ 金币+{gold}\n{luckygold_msg}'
        if logindays >= 10:
            extra_msg += f'☆ 星星+{star_add} (累签)\n☆ 金币+{gold_add} (累签)\n'

    if int(uid) == 80000000:  # 如果是匿名
        rp = -1
        info = '  Vanitas vanitatum,Et omnia vanitas.'
        good_luck_msg = '宜 取消匿名'
        bad_luck_msg = '忌 匿名'
        date_msg = f'{months}月{days}日星期{week_list[week]}'
        total_get_msg = f'△ 无'
        extra_msg = ''
        login_flag = 0


# ------> 下面开始绘图 <------
    money.check_mode(uid)
    user_bg = money.get_user_background(uid)
    # === 背景部分 ===
    if not debug_mode:
        if user_bg['mode'] == 2:
            border = 2
            is_bold = True
            user_bg_choose = f"customize/{user_bg['custom']}"
            imageFile = os.path.join(srcpath, user_bg_choose)
            bg = BuildImage(0, 0, font_size=30, background=os.path.join(srcpath, 'whiteboard.jpg'), font = 'HYShiGuangTiW_0.ttf')
            cstm_bg = BuildImage(0, 0, font_size=30, background=imageFile, font = 'HYShiGuangTiW_0.ttf')
            if cstm_bg.w > cstm_bg.h * 16 / 9:
                cstm_bg.resize(ratio = 540 / cstm_bg.h)
            else:
                cstm_bg.resize(ratio = 960 / cstm_bg.w)
            bg.paste(cstm_bg, (int(480 - cstm_bg.w / 2), int(270 - cstm_bg.h / 2)), True)
            mask = BuildImage(0, 0, font_size=30, background=os.path.join(srcpath, 'login_background_custom.png'), font = 'HYShiGuangTiW_0.ttf')
            bg.paste(mask, (0, 0), True)
        else:
            border = 0
            is_bold = False
            if user_bg['default']:
                user_bg_choose = user_bg['default']
            else:
                user_bg_choose = random.choice(backgroundList)
                money.set_user_background(uid, user_bg_choose)
                money.set_user_bg_mode(uid, 0)

            if int(uid) == 80000000:
                user_bg_choose = extra_bg_list[0]

            imageFile = os.path.join(srcpath, user_bg_choose)
            bg = BuildImage(0, 0, font_size=30, background=imageFile, font = 'HYShiGuangTiW_0.ttf')

    else:
        border = 0
        is_bold = True
        imageFile = os.path.join(srcpath, random.choice(hoshi_bg_list))
        bg = BuildImage(0, 0, font_size=30, background=imageFile, font = 'HYShiGuangTiW_0.ttf')

    # === 头像部分 ===
    imageUrl = f'https://q1.qlogo.cn/g?b=qq&nk={uid}&src_uin=www.jlwz.cn&s=0'
    async with aiohttp.ClientSession() as session:
        profile_img = await creep_img(session, url = imageUrl, uid = uid)
    iconFile = io.BytesIO(profile_img)
    icon = BuildImage(0, 0, background = iconFile)
    w, h = icon.size
    icon.resize(ratio = 100 / w)
    icon.circle()
    bg.paste(icon, (23, 23), True)

    # === 日期+累计签到部分 ===
    date_text = BuildImage(0, 0, plain_text=date_msg, font_size=30, font='nyan.ttf',
                           font_color=(77, 83, 149), stroke_width = border, stroke_fill=(255, 255, 255))
    bg.paste(date_text, (23, 490), True)

    # === 用户名部分 ===
    size = check_str_len(qqname)
    if size >= 20:
        final_txt = ''
        for i in qqname:
            final_txt += i
            txt_size = check_str_len(final_txt)
            if txt_size >= 20:
                break
    else:
        final_txt = qqname
    name_text = BuildImage(0, 0, plain_text=final_txt, font_size=30, font='yz.ttf',
                           font_color=(77, 83, 149), stroke_width = border, stroke_fill=(255, 255, 255))
    if nick_flag:
        nick_msg = f"欢迎回来，{username}~"
    else:
        nick_msg = f"欢迎回来~"

    if int(uid) == 80000000:
        nick_msg = f"......"

    nick_text = BuildImage(0, 0, plain_text=nick_msg, font_size=25, font='yz.ttf',
                           font_color=(77, 83, 149), stroke_width = border, stroke_fill=(255, 255, 255))
    bg.paste(name_text, (190, 30), True)
    bg.paste(nick_text, (190, 75), True)

    # === 节日提醒部分 ===
    if festival_msg and birthday_msg:
        jieri_msg = f'今天是{festival_msg}和{birthday_msg}~'
    elif festival_msg:
        jieri_msg = f'今天是{festival_msg}~'
    elif birthday_msg:
        jieri_msg = f'今天是{birthday_msg}~'
    else:
        jieri_msg = ''
    if jieri_msg:
        jieri_image = BuildImage(0, 0, plain_text=jieri_msg, font_size=30, font='HYShiGuangTiW_0.ttf',
                                 font_color=(77, 83, 149), stroke_width = border, stroke_fill=(255, 255, 255))
        w, h = jieri_image.size
        bg.paste(jieri_image, (int(215 - w / 2), 157), True)

    # === 运势部分 ===
    bg.text((49, 259), good_luck_msg, (77, 83, 149), stroke_width = border, stroke_fill=(255, 255, 255))
    bg.text((261, 259), bad_luck_msg, (77, 83, 149), stroke_width = border, stroke_fill=(255, 255, 255))

    # === 人品部分 ===
    if rp < 0:
        rp_colormap = (244, 93, 129)
    elif rp == 0:
        rp_colormap = (100, 100, 100)
    elif rp <= 100:
        rp_colormap = lab2rgb(86, 80 - rp * 1.6, 4)
    else:
        rp_colormap = (68, 118, 244)
    rp_number = BuildImage(0, 0, plain_text=str(rp), font_size=60, font='nyan.ttf',
                           font_color=rp_colormap, stroke_width= border, stroke_fill=(255, 255, 255))
    rp_w, rp_h = rp_number.size
    bg.paste(rp_number, (int(215 - rp_w / 2), 356), True)
    infoImage = BuildImage(0, 0, plain_text=info, font_size=25, font='HYShiGuangTiW_0.ttf',
                           font_color=rp_colormap, stroke_width=border, stroke_fill=(255, 255, 255))
    info_w, info_h = infoImage.size
    bg.paste(infoImage, (int(215 - info_w / 2), 424), True)

    # === 额外奖励 ===
    if not login_flag:
        bg.text((590, 70), extra_msg, (77, 83, 149), stroke_width = 2, stroke_fill=(255, 255, 255, 1))
        if extra_msg:
            bonusIconFile = os.path.join(srcpath, 'extra_bonus.png')
            bonus_icon = BuildImage(0, 0, background = bonusIconFile)
            bg.paste(bonus_icon, (551, 7), True)

    # === 总计获得 ===
        totalIconFile = os.path.join(srcpath, 'text_block_new.png')
        total_bg = BuildImage(0, 0, background = totalIconFile)
        bg.paste(total_bg, (553, 255), True)
        final_text = BuildImage(0, 0, plain_text=total_get_msg, font_size=25, font='HYShiGuangTiW_0.ttf', font_color=(77, 83, 149))
        bg.text((618, 338), total_get_msg, (77, 83, 149), stroke_width=2, stroke_fill=(255, 255, 255, 1))

    # === 已签到之后 ===
    else:
        if user_bg['mode'] == 2:
            loginFlagIconFile = os.path.join(srcpath, 'login_flag_custom.png')
        elif user_bg['mode'] == 1:
            loginFlagIconFile = os.path.join(srcpath, 'login_flag_hoshi.png')
        else:
            loginFlagIconFile = os.path.join(srcpath, 'login_flag.png')
        login_flag_img = BuildImage(0, 0, background= loginFlagIconFile)
        bg.paste(login_flag_img, (373, 174), True)

    # === 添加水印 ===
    if debug_mode and add_watermark:
        waterMarkFile = os.path.join(srcpath, 'watermark.png')
        watermark = BuildImage(0, 0, background = waterMarkFile)
        bg.paste(watermark, (102, 102), True)

    # === 图片最终处理，转base64，返回值 ===
    if save_image_mode:
        bg.save(path = os.path.join(os.path.dirname(__file__), f'cache/{uid}-{login_flag}.jpg'))
    imageToSend = f"[CQ:image,file=base64://{bg.pic2bs4()}]"
    hoshino.logger.info('绘制签到图片完成')
    return imageToSend


async def get_purse(uid, user_name, guild_flag = 0):
    normal_bg_list = ['purse_01.jpg', 'purse_02.jpg', 'purse_05.jpg', 'purse_09.jpg']
    normal_coin_bg = 'purse_03.jpg'
    normal_star_bg = 'purse_04.jpg'
    many_coin_bonus = 'purse_06.jpg'
    no_coin_bouns = 'purse_07.jpg'
    coin_1w_bonus = 'purse_15.jpg'
    coin_2w_bonus = 'purse_20.jpg'
    coin_3w_bonus = 'purse_21.jpg'
    coin_4w_bonus = 'purse_22.jpg'
    many_lucky_bonus = 'purse_08.jpg'
    lucky_100_bonus = 'purse_19.jpg'
    many_star_bouns = 'purse_10.jpg'
    no_star_bonus = 'purse_13.jpg'
    star_10w_bonus = 'purse_14.jpg'
    time_limit_bonus = 'purse_11.jpg'
    night_limit_bonus = 'purse_12.jpg'
    heart_bonus = 'purse_16.jpg'
    fish_nonus = 'purse_17.jpg'
    zheli_bonus = 'purse_18.jpg'

    anony_bonus = 'purse_anony.jpg'  # 匿名者

    money.load_user_money()
    msg = ''
    key_list = ["金币", "幸运币", "星星"]
    for key in key_list:
        msg += f'\n{key} : {money.get_user_money(uid, money.translatename(key))}'

    font_color = (116, 88, 86)

    # 背景
    user_starstone = money.get_user_money(uid, 'starstone')
    user_gold = money.get_user_money(uid, 'gold')
    user_lucky = money.get_user_money(uid, 'luckygold')
    choose_list = normal_bg_list[:]
    # === 普通解锁背景
    if user_gold > 300:
        choose_list.append(normal_coin_bg)
    if user_starstone > 15000:
        choose_list.append(normal_star_bg)
    # === 星星解锁背景
    if 25000 < user_starstone < 100000 and random.randint(1, 101) >= 50:
        choose_list.append(many_star_bouns)
    if user_starstone >= 100000:
        choose_list.append(star_10w_bonus)
    if user_starstone < 4000:
        choose_list.append(no_star_bonus)
    # === 金币解锁背景
    if user_gold >= 40000:
        choose_list.append(coin_4w_bonus)
    elif user_gold >= 30000:
        choose_list.append(coin_3w_bonus)
    elif user_gold >= 20000:
        choose_list.append(coin_2w_bonus)
    elif user_gold >= 10000:
        choose_list.append(coin_1w_bonus)
    if 1000 < user_gold < 10000 and random.randint(1, 101) >= 50:
        choose_list.append(many_coin_bonus)
    if user_gold < 75:
        choose_list.append(no_coin_bouns)
    # === 幸运币解锁背景
    if 20 < user_lucky < 100 and random.randint(1, 101) >= 50:
        choose_list.append(many_lucky_bonus)
    if user_lucky >= 100:
        choose_list.append(lucky_100_bonus)
    # === 其他彩蛋背景
    bonus_point = random.randint(1, 101)
    if bonus_point > 95:
        choose_list.append(heart_bonus)
    elif bonus_point < 6:
        choose_list.append(fish_nonus)
    elif 47 < bonus_point < 53:
        choose_list.append(fish_nonus)
    # === 夜间彩蛋背景
    now = datetime.now()
    hour = now.strftime('%H')
    if 1 < int(hour) < 5:
        choose_list.append(night_limit_bonus)
    purse_choose = random.choice(choose_list)

    if int(uid) == 80000000:  # 匿名者

        purse_choose = 'purse_anony.jpg'
        font_color = (255, 255, 255)
        user_starstone = ''.join(random.sample(random_string, random.randint(3, 5))) if random.randint(1, 101) >= 10 else '9999999'
        user_gold = ''.join(random.sample(random_string, random.randint(3, 5))) if random.randint(1, 101) >= 10 else '999999'
        user_lucky = ''.join(random.sample(random_string, random.randint(3, 5))) if random.randint(1, 101) >= 10 else '9999999'

    imageFile = os.path.join(srcpath, purse_choose)
    bg = BuildImage(0, 0, font_size=30, background=imageFile, font = 'yz.ttf')

    # === 头像 ===
    imageUrl = f'https://q1.qlogo.cn/g?b=qq&nk={uid}&src_uin=www.jlwz.cn&s=0'
    async with aiohttp.ClientSession() as session:
        profile_img = await creep_img(session, url = imageUrl, uid = uid)
    iconFile = io.BytesIO(profile_img)
    icon = BuildImage(0, 0, background = iconFile)
    w, h = icon.size
    icon.resize(ratio = 80 / w)
    icon.circle()
    bg.paste(icon, (20, 18), True)

    # === 昵称 ===
    if len(user_name) >= 10:
        user_name = f'{user_name[:9]}...'
    name_text = BuildImage(0, 0, plain_text=f'{user_name}的钱包', font_size=35, font='yz.ttf', font_color=font_color)
    bg.paste(img = name_text, pos = (122, 25), alpha=True)

    # === 钱 ===
    star_text = BuildImage(0, 0, plain_text=f'星星 {user_starstone}颗', font_size=30, font='yz.ttf', font_color=font_color)
    bg.paste(img = star_text, pos = (160, 128), alpha=True)
    gold_text = BuildImage(0, 0, plain_text=f'金币 {user_gold}枚', font_size=30, font='yz.ttf', font_color=font_color)
    bg.paste(img = gold_text, pos = (280, 187), alpha=True)
    lucky_text = BuildImage(0, 0, plain_text=f'幸运币 {user_lucky}枚', font_size=30, font='yz.ttf', font_color=font_color)
    bg.paste(img = lucky_text, pos = (100, 245), alpha=True)
    # 结束
    if save_image_mode:
        bg.save(path = os.path.join(os.path.dirname(__file__), f'cache/{uid}.jpg'))
    imageToSend = f"[CQ:image,file=base64://{bg.pic2bs4()}]"
    hoshino.logger.info('绘制钱包图片完成')
    return imageToSend


async def dl_save_image(url, uid):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            content = await r.read()
            with open(os.path.join(srcpath, f'customize/{uid}.jpg'), 'wb') as f:
                f.write(content)
    money.set_user_background(uid, f'{uid}.jpg', 'custom')
    money.set_user_bg_mode(uid, mode = 2)


def del_custom_bg(uid):
    if not os.path.exists(os.path.join(os.path.join(srcpath, f'customize/{uid}.jpg'))):
        return
    os.remove(os.path.join(os.path.join(srcpath, f'customize/{uid}.jpg')))
    money.set_user_background(uid, '', 'custom')
    if 'hoshi' in money.get_user_background(uid)['default']:
        money.set_user_bg_mode(uid, mode = 1)
    else:
        money.set_user_bg_mode(uid, mode = 0)


if __name__ == '__main__':
    qq_list = [10001]
    asyncio.get_event_loop().run_until_complete(as_login_v3(qq_list[0], '名字', '无', 0))
