import json
import os
import re

from PIL import Image

import hoshino

try:
    from ..build_image import BuildImage

    from .term_dict import *
    from .util import *
    from .._R import imgPath
except:
    import sys
    sys.path.append('../../koinoribot/')
    from build_image import BuildImage

    from term_dict import *
    from util import *
    from _R import imgPath

proxies = {'http': 'http://127.0.0.1:7890'}


from fuzzywuzzy import process

plugin_path = os.path.dirname(__file__)
baImgPath = os.path.join(imgPath, 'ba_wiki')
database_path = os.path.join(plugin_path, 'db')

students_url = "https://lonqie.github.io/SchaleDB/data/cn/students.json"
localization_cn_url = "https://lonqie.github.io/SchaleDB/data/cn/localization.json"
localization_jp_url = "https://lonqie.github.io/SchaleDB/data/jp/localization.json"
items_url = "https://lonqie.github.io/SchaleDB/data/cn/items.json"
furniture_url = "https://lonqie.github.io/SchaleDB/data/cn/furniture.json"
common_url = "https://lonqie.github.io/SchaleDB/data/common.json"
raids_url = "https://lonqie.github.io/SchaleDB/data/cn/raids.json"
enemies_url = "https://lonqie.github.io/SchaleDB/data/cn/enemies.json"

font_color_white = (255, 255, 255)
font_color_black = (0, 0, 0)
font_SC_Bold = 'NotoSansSC-Bold.otf'
font_SC = 'NotoSansSC-Medium.otf'
font_heiti = 'simhei2.ttf'
font_rothorn = 'extra-bold-italia.ttf'

mark_color = (255, 255, 255, 30)

localization_data = {}
debug_mode = 0


def update_db():
    """
        更新数据库
    """
    # hoshino.logger.info('更新碧蓝档案数据库...')

    archive = get_json_data(students_url)
    if archive:
        with open(os.path.join(database_path, 'students.json'), 'w', encoding='utf-8') as f:
            f.truncate(0)
            json.dump(archive, f, ensure_ascii=False, indent=2)
            print('学生数据拉取成功')
    else:
        print('学生数据拉取失败')

    archive = get_json_data(furniture_url)
    if archive:
        with open(os.path.join(database_path, 'furniture.json'), 'w', encoding='utf-8') as f:
            f.truncate(0)
            json.dump(archive, f, ensure_ascii=False, indent=2)
            print('家具数据拉取成功')
    else:
        print('家具数据拉取失败')
    archive = get_json_data(items_url)
    if archive:
        with open(os.path.join(database_path, 'items.json'), 'w', encoding='utf-8') as f:
            f.truncate(0)
            json.dump(archive, f, ensure_ascii=False, indent=2)
            print('道具数据拉取成功')
    else:
        print('道具数据拉取失败')
    archive = get_json_data(localization_cn_url)
    if archive:
        with open(os.path.join(database_path, 'localization.json'), 'w', encoding='utf-8') as f:
            f.truncate(0)
            json.dump(archive, f, ensure_ascii=False, indent=2)
            print('中文翻译数据拉取成功')
    else:
        print('中文翻译数据拉取失败')
    archive = get_json_data(raids_url)
    if archive:
        with open(os.path.join(database_path, 'raids.json'), 'w', encoding='utf-8') as f:
            f.truncate(0)
            json.dump(archive, f, ensure_ascii=False, indent=2)
            print('总力战boss数据拉取成功')
    else:
        print('总力战boss数据拉取失败')
    archive = get_json_data(enemies_url)
    if archive:
        with open(os.path.join(database_path, 'enemies.json'), 'w', encoding='utf-8') as f:
            f.truncate(0)
            json.dump(archive, f, ensure_ascii=False, indent=2)
            print('敌人数据拉取成功')
    archive = get_json_data(localization_jp_url)
    if archive:
        with open(os.path.join(database_path, 'localizationJP.json'), 'w', encoding='utf-8') as f:
            f.truncate(0)
            json.dump(archive, f, ensure_ascii=False, indent=2)
            print('日文翻译数据拉取成功')
    else:
        print('日文翻译数据拉取失败')
    archive = get_json_data(common_url)
    if archive:
        with open(os.path.join(database_path, 'common.json'), 'w', encoding='utf-8') as f:
            f.truncate(0)
            json.dump(archive, f, ensure_ascii=False, indent=2)
            print('当前活动数据拉取成功')
    else:
        print('当前活动数据拉取失败')

    # favor.json数据更新
    items_data = json.load(open(os.path.join(database_path, 'items.json'), encoding='utf-8'))
    favor_list = []
    for item in items_data:
        if item["Category"] == 'Favor':
            favor_list.append(item)
    with open(os.path.join(database_path, 'favor.json'), 'w', encoding='utf-8') as f:
        f.truncate(0)
        json.dump(favor_list, f, ensure_ascii=False, indent=2)
        print('礼物数据更新成功')

    student_data = json.load(open(os.path.join(database_path, 'students.json'), encoding='utf-8'))

    # 学生昵称更新
    '''nickname_data = json.load(open(os.path.join(database_path, 'students_nickname.json'), encoding='utf-8'))["CHARA_NAME"]
    for student in student_data:
        if str(student['Id']) not in nickname_data:
            nickname_data[str(student['Id'])] = [student['DevName'], student['Name']]
    with open(os.path.join(database_path, 'students_nickname.json'), 'w', encoding='utf-8') as f:
        f.truncate(0)
        json.dump({'CHARA_NAME': nickname_data}, f, ensure_ascii=False, indent=2)
    print('学生昵称更新成功')'''

    # 抽卡卡池更新
    _dict = {
        'pickup': [],
        'star3_0': [],
        'star3_1': [],
        'star3_2': [],
        'star2_0': [],
        'star2_1': [],
        'star2_2': [],
        'star1_0': [],
        'star1_1': [],
        'star1_2': []
    }
    common_data = json.load(open(os.path.join(database_path, 'common.json'), encoding='utf-8'))
    gacha_data = common_data['regions'][0]['current_gacha']
    _dict['pickup'] = list(gacha_data[0]['characters'])

    for student_dict in student_data:
        sort_list = f""
        _dict[f"star{student_dict['StarGrade']}_{student_dict['IsLimited']}"].append(student_dict['Id'])

    with open(os.path.join(database_path, 'gacha.json'), 'w', encoding='utf-8') as f:
        f.truncate(0)
        json.dump(_dict, f, ensure_ascii=False, indent=2)
    print('抽卡卡池更新成功')


