from hoshino import Service
from ..build_image import BuildImage
from .._R import imgPath, check_path_exists
import aiohttp
import os
import re
import random

path = os.path.join(imgPath, 'chat_scrshot/picture')
srcpath = os.path.join(imgPath, 'chat_scrshot/src')

sv = Service("伪造聊天记录", enable_on_default=True)


@sv.on_prefix(".qys")
@sv.on_prefix("。qys")
@sv.on_prefix("#qys")
@sv.on_prefix("qys")
@sv.on_prefix(".qtest")
async def jia_xiao_xi(bot, ev):
    message = ev.message.extract_plain_text().strip()
    match = re.findall(r'(?:\[CQ:at,qq=(\d+)\])', ev.raw_message)
    if not match:
        messageSplit = message.split(" ", 1)
        uid = messageSplit[-1]  # 要么直接输入QQ号
        if not uid.isdigit():
            uid = ev.user_id  # 没有QQ号则使用触发者的QQ
        else:
            message = messageSplit[0]
    else:
        uid = match[0]  # 要么匹配到艾特
    message_cut = message.split("#")

    if uid in [2530075673, 3625681236]:
        return

    try:
        userInfo = await bot.get_group_member_info(user_id=uid, group_id=ev.group_id, no_cache=True)
    except:
        userInfo = await bot.get_stranger_info(user_id=uid, no_cache=True)
    bg = BuildImage(0, 0, background=os.path.join(srcpath, 'background.jpg'))

    # === 头像部分 ===
    imageUrl = f'https://q1.qlogo.cn/g?b=qq&nk={uid}&src_uin=www.jlwz.cn&s=0'
    async with aiohttp.ClientSession() as session:
        profile_img = await creep_img(session, url = imageUrl, uid = uid)
    iconFile = os.path.join(path, profile_img)
    icon = BuildImage(0, 0, background = iconFile)
    w, h = icon.size
    icon.resize(w = 108, h = 108)
    icon.circle()

    # === 头衔部分 ===
    # userLevel = userInfo['level']  # 等级没用，改成随机的吧
    userLevel = random.randrange(1, 101)
    try:
        userTitle = userInfo['title']
        role = userInfo['role']
    except:  # 允许使用群外人员
        userTitle = ''
        role = 'member'
    if userTitle or role != 'member':
        level_text = BuildImage(0, 0, plain_text=f"LV{userLevel} ",
                                font_size=24, font_color=(255, 255, 255), font='extra-bold-italia.ttf')
    else:

        level_text = BuildImage(0, 0, plain_text=f"LV{userLevel}",
                                font_size=24, font_color=(255, 255, 255), font='extra-bold-italia.ttf')
    level_w, level_h = level_text.size
    if not userTitle:
        if role == 'admin':
            title_text = BuildImage(0, 0, plain_text=f"管理员",
                                    font_size=32, font_color=(255, 255, 255), font='simhei2.ttf')
        elif role == 'owner':
            title_text = BuildImage(0, 0, plain_text=f"群主",
                                    font_size=32, font_color=(255, 255, 255), font='simhei2.ttf')
        else:
            title_text = BuildImage(0, 0, plain_text=f"",
                                    font_size=32, font_color=(255, 255, 255), font='simhei2.ttf')
    else:
        title_text = BuildImage(0, 0, plain_text=f"{userTitle}",
                                font_size=32, font_color=(255, 255, 255), font='simhei2.ttf')
    title_w, title_h = title_text.size
    if role == 'owner':
        badge_bg = os.path.join(srcpath, 'badge_owner.jpg')
    elif role == 'admin':
        badge_bg = os.path.join(srcpath, 'badge_admin.jpg')
    else:
        if userTitle:
            badge_bg = os.path.join(srcpath, 'badge_title.jpg')
        else:
            badge_bg = os.path.join(srcpath, 'badge_member.jpg')
    bg_badge = BuildImage(0, 0, font_size=24, background=badge_bg, font = 'HYShiGuangTiW_0.ttf')
    bg_badge.resize(w = level_w + title_w + 16, h = 38)
    bg_badge.paste(level_text, (8, 10), True)
    if userTitle or role != 'member':
        bg_badge.paste(title_text, (8 + level_w, 2), True)
    bg_badge.circle_corner(radii=8)  # 完成绘制

    # === 昵称与头衔贴一块 ===
    userName = userInfo['nickname']
    name_text = BuildImage(0, 0, plain_text=userName,
                           font_size=32, font_color=(138, 138, 148), font = 'AdobeHeitiStd-Regular.otf')  # 昵称
    name_w, name_h = name_text.size
    total_weight = level_w + title_w + 16 + 8 + name_w + 8
    bg_badge.crop((0, 0, total_weight, 38))
    bg_badge.paste(name_text, (level_w + title_w + 16 + 8, 2), True)
    badge_w, badge_h = bg_badge.size

    # === 绘制聊天记录图片 ===

    box = []
    weight = []

    await bot.send(ev, '正在制作截图中~')

    for message in message_cut:
        if len(message) > 40:
            await bot.send(ev, '字数太多了>_<')
            break
        if len(message) == 0:
            await bot.send(ev, '有空气泡噢~')
            break

        # === 气泡部分 ===
        content_text = BuildImage(0, 0, plain_text= message,
                                  font_size=45, font_color=(0, 0, 0), font='simhei.ttf')
        content_w, content_h = content_text.size
        bg_left = BuildImage(0, 0, background=os.path.join(srcpath, 'bubble_left.png'))
        bg_middle = BuildImage(0, 0, background=os.path.join(srcpath, 'bubble_middle.png'))
        bg_right = BuildImage(0, 0, background=os.path.join(srcpath, 'bubble_right.png'))
        bg_middle.resize(w = max(content_w - 8, 10), h = 116)
        bg_left.crop((0, 0, content_w + 107, 116))
        bg_left.paste(bg_middle, (66, 0), True)
        bg_left.paste(bg_right, (content_w + 44, 0), True)
        bg_left.paste(content_text, (54, 32), True)
        bubble_w, bubble_h = bg_left.size

        # === 把元素往背景上贴 ===
        bg = BuildImage(0, 0, background=os.path.join(srcpath, 'background.png'))
        bg.resize(w = 187 + max(25+badge_w, bubble_w), h = 229)
        local_weight = 187 + max(25+badge_w, bubble_w)
        weight.append(local_weight)
        bg.paste(icon, (38, 25), True)
        bg.paste(bg_badge, (184, 28), True)
        bg.paste(bg_left, (159, 87), True)
        box.append(bg)

    max_weight = max(weight)
    j = 0
    bg_final = BuildImage(0, 0, background=os.path.join(srcpath, 'background.png'))
    bg_final.resize(w = max_weight, h = 229 * len(message_cut))
    for bg_element in box:
        bg_final.paste(bg_element, (0, 229 * j - 10), True)
        j += 1

    # === 发送图片 ===
    bg_final.resize(ratio = 0.8)
    imageToSend = f"[CQ:image,file=base64://{bg_final.pic2bs4()}]"
    await bot.send(ev, imageToSend)


async def creep_img(session, url, uid):  # 异步爬取
    imgname = f'{uid}.jpg'
    async with session.get(url) as r:
        content = await r.read()
        with open(os.path.join(path, imgname), "wb") as f:
            f.write(content)
    return imgname