def desc_type_transform(match):
    global localization_data
    buffName = localization_data["BuffName"]  # localization里的译文

    buff_types = {"b": "Buff_", "d": "Debuff_", "c": "CC_", "s": "Special_"}
    if match.group(1) not in buff_types:
        return match.group()

    buff_name = buff_types[match.group(1)] + match.group(2)
    # print(buff_name)
    if buff_name not in buffName.keys():
        return match.group()
    return buffName[buff_name]


parameters = []


def desc_param_transform(match):
    global parameters
    if not parameters:
        return "UNKNOWN"
    # print(parameters)
    lv1_param = parameters[int(match.group(1)) - 1][0] if parameters[int(match.group(1)) - 1][0] else 'none'
    lvmax_param = parameters[int(match.group(1)) - 1][-1] if parameters[int(match.group(1)) - 1][-1] else 'none'
    string = f'[Lv1:{lv1_param}→MAX:{lvmax_param}]'
    return string


def get_student_id(nickname):
    """
    获取学生id
    """
    student_list = json.load(open(os.path.join(database_path, 'students_nickname.json'), encoding="utf-8"))["CHARA_NAME"]
    most_fit_chara = ''
    fit_rate = 0
    for student_id, student_names in student_list.items():
        if nickname in student_names:
            return student_id
        else:
            student_id = process.extractOne(nickname, student_names)
            if student_id[-1] > fit_rate:
                most_fit_chara = student_id[0]
                fit_rate = student_id[-1]
    return [most_fit_chara, fit_rate]


def get_bgm_id(name: str, mode = 0):
    """
        mode = 0: 名称模糊匹配，mode = 1: ID模糊匹配
    """
    bgm_dict = json.load(open(os.path.join(database_path, 'bgm.json'), encoding='utf-8'))
    most_fit_bgm = ''
    fit_rate = 0
    fit_bgm_id = '01'
    if name in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        name = f'0{name}'
    if mode == 0:
        for bgm_id, name_list in bgm_dict.items():
            if name in name_list:
                fit_rate = 100
                return [bgm_id, name, fit_rate]
            elif name.lower() == bgm_id.lower():
                fit_rate = 100
                return [bgm_id, name_list[0], fit_rate]
            else:
                bgm_fit = process.extractOne(name, name_list)
                if bgm_fit[-1] > fit_rate:
                    most_fit_bgm = bgm_fit[0]
                    fit_rate = bgm_fit[-1]
                    fit_bgm_id = bgm_id
        return [fit_bgm_id, most_fit_bgm, fit_rate]



def image_exist_check(file_path, url):
    """
    检查图片是否缺失，缺失则获取图片
    """
    if not os.path.exists(file_path):
        hoshino.logger.info('downloading request image...')
        resp = requests.get(url = url, headers=headers, proxies=proxies).content
        with open(file_path, 'wb') as f:
            f.write(resp)


def get_student_info(student_id):
    """
    获取学生信息并进行处理
    """
    global localization_data, parameters
    student_id = int(student_id)

    '''if str.isdigit(str(student_id)):
        return None, None, None'''

    furniture_data = json.load(open(os.path.join(database_path, 'furniture.json'), encoding='utf-8'))
    student_data = json.load(open(os.path.join(database_path, 'students.json'), encoding='utf-8'))
    localization_data = json.load(open(os.path.join(database_path, 'localization.json'), encoding='utf-8'))
    favor_data = json.load(open(os.path.join(database_path, 'favor.json'), encoding='utf-8'))

    message_list = []

    base_info = get_item(student_data, "Id", student_id)  # 获取学生信息

    # 资料部分

    name = base_info['Name']
    fullName = f"{base_info['FamilyName']} {base_info['PersonalName']}"
    school = base_info['School']
    club = base_info['Club']
    age = base_info['CharacterAge']
    birthday = base_info['Birthday']
    hobby = base_info['Hobby']
    if '\n' in hobby:
        hobby.replace('\n', '')
    height = base_info['CharHeightMetric']
    cv = base_info['CharacterVoice']
    illustor = base_info['Illustrator'] + '/' + base_info['Designer'] if base_info['Illustrator'] != base_info['Designer'] else base_info['Illustrator'] # 插画与设计
    introduction = f"学生介绍：\n{base_info['ProfileIntroduction']}\n\n招募台词：\n{base_info['CharacterSSRNew']}"
    memoryLobby = base_info['MemoryLobby'][0]
    memoryLobbyBGM = base_info['MemoryLobbyBGM']
    furnitureInteractionList = base_info['FurnitureInteraction'][0]
    if furnitureInteractionList:
        furnitureInteraction = furnitureInteractionList[0]  # 可互动家具
    else:
        furnitureInteraction = 0

    # 属性信息

    starGrade = base_info['StarGrade']
    squadType = localization_data['SquadType'][base_info['SquadType']]  # 主力/支援
    tacticRole = base_info['TacticRole']  # 作用类别
    position = base_info['Position']  # 站位
    bulletType = base_info['BulletType']  # 攻击类型
    armorType = base_info['ArmorType']  # 防御类型
    streetBattleAdaptation = BattleAdaptation[base_info['StreetBattleAdaptation']],  # 街区战斗力
    outdoorBattleAdaptation = BattleAdaptation[base_info['OutdoorBattleAdaptation']],  # 户外战斗力
    indoorBattleAdaptation = BattleAdaptation[base_info['IndoorBattleAdaptation']],  # 室内战斗力
    weaponType = base_info['WeaponType']  # 武器类型
    equipment = base_info['Equipment'][:]
    stabilityPoint = base_info["StabilityPoint"]
    attackPower = f'{base_info["AttackPower1"]}→{base_info["AttackPower100"]}'
    healthPoint = f'{base_info["MaxHP1"]}→{base_info["MaxHP100"]}'
    defensePower = f'{base_info["DefensePower1"]}→{base_info["DefensePower100"]}'
    healPower = f'{base_info["HealPower1"]}→{base_info["HealPower100"]}'
    dodgePoint = base_info["DodgePoint"]
    accuracyPoint = base_info["AccuracyPoint"]
    criticalPoint = base_info["CriticalPoint"]
    criticalDamageRate = str(int(base_info["CriticalDamageRate"] / 100)) + "%"
    ammoCount = f'{base_info["AmmoCount"]}({base_info["AmmoCost"]})'
    ammoCost = base_info["AmmoCost"]
    range_ = base_info["Range"]
    regenCost = base_info["RegenCost"]

    # 绘图

    # 背景

    bg_name = base_info['CollectionBG']
    bg_file_path = baImgPath + f'/source/background/{bg_name}.jpg'
    image_exist_check(bg_file_path, f'https://raw.githubusercontent.com/lonqie/SchaleDB/main/images/background/{bg_name}.jpg')
    background = BuildImage(0, 0, font_size = 25, background = bg_file_path, font = 'yz.ttf')
    background.resize(ratio = 2)

    # 立绘

    portrait_name = base_info["DevName"]
    portrait_file_path = baImgPath + f'/source/student/portraitpng/Portrait_{portrait_name}.png'
    if not os.path.exists(portrait_file_path):
        portrait_file_path_webp = baImgPath + f'/source/student/portrait/Portrait_{portrait_name}.webp'
        image_exist_check(portrait_file_path_webp, f'https://raw.githubusercontent.com/lonqie/SchaleDB/main/images/student/portrait/Portrait_{portrait_name}.webp')
        portrait_png = Image.open(portrait_file_path_webp)
        portrait_png.load()
        portrait_png.save(portrait_file_path)
    portrait = BuildImage(0, 0, background = portrait_file_path)
    portrait.resize(ratio = 1104 / portrait.h)
    background.paste(img = portrait, pos = (int(600 - portrait.w / 2), max(0, int(600 - portrait.h / 2))), alpha = True)

    # 左下角部分

    left_bottom_template = BuildImage(0, 0, background = baImgPath + '/source/cardsrc/left_bottom_part.png',
                                      font = font_SC_Bold, font_size = 50)
    # 名字
    left_bottom_template.text((41, 12), name, (255, 255, 255))
    fullName_text = BuildImage(0, 0, plain_text = fullName, font = font_SC_Bold, font_size = 40, font_color = font_color_white)
    left_bottom_template.paste(img = fullName_text, pos = (270, 86), alpha = True)
    # text_student_name = BuildImage(0, 0, plain_text = name, font_size = 50, font = 'simhei2.ttf', font_color = (255, 255, 255))
    # left_bottom_template.paste(img = text_student_name, pos = (41, 27), alpha = True)
    # 星级，作用类型
    star_icon = BuildImage(0, 0, background = baImgPath + f'/source/ui/Common_Icon_Formation_Star_R{starGrade}.png')
    left_bottom_template.paste(img = star_icon, pos = (42, 95), alpha = True)
    squadType_icon = BuildImage(0, 0, background = baImgPath + f'/source/cardsrc/{squadType}.png')
    left_bottom_template.paste(img = squadType_icon, pos = (104, 108), alpha = True)
    # 作用类别、站位、攻击类型、防御类型
    tacticRole_icon = BuildImage(0, 0, background = baImgPath + f'/source/cardsrc/{tacticRole}.png')
    left_bottom_template.paste(img = tacticRole_icon, pos = (37, 174), alpha = True)
    position_icon = BuildImage(0, 0, background = baImgPath + f'/source/cardsrc/{position}.png')
    left_bottom_template.paste(img = position_icon, pos = (37, 249), alpha = True)
    bulletType_icon = BuildImage(0, 0, background = baImgPath + f'/source/cardsrc/{bulletType}.png')
    left_bottom_template.paste(img = bulletType_icon, pos = (280, 174), alpha = True)
    armorType_icon = BuildImage(0, 0, background = baImgPath + f'/source/cardsrc/{armorType}.png')
    left_bottom_template.paste(img = armorType_icon, pos = (280, 249), alpha = True)
    # 场地适性
    streetAdaption_icon = BuildImage(0, 0, background = baImgPath + f'/source/ui/Ingame_Emo_Adaptresult{streetBattleAdaptation[0]}.png')
    outdoorAdaptation_icon = BuildImage(0, 0, background = baImgPath + f'/source/ui/Ingame_Emo_Adaptresult{outdoorBattleAdaptation[0]}.png')
    indoorAdaptation_icon = BuildImage(0, 0, background = baImgPath + f'/source/ui/Ingame_Emo_Adaptresult{indoorBattleAdaptation[0]}.png')
    left_bottom_template.paste(img = streetAdaption_icon, pos = (544, 241), alpha = True)
    left_bottom_template.paste(img = outdoorAdaptation_icon, pos = (623, 241), alpha = True)
    left_bottom_template.paste(img = indoorAdaptation_icon, pos = (702, 241), alpha = True)
    # 学校图标
    school_icon = BuildImage(0, 0, background = baImgPath + f'/source/schoolicon/School_Icon_{school}_W.png')
    school_icon.resize(ratio = 1.5)
    left_bottom_template.paste(img = school_icon, pos = (int(932 - school_icon.w / 2), int(170 - school_icon.h / 2)), alpha = True)
    # 粘贴
    background.paste(img = left_bottom_template, pos = (44, 1166), alpha = True)

    # 右上角部分

    right_top_template = BuildImage(0, 0, background = baImgPath + '/source/cardsrc/right_top_part.png',
                                    font = font_SC, font_size = 25)
    right_top_template.text((82, 14), f'体力值{space_amount(healthPoint)}{healthPoint}\n\n'
                                      f'防御力{space_amount(defensePower)}{defensePower}\n\n'
                                      f'闪避值{space_amount(dodgePoint)}{dodgePoint}\n\n'
                                      f'暴击值{space_amount(criticalPoint)}{criticalPoint}\n\n'
                                      f'载弹量{space_amount(ammoCount, 2)}{ammoCount}\n\n'
                                      f'回费量{space_amount(regenCost)}{regenCost}\n\n',
                            font_color_white)
    right_top_template.text((469, 14),  f'攻击力{space_amount(attackPower, -1)}{attackPower}\n\n'
                                        f'治愈力{space_amount(healPower)}{healPower}\n\n'
                                        f'准确度{space_amount(accuracyPoint)}{accuracyPoint}\n\n'
                                        f'暴击伤害{space_amount(criticalDamageRate, -6)}{criticalDamageRate}\n\n'
                                        f'射程{space_amount(range_, 4)}{range_}\n\n'
                                        f'稳定值{space_amount(stabilityPoint)}{stabilityPoint}\n\n',
                            font_color_white)
    # 武器及类别
    weapon_desc = f'武器描述：\n{base_info["Weapon"]["Desc"]}'
    weapon_icon_path = baImgPath + f'/source/weapon/{base_info["WeaponImg"]}.png'
    image_exist_check(weapon_icon_path, f'https://raw.githubusercontent.com/lonqie/SchaleDB/main/images/weapon/{base_info["WeaponImg"]}.png')
    weapon_icon = BuildImage(0, 0, background = weapon_icon_path)
    weapon_icon.resize(ratio = 0.35)
    right_top_template.paste(img = weapon_icon, pos = (int(175 - weapon_icon.w / 2), int(482 - weapon_icon.h / 2)), alpha = True)
    weaponType_text = BuildImage(0, 0, plain_text = weaponType, font_size = 25, font_color = font_color_white, font = font_SC)
    right_top_template.paste(img = weaponType_text, pos = (int(315 - weaponType_text.w / 2), int(510 - weaponType_text.h / 2)), alpha = True)
    # 饰品
    i = 0
    for equip in equipment:
        equip_icon = BuildImage(0, 0, background = baImgPath + f'/source/equipment/Equipment_Icon_{equip}_Tier1.png')
        right_top_template.paste(img = equip_icon, pos = (377 + i * 129, 425), alpha = True)
        i += 1

    background.paste(img = right_top_template, pos = (1199, 66), alpha = True)

    # 右下角部分

    pos = [-150, 220]
    fnt_icon_shift_flag = 1 if furnitureInteraction else 0
    lobby_icon_shift_flag = 1 if base_info['MemoryLobby'][0] else 0
    if fnt_icon_shift_flag and lobby_icon_shift_flag:
        right_bottom_template = BuildImage(0, 0, background = baImgPath + f'/source/cardsrc/right_bottom_part.png',
                                           font_size = 25, font = font_SC)
    elif not fnt_icon_shift_flag and lobby_icon_shift_flag:
        right_bottom_template = BuildImage(0, 0, background = baImgPath + f'/source/cardsrc/right_bottom_part_no_furniture.png',
                                           font_size = 25, font = font_SC)
    elif lobby_icon_shift_flag and not fnt_icon_shift_flag:
        right_bottom_template = BuildImage(0, 0, background = baImgPath + f'/source/cardsrc/right_bottom_part_no_lobby.png',
                                           font_size = 25, font = font_SC)
    else:
        right_bottom_template = BuildImage(0, 0, background = baImgPath + f'/source/cardsrc/right_bottom_part_only_icon.png',
                                           font_size = 25, font = font_SC)

    # 学生档案
    left_text_to_paste_list = [localization_data["SchoolLong"][school], age, hobby, cv]
    right_text_to_paste_list = [Club[club], birthday, height, illustor]
    i = 0
    for info in left_text_to_paste_list:
        info_split = ''
        if background.getsize(info)[0] > 300:
            info_split += info[12:]
            info = info[:12] + '\n'
            info += info_split
            pos_shift_x = 40
            pos_shift_y = -10
            info_text = BuildImage(0, 0, background = baImgPath + '/source/cardsrc/blank.png', font_size = 20, font = font_SC, font_color = font_color_white)
            info_text.text((0, 0), info, font_color_white)
        else:
            pos_shift_x = 0
            pos_shift_y = 0
            info_text = BuildImage(0, 0, plain_text = str(info), font_size = 25, font = font_SC, font_color = font_color_white)
        right_bottom_template.paste(img = info_text, pos = (380 - info_text.w + pos_shift_x, 14 + i * 66 + pos_shift_y), alpha = True)
        i += 1
    i = 0
    for info in right_text_to_paste_list:
        info_split = ''
        if background.getsize(info)[0] > 270:
            info_split += info[12:]
            info = info[:12] + '\n'
            info += info_split
            pos_shift_x = 40
            pos_shift_y = -10
            info_text = BuildImage(0, 0, background = baImgPath + '/source/cardsrc/blank.png', font_size = 20, font = font_SC, font_color = font_color_white)
            info_text.text((0, 0), info, font_color_white)
        else:
            pos_shift_x = 0
            pos_shift_y = 0
            info_text = BuildImage(0, 0, plain_text = str(info), font_size = 25, font = font_SC, font_color = font_color_white)
        # info_text = BuildImage(0, 0, plain_text = str(info), font_size = 25, font = font_SC, font_color = font_color_white)
        right_bottom_template.paste(img = info_text, pos = (775 - info_text.w, 14 + i * 66), alpha = True)
        i += 1

    # 礼物 （要命)
    # 大概规则：一件礼物的Tags里如果有某名学生的FavorItemTags，则喜爱度+1，如果有FavorItemUniqueTags则喜爱度+2;
    # 最后再进行一次判定，SR礼物喜爱度不可大于3，SSR礼物喜爱度不可大于4小于3.
    favor_dict = {}
    favor_quality = {}
    for item in favor_data:
        favor_level = 1
        for tag in base_info['FavorItemTags']:
            if tag in item['Tags']:
                favor_level += 1
        for tag in base_info['FavorItemUniqueTags']:
            if tag in item['Tags']:
                favor_level += 2
        if favor_level > 1:
            if item['Quality'] == 3:
                favor_level = min(favor_level, 3)
            if item['Quality'] == 4:
                favor_level = min(max(favor_level, 3), 4)
            favor_dict[item['Icon']] = favor_level
            favor_quality[item['Icon']] = item['Rarity']
    favor_sorted = sorted(favor_dict.items(), key=lambda d: d[1], reverse=True)
    i = 0
    for favor in favor_sorted:
        favor_icon = BuildImage(0, 0, background = baImgPath + f'/source/items/{favor[0]}.png')
        favor_icon.resize(0.9)
        like_icon = BuildImage(0, 0, background = baImgPath + f'/source/ui/Cafe_Interaction_Gift_0{favor[-1]}.png')
        quality_backcolor = BuildImage(0, 0, background = baImgPath + f'/source/items/Quality_{favor_quality[favor[0]]}.png')
        if i < 6:
            right_bottom_template.paste(img = quality_backcolor, pos = (18 + i * 129, 348), alpha = True)
            right_bottom_template.paste(img = favor_icon, pos = (10 + i * 129, 355), alpha = True)
            right_bottom_template.paste(img = like_icon, pos = (76 + i * 129, 410), alpha = True)
            i += 1
        else:
            right_bottom_template.paste(img = quality_backcolor, pos = (18 + (i - 6) * 129, 477), alpha = True)
            right_bottom_template.paste(img = favor_icon, pos = (10 + (i - 6) * 129, 484), alpha = True)
            right_bottom_template.paste(img = like_icon, pos = (76 + (i - 6) * 129, 539), alpha = True)
            i += 1
    i = 0

    # 互动家具
    print(furnitureInteraction)
    if furnitureInteraction:
        for item in furniture_data:
            if furnitureInteraction == int(item['Id']):
                furniture_icon_path = baImgPath + f"/source/furniture/{item['Icon']}.png"
                image_exist_check(furniture_icon_path, f'https://raw.githubusercontent.com/lonqie/SchaleDB/main/images/furniture/{item["Icon"]}.png')
                furniture_icon = BuildImage(0, 0, background = furniture_icon_path)
                quality_backcolor = BuildImage(0, 0, background = baImgPath + f"/source/items/Quality_{item['Rarity']}.png")
                quality_backcolor.resize(ratio = 1.15)
                right_bottom_template.paste(img = quality_backcolor, pos = (139 + pos[1] * (1-lobby_icon_shift_flag), 641), alpha=True)
                right_bottom_template.paste(img = furniture_icon, pos = (int(203 - furniture_icon.w / 2 + pos[1] * (1-lobby_icon_shift_flag)), int(707 - furniture_icon.h / 2)), alpha = True)
                break

    # 大厅档案
    if base_info['MemoryLobby'][0]:
        lobby_archive_icon_path = baImgPath + f"/source/student/lobby/Lobbyillust_Icon_{base_info['DevName']}_01.png"
        image_exist_check(lobby_archive_icon_path, f"https://raw.githubusercontent.com/lonqie/SchaleDB/main/images/student/lobby/Lobbyillust_Icon_{base_info['DevName']}_01.png")
        lobby_archive_icon = BuildImage(0, 0, background = lobby_archive_icon_path)
        love_icon = BuildImage(0, 0, background = baImgPath + f"/source/ui/School_Icon_Schedule_Favor.png")
        love_point = BuildImage(0, 0, plain_text = str(base_info['MemoryLobby'][0]),
                                font = font_SC, font_size = 25, font_color = font_color_white)
        love_icon.paste(img = love_point, pos = (int(32 - love_point.w / 2), int(27 - love_point.h / 2)), alpha = True)
        right_bottom_template.paste(img = lobby_archive_icon, pos = (502 + pos[0] * (1-fnt_icon_shift_flag), 633), alpha = True)
        right_bottom_template.paste(img = love_icon, pos = (636 + pos[0] * (1-fnt_icon_shift_flag), 731), alpha = True)
    background.paste(img = right_bottom_template, pos = (1199, 696), alpha = True)

    # 最后水印
    mark_path = baImgPath + f"/source/cardsrc/markdown.png"
    mark_ds_path = baImgPath + f"/source/cardsrc/mark_datasource.png"
    mark_text = BuildImage(0, 0, background = mark_path)
    mark_ds_text = BuildImage(0, 0, background = mark_ds_path)
    background.paste(mark_text, (int(background.w - mark_text.w), int(background.h - mark_text.h)), alpha=True)
    background.paste(mark_ds_text, (0, int(background.h - mark_text.h)), alpha=True)

    #background.resize(ratio = 0.75)
    imageToSend = f"[CQ:image,file=base64://{background.pic2bs4()}]"

    # 最后学生介绍
    global debug_mode
    if debug_mode == 1:
        background.save(os.path.join(baImgPath, 'card.png'))
    return imageToSend, memoryLobbyBGM, introduction


def get_skill_info(student_id):
    global localization_data, parameters
    student_id = int(student_id)

    '''if student_id == 0:
        return None'''

    furniture_data = json.load(open(os.path.join(database_path, 'furniture.json'), encoding='utf-8'))
    student_data = json.load(open(os.path.join(database_path, 'students.json'), encoding='utf-8'))
    localization_data = json.load(open(os.path.join(database_path, 'localization.json'), encoding='utf-8'))
    favor_data = json.load(open(os.path.join(database_path, 'favor.json'), encoding='utf-8'))
    if favor_data is None or student_data is None or localization_data is None:
        print('数据库不齐全')
        return None

    base_info = get_item(student_data, "Id", student_id)  # 获取学生信息
    school = base_info['School']
    bulletType = base_info['BulletType']
    weaponType = base_info['WeaponType']

    # 固有武器

    weapon_info = base_info['Weapon']
    weaponName = weapon_info['Name']
    weaponDesc = weapon_info['Desc']
    weaponAdaptationType = weapon_info['AdaptationType']
    weaponAdaptationValue = weapon_info['AdaptationValue']
    terrian_adapt_tag = f'{weaponAdaptationType}BattleAdaptation'
    terrian_adapt_value = base_info[terrian_adapt_tag]
    new_adapt_value = int(terrian_adapt_value) + int(weaponAdaptationValue)

    # 技能组

    skill_info = base_info['Skills']
    skill_list = []
    gear_skill = []
    weapon_skill = []
    normal_skill = []
    for skill in skill_info:
        skillType = skill['SkillType']  # 属于哪种技能

        if skillType == 'weaponpassive':
            weapon_skill.append(skill)
        elif skillType == 'gearnormal':
            gear_skill.append(skill)
        else:
            normal_skill.append(skill)

    # 绘图

    # weapon_skill_background = BuildImage(0, 0, background=baImgPath + f'/source/cardsrc/skill_icon_{bulletType}.png')

    # 背景

    bg_name = base_info['CollectionBG']
    bg_file_path = baImgPath + f'/source/background/{bg_name}.jpg'
    background = BuildImage(0, 0, font_size = 25, background = bg_file_path, font = 'yz.ttf')
    background.resize(ratio = 2)

    # 右上角 简要
    # 头像
    collection_name = base_info["DevName"]
    collection_file_path_webp = baImgPath + f'/source/student/collection/{base_info["CollectionTexture"]}.webp'
    collection_file_path = baImgPath + f'/source/student/collectionpng/{base_info["CollectionTexture"]}.png'
    if not os.path.exists(collection_file_path):
        image_exist_check(collection_file_path_webp, f'https://raw.githubusercontent.com/lonqie/SchaleDB/main/images/student/collection/{base_info["CollectionTexture"]}.webp')
        collection_png = Image.open(collection_file_path_webp)
        collection_png.load()
        collection_png.save(collection_file_path)
    collection_icon = BuildImage(0, 0, background = collection_file_path)
    profile_lite_template = BuildImage(0, 0, background = baImgPath + f'/source/cardsrc/skill_card_student.png', font = 'NotoSansSC-Bold.otf', font_color = font_color_white)
    # 校徽
    school_icon = BuildImage(0, 0, background = baImgPath + f"/source/schoolicon/School_Icon_{school}_W.png")
    # 姓名
    fullName_text = BuildImage(0, 0, plain_text = f'{base_info["FamilyName"]} {base_info["PersonalName"]}',
                               font_size=50, font_color=font_color_white, font = 'NotoSansSC-Bold.otf')
    # 学校,年级
    school_and_year_text = BuildImage(0, 0, plain_text =f'{localization_data["SchoolLong"][school]} {base_info["SchoolYear"]}',
                                      font_size=35, font_color=font_color_white, font = 'NotoSansSC-Bold.otf')
    profile_lite_template.paste(img = school_and_year_text, pos = (37, 351), alpha= True)
    profile_lite_template.paste(img = fullName_text, pos = (37, 281), alpha= True)
    profile_lite_template.paste(img = school_icon, pos = (279, 85), alpha = True)
    profile_lite_template.paste(img = collection_icon, pos = (40, 40), alpha = True)

    # 枪部分

    weapon_template = BuildImage(0, 0, background = baImgPath + '/source/cardsrc/skill_card_weapon_vac.png')
    # 枪
    weapon_path = baImgPath + f'/source/weapon/{base_info["WeaponImg"]}.png'
    image_exist_check(weapon_path, f"https://raw.githubusercontent.com/lonqie/SchaleDB/main/images/weapon/{base_info['WeaponImg']}.png")
    weapon_plate = BuildImage(0, 0, background = baImgPath + '/source/cardsrc/weapon_background.png')
    weapon_model = BuildImage(0, 0, background = baImgPath + f'/source/weapon/{base_info["WeaponImg"]}.png')
    weapon_plate.paste(img = weapon_model, pos = (0, 0), alpha = True)
    weapon_plate.resize(ratio = 0.5)
    # 名字
    weapon_name_text = BuildImage(0, 0, plain_text = f'{weaponName}({weaponType})', font_size = 50, font_color=font_color_white, font = font_SC_Bold)
    # 武器技能
    weapon_skill = weapon_skill[0]
    weapon_skill_bg = BuildImage(0, 0, background=baImgPath + f'/source/cardsrc/skill_icon_{bulletType}.png')
    weapon_skill_icon = BuildImage(0, 0, background = baImgPath + f'/source/skill/{weapon_skill["Icon"]}.png')
    weapon_skill_icon.resize(ratio = 0.8)
    weapon_skill_bg.paste(img = weapon_skill_icon, pos = (12, 13), alpha=True)
    parameters = weapon_skill["Parameters"]
    skillName_text = BuildImage(0, 0, plain_text=weapon_skill["Name"], font_size=40, font_color=font_color_white, font = font_SC_Bold)
    skillType_text = BuildImage(0, 0, plain_text=SkillType[weapon_skill["SkillType"]], font_size=25, font_color=font_color_white, font = font_SC)
    skillDesc = weapon_skill['Desc']
    # print(skillDesc)
    skillDesc = re.sub(r'<\?(\d+)>', desc_param_transform, skillDesc)  # <?d>类型转换
    skillDesc = re.sub(r'<(\w):(\w+)>', desc_type_transform, skillDesc)  # <?:?>类型转换
    skillDesc = skillDesc.replace("/\n", "/")
    skillDesc = skillDesc.replace("\n", '；')
    skillDesc_text = BuildImage(0, 0, plain_text=skillDesc, font_size=25, font_color=font_color_white, font=font_SC_Bold)
    if skillDesc_text.w > 1170:
        skillDesc_text.resize(w = 1170, h = skillDesc_text.h)
    # 地形战力强化
    terrian_adapt_tplate = BuildImage(0, 0, background = baImgPath + f'/source/cardsrc/skill_card_terrain.png')
    terrian_icon = BuildImage(0, 0, background = baImgPath + f'/source/cardsrc/Terrain_{weaponAdaptationType}.png')
    terrian_old_adapt_icon = BuildImage(0, 0, background = baImgPath + f'/source/ui/Ingame_Emo_Adaptresult{BattleAdaptation[terrian_adapt_value]}.png')
    terrian_new_adapt_icon = BuildImage(0, 0, background = baImgPath + f'/source/ui/Ingame_Emo_Adaptresult{BattleAdaptation[new_adapt_value]}.png')
    terrian_adapt_tplate.paste(img = terrian_icon, pos = (75, 89), alpha=True)
    terrian_adapt_tplate.paste(img = terrian_icon, pos = (283, 89), alpha=True)
    terrian_adapt_tplate.paste(img = terrian_old_adapt_icon, pos = (109, 123), alpha=True)
    terrian_adapt_tplate.paste(img = terrian_new_adapt_icon, pos = (317, 123), alpha=True)

    weapon_template.paste(img = weapon_plate, pos = (47, 44), alpha = True)
    weapon_template.paste(img = weapon_name_text, pos = (117, 167), alpha = True)
    weapon_template.paste(img = weapon_skill_bg, pos = (42, 263), alpha = True)
    weapon_template.paste(img = skillName_text, pos = (175, 250), alpha=True)
    weapon_template.paste(img = skillType_text, pos = (179, 308), alpha=True)
    weapon_template.paste(img = skillDesc_text, pos = (177, 353), alpha=True)
    weapon_template.paste(img = terrian_adapt_tplate, pos = (876, 44), alpha=True)

    # 技能
    if gear_skill:
        skill_template = BuildImage(0, 0, background = baImgPath + '/source/cardsrc/skill_card_skill_vac_2.png', font_size=25, font = font_SC_Bold)
    else:
        skill_template = BuildImage(0, 0, background = baImgPath + '/source/cardsrc/skill_card_skill_vac_1.png', font_size=25, font = font_SC_Bold)
    i = 0
    for skill in normal_skill:

        if skill['SkillType'] == 'autoattack':  # 作用暂时不明？
            continue

        skillType = SkillType[skill['SkillType']]
        skillName = skill['Name']
        if skillType == 'EX技能':
            skillType += '       Cost['
            for c in range(len(skill['Cost'])):
                cost = skill['Cost'][c]
                skillType += f'{cost}→'
            skillType = skillType.strip('→')
            skillType += ']'
        skillDesc = skill['Desc']
        parameters = skill["Parameters"]
        skillDesc = re.sub(r'<\?(\d+)>', desc_param_transform, skillDesc)  # <?d>类型转换
        skillDesc = re.sub(r'<(\w):(\w+)>', desc_type_transform, skillDesc)  # <?:?>类型转换
        '''len_of_cn = len(re.sub(u"([^\u4e00-\u9fa5])", "", skillDesc))
        len_of_cn_before134 = len(re.sub(u"([^\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\u4e00-\u9fa5])", "", skillDesc[:85]))
        skillDesc = skillDesc[:int(134 - len_of_cn_before134)].strip('，') + '...' if len(skillDesc) > int(134 - len_of_cn) else skillDesc + '.'''''
        skillDesc = skillDesc.replace("/\n", "/")
        skillDesc = skillDesc.replace('\n', '；')
        # print(skillDesc)
        skillDesc_text = BuildImage(0, 0, plain_text=skillDesc, font_size=25, font_color=font_color_white, font = font_SC_Bold)
        if skillDesc_text.w > 1710:
            skillDesc_text.resize(w = 1710, h = skillDesc_text.h)
        # 图标
        skill_background = BuildImage(0, 0, background=baImgPath + f'/source/cardsrc/skill_icon_{bulletType}.png')
        skill_icon_path = baImgPath + f'/source/skill/{skill["Icon"]}.png'
        image_exist_check(skill_icon_path, f"https://raw.githubusercontent.com/lonqie/SchaleDB/main/images/skill/{skill['Icon']}.png")
        skill_icon = BuildImage(0, 0, background = baImgPath + f'/source/skill/{skill["Icon"]}.png')
        skill_icon.resize(ratio = 0.8)
        skill_background.paste(img = skill_icon, pos = (12, 13), alpha=True)
        # 技能名及技能种类
        skillName_text = BuildImage(0, 0, plain_text=skillName, font_size=40, font_color=font_color_white, font = font_SC_Bold)
        skillType_text = BuildImage(0, 0, plain_text=skillType, font_size=25, font_color=font_color_white, font = font_SC)
        # 统一粘贴
        skill_template.paste(img = skillDesc_text, pos = (183, 112 + i * 191), alpha = True)
        skill_template.paste(img = skillName_text, pos = (183, 9 + i * 191), alpha = True)
        skill_template.paste(img = skillType_text, pos = (187, 67 + i * 191), alpha=True)

        skill_template.paste(img = skill_background, pos = (35, 19 + i * 191), alpha=True)
        i += 1

    if gear_skill:
        skill = gear_skill[0]
        parameters = skill["Parameters"]
        skillType = SkillType[skill['SkillType']]
        skillName = skill['Name']
        skillDesc = skill['Desc'] + '.'
        skillDesc = re.sub(r'<\?(\d+)>', desc_param_transform, skillDesc)  # <?d>类型转换
        skillDesc = re.sub(r'<(\w):(\w+)>', desc_type_transform, skillDesc)  # <?:?>类型转换
        skillDesc = skillDesc.replace("/\n", "/")
        skillDesc = skillDesc.replace('\n', '；')
        skill_background = BuildImage(0, 0, background=baImgPath + f'/source/cardsrc/skill_icon_{bulletType}.png')
        skill_icon_path = baImgPath + f'/source/skill/{skill["Icon"]}.png'
        image_exist_check(skill_icon_path, f"https://raw.githubusercontent.com/lonqie/SchaleDB/main/images/skill/{skill['Icon']}.png")
        skill_icon = BuildImage(0, 0, background = baImgPath + f'/source/skill/{skill["Icon"]}.png')
        skill_icon.resize(ratio = 0.8)
        skill_background.paste(img = skill_icon, pos = (12, 13), alpha=True)
        skillName_text = BuildImage(0, 0, plain_text=skillName, font_size=40, font_color=font_color_white, font = font_SC_Bold)
        skillType_text = BuildImage(0, 0, plain_text=skillType, font_size=25, font_color=font_color_white, font = font_SC)
        skillDesc_text = BuildImage(0, 0, plain_text=skillDesc, font_size=25, font_color=font_color_white, font = font_SC_Bold)
        if skillDesc_text.w > 1710:
            skillDesc_text.resize(w = 1710, h = skillDesc_text.h)
        skill_template.paste(img = skillName_text, pos = (183, 773), alpha = True)
        skill_template.paste(img = skillType_text, pos = (187, 831), alpha=True)
        skill_template.paste(img = skillDesc_text, pos = (183, 876), alpha=True)
        skill_template.paste(img = skill_background, pos = (35, 783), alpha=True)
        gear_bg = BuildImage(0, 0, background = baImgPath + '/source/cardsrc/Gear_Background.png')
        gear_icon_path = baImgPath + f'/source/gear/{base_info["Gear"]["Icon"]}.png'
        image_exist_check(gear_icon_path, f"https://raw.githubusercontent.com/lonqie/SchaleDB/main/images/gear/{base_info['Gear']['Icon']}.png")
        gear_icon = BuildImage(0, 0, background = baImgPath + f'/source/gear/{base_info["Gear"]["Icon"]}.png')
        gear_bg.paste(img = gear_icon, pos = (30, 0), alpha = True)
        skill_template.paste(img = gear_bg, pos = (1666, 793), alpha = True)
    else:
        no_gear_text = BuildImage(0, 0, plain_text='该学生暂时没有爱用品...', font_size = 40, font_color=font_color_white)
        skill_template.paste(img = no_gear_text, pos = (int(957 - no_gear_text.w / 2), int(844 - no_gear_text.h / 2)), alpha = True)

    background.paste(img = profile_lite_template, pos = (66, 60), alpha = True)
    background.paste(img = weapon_template, pos = (610, 59), alpha=True)
    background.paste(img = skill_template, pos = (66, 549), alpha = True)

    global debug_mode
    if debug_mode:
        background.save(os.path.join(baImgPath, 'skill_card.png'))

    # 最后水印
    mark_path = baImgPath + f"/source/cardsrc/markdown.png"
    mark_ds_path = baImgPath + f"/source/cardsrc/mark_datasource.png"
    mark_text = BuildImage(0, 0, background = mark_path)
    mark_ds_text = BuildImage(0, 0, background = mark_ds_path)
    background.paste(mark_text, (int(background.w - mark_text.w), int(background.h - mark_text.h)), alpha=True)
    background.paste(mark_ds_text, (0, int(background.h - mark_text.h)), alpha=True)

    # background.resize(ratio = 0.75)
    imageToSend = f"[CQ:image,file=base64://{background.pic2bs4()}]"
    weapon_desc = f'武器描述:\n{weaponDesc}'
    if base_info["Gear"]:
        favoritem_desc = f'爱用品描述:\n{base_info["Gear"]["Desc"]}'
    else:
        favoritem_desc = ''
    return imageToSend, weapon_desc, favoritem_desc


def get_material_info(student_id):
    global localization_data, parameters
    student_id = int(student_id)

    items_data = json.load(open(os.path.join(database_path, 'items.json'), encoding='utf-8'))
    student_data = json.load(open(os.path.join(database_path, 'students.json'), encoding='utf-8'))
    localization_data = json.load(open(os.path.join(database_path, 'localization.json'), encoding='utf-8'))
    favor_data = json.load(open(os.path.join(database_path, 'favor.json'), encoding='utf-8'))
    if favor_data is None or student_data is None or localization_data is None:
        print('数据库不齐全')
        return None

    base_info = get_item(student_data, "Id", student_id)  # 获取学生信息

    ex_material_list = base_info["SkillExMaterial"]
    ex_material_mount = base_info["SkillExMaterialAmount"]
    skill_material_list = base_info["SkillMaterial"]
    skill_material_mount = base_info["SkillMaterialAmount"]

    background = BuildImage(0, 0, background=baImgPath + '/source/cardsrc/material_card.jpg')

    # 爱用品的升级材料
    if base_info["Gear"]:
        paste_shift = 0
        right_top_background = BuildImage(0, 0, background=baImgPath + '/source/cardsrc/material_card_gear.png')
        tier_up_material_list = base_info["Gear"]["TierUpMaterial"][0]
        tier_up_material_mount = base_info["Gear"]["TierUpMaterialAmount"][0]
        material_list = []
        for item in tier_up_material_list:
            item_info = get_item(items_data, "Id", item)
            item_index = tier_up_material_list.index(item)
            item_icon_path = baImgPath + f'/source/items/{item_info["Icon"]}.png'
            item_bg_path = baImgPath + f'/source/cardsrc/item_bg_{item_info["Rarity"]}.png'
            image_exist_check(item_icon_path, f"https://raw.githubusercontent.com/lonqie/SchaleDB/main/images/items/{item_info['Icon']}.png")
            item_icon = BuildImage(0, 0, background=item_icon_path)
            item_bg = BuildImage(0, 0, background=item_bg_path)
            item_bg.paste(item_icon, pos=(-2, 0), alpha=True)
            mount_text = BuildImage(0, 0, plain_text=str(tier_up_material_mount[item_index]), font=font_rothorn, font_size=30, font_color=font_color_black)
            w, h = mount_text.size
            item_bg.paste(mount_text, pos=(int(142 - w / 2), int(99 - h / 2)), alpha=True)
            if item_index < 2:
                right_top_background.paste(item_bg, pos=(698 + 320 * item_index, 234), alpha=True)
            else:
                right_top_background.paste(item_bg, pos=(856, 434), alpha=True)
    else:
        right_top_background = BuildImage(0, 0, background=baImgPath + '/source/cardsrc/material_card_no_gear.png')
        paste_shift = 1

    # 头像
    collection_name = base_info["DevName"]
    collection_file_path_webp = baImgPath + f'/source/student/collection/{base_info["CollectionTexture"]}.webp'
    collection_file_path = baImgPath + f'/source/student/collectionpng/{base_info["CollectionTexture"]}.png'
    if not os.path.exists(collection_file_path):
        image_exist_check(collection_file_path_webp, f'https://raw.githubusercontent.com/lonqie/SchaleDB/main/images/student/collection/{base_info["CollectionTexture"]}.webp')
        collection_png = Image.open(collection_file_path_webp)
        collection_png.load()
        collection_png.save(collection_file_path)
    collection_icon = BuildImage(0, 0, background = collection_file_path)
    collection_icon.resize(ratio=2)
    right_top_background.paste(collection_icon, pos=(83, 50), alpha=True)

    # 全名
    fullName_text = BuildImage(0, 0, plain_text = f'{base_info["FamilyName"]} {base_info["PersonalName"]}',
                               font_size=70, font_color=font_color_white, font = font_SC_Bold)
    w, h = fullName_text.size
    right_top_background.paste(fullName_text, pos=(int(285 - w / 2), int(585 - h / 2)), alpha=True)

    # 贴上
    background.paste(right_top_background, pos = (109 + 400 * paste_shift, 50), alpha=True)

    # EX技能材料

    _list_index = -1
    for _list in ex_material_list:
        material_serial = BuildImage(0, 0, is_alpha=True)
        _list_index += 1
        material_serial.resize(w = 186 * len(_list), h = 116)
        item_index = -1
        for item in _list:
            item_index += 1
            item_info = get_item(items_data, "Id", item)
            item_icon_path = baImgPath + f'/source/items/{item_info["Icon"]}.png'
            item_bg_path = baImgPath + f'/source/cardsrc/item_bg_{item_info["Rarity"]}.png'
            image_exist_check(item_icon_path, f"https://raw.githubusercontent.com/lonqie/SchaleDB/main/images/items/{item_info['Icon']}.png")
            item_icon = BuildImage(0, 0, background=item_icon_path)
            item_bg = BuildImage(0, 0, background=item_bg_path)
            item_bg.paste(item_icon, pos=(-2, 0), alpha=True)
            mount_text = BuildImage(0, 0, plain_text=str(ex_material_mount[_list_index][item_index]), font=font_rothorn, font_size=30, font_color=font_color_black)
            w, h = mount_text.size
            item_bg.paste(mount_text, pos=(int(142 - w / 2), int(99 - h / 2)), alpha=True)
            material_serial.paste(item_bg, pos=(0 + item_index * 186, 0), alpha=True)
            w, h = material_serial.size
            background.paste(material_serial, pos=(int(892 - w / 2), int(976 + 149 * _list_index - h / 2)), alpha=True)

    # 普通技能材料
    _list_index = -1
    for _list in skill_material_list:
        material_serial = BuildImage(0, 0, is_alpha=True)
        _list_index += 1
        material_serial.resize(w = 186 * len(_list), h = 116)
        item_index = -1
        for item in _list:
            item_index += 1
            item_info = get_item(items_data, "Id", item)
            item_icon_path = baImgPath + f'/source/items/{item_info["Icon"]}.png'
            item_bg_path = baImgPath + f'/source/cardsrc/item_bg_{item_info["Rarity"]}.png'
            image_exist_check(item_icon_path, f"https://raw.githubusercontent.com/lonqie/SchaleDB/main/images/items/{item_info['Icon']}.png")
            item_icon = BuildImage(0, 0, background=item_icon_path)
            item_bg = BuildImage(0, 0, background=item_bg_path)
            item_bg.paste(item_icon, pos=(-2, 0), alpha=True)
            mount_text = BuildImage(0, 0, plain_text=str(skill_material_mount[_list_index][item_index]), font=font_rothorn, font_size=30, font_color=font_color_black)
            w, h = mount_text.size
            item_bg.paste(mount_text, pos=(int(142 - w / 2), int(99 - h / 2)), alpha=True)
            material_serial.paste(item_bg, pos=(0 + item_index * 186, 0), alpha=True)
            w, h = material_serial.size
            background.paste(material_serial, pos=(int(2368 - w / 2), int(225 + 149 * _list_index - h / 2)), alpha=True)

    global debug_mode
    if debug_mode:
        background.save(os.path.join(baImgPath, 'material_card.png'))

    # 最后水印
    mark_path = baImgPath + f"/source/cardsrc/markdown.png"
    mark_ds_path = baImgPath + f"/source/cardsrc/mark_datasource.png"
    mark_text = BuildImage(0, 0, background = mark_path)
    mark_ds_text = BuildImage(0, 0, background = mark_ds_path)
    background.paste(mark_text, (int(background.w - mark_text.w), int(background.h - mark_text.h)), alpha=True)
    background.paste(mark_ds_text, (0, int(background.h - mark_text.h)), alpha=True)

    background.resize(ratio=0.75)
    imageToSend = f"[CQ:image,file=base64://{background.pic2bs4()}]"

    return imageToSend


if __name__ == '__main__':
    debug_mode = 1
    update_db()
    # student_id = get_student_id('幼瞬')
    # print(student_id)
    # get_student_info(student_id)
    # get_skill_info(student_id)
    # get_material_info('水大叔')
    # get_skill_info('若藻')
    # get_skill_info('阿露(正月)')
