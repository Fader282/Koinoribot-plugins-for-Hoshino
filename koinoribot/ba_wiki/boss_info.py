import json
import os
import re


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


plugin_path = os.path.dirname(__file__)
baImgPath = os.path.join(imgPath, 'ba_wiki')
database_path = os.path.join(plugin_path, 'db')

debug_mode = 0

parameters = []
diff_int = 0

font_color_white = (255, 255, 255)
font_color_black = (0, 0, 0)
font_SC_Bold = 'NotoSansSC-Bold.otf'
font_SC = 'NotoSansSC-Medium.otf'
font_heiti = 'simhei2.ttf'
font_rothorn = 'extra-bold-italia.ttf'

mark_color = (255, 255, 255, 30)


def get_boss_raids_id(nickname):
    """
        获取boss的raids ID
    """
    boss_list = json.load(open(os.path.join(database_path, 'boss_nickname.json'), encoding="utf-8"))
    nickname = str(nickname).capitalize()
    for boss_id, boss_names in boss_list.items():
        if nickname in boss_names:
            return boss_id
    return None


def get_boss_detail_info(enemies_id):
    """
        获取boss的详细数据，需要enemies_id如:7300100（大蛇）
    """
    enemies_data = json.load(open(os.path.join(database_path, 'enemies.json'), encoding='utf-8'))
    for enemy in enemies_data:
        if enemies_id == enemy['Id']:
            return enemy
    raise ValueError(f'get_boss_detail_info错误：未找到{enemies_id}对应的boss')


def get_difficulty_id(difficulty):
    difficulty_list = {'0': ['nm', 'normal'],
                       '1': ['hd', 'hard'],
                       '2': ['vh', 'veryhard'],
                       '3': ['hc', 'hardcore'],
                       '4': ['ex', 'extreme'],
                       '5': ['ins', 'insane'],
                       '6': ['tm', 'torment']}
    difficulty = str(difficulty).lower()
    for diff_id, diff_list in difficulty_list.items():
        if difficulty in diff_list:
            return diff_id
    return None


def get_boss_info(boss_id, difficulty):
    global parameters, diff_int
    diff_int = int(difficulty)

    ins_type = 1 if diff_int > 4 else 0
    boss_banner_path = os.path.join(baImgPath, f'source/cardsrc/boss/{boss_id}_{ins_type}.png')
    background1 = BuildImage(0, 0, background=boss_banner_path)

    level_icon_path = os.path.join(baImgPath, f'source/cardsrc/lv_{diff_int}.png')  # boss等级
    level_icon = BuildImage(0, 0, background=level_icon_path)
    background1.paste(level_icon, (358, 432), alpha=True)

    # 获取boss一系列数据
    boss_base_info = {}
    boss_data = json.load(open(os.path.join(database_path, 'raids.json'), encoding='utf-8'))['Raid']
    for boss in boss_data:
        if int(boss_id) == boss['Id']:
            boss_base_info = boss

    if not boss_base_info:
        raise TypeError('未找到该Boss数据')

    # print(boss_base_info)
    if int(boss_id) == 3:  # 黑白双子的情况
        base_id_2 = boss_base_info['EnemyList'][diff_int][1]
        base_info_2 = get_boss_detail_info(base_id_2)
    else:
        boss_id_2 = None
        base_info_2 = None
    try:
        base_id = boss_base_info['EnemyList'][diff_int][0]
    except IndexError:
        imageToSend = '没有这个难度喔..'
        return imageToSend
    base_info = get_boss_detail_info(base_id)  # 从enemies.json获取数据

    terrian = boss_base_info['Terrain']  # 地形，可能是两个
    for i in range(len(terrian)):
        terr_path = os.path.join(baImgPath, f'source/ui/Terrain_{terrian[i]}.png')
        terr_icon = BuildImage(0, 0, background=terr_path)
        background1.paste(terr_icon, (446 + i * 79, 425), alpha=True)

    bulletType = base_info['BulletType']  # 攻击类型
    bulletType_icon_path = os.path.join(baImgPath, f'source/cardsrc/{bulletType}.png')
    bulletType_icon = BuildImage(0, 0, background=bulletType_icon_path)
    background1.paste(bulletType_icon, (38, 517), alpha=True)

    armorType = base_info['ArmorType']  # 防具类型
    armorType_icon_path = os.path.join(baImgPath, f'source/cardsrc/{armorType}.png')
    armorType_icon = BuildImage(0, 0, background=armorType_icon_path)
    background1.paste(armorType_icon, (293, 517), alpha=True)

    bodyType = ''  # 大型还是超大型
    if 'EnemyXLarge' in base_info['Tags']:
        bodyType = 'EnemyXLarge'
    elif 'EnemyLarge' in base_info['Tags']:
        bodyType = 'EnemyLarge'
    if bodyType:
        bodyType_icon_path = os.path.join(baImgPath, f'source/cardsrc/{bodyType}.png')
        bodyType_icon = BuildImage(0, 0, background=bodyType_icon_path)
        background1.paste(bodyType_icon, (38, 431), alpha=True)


    # 数值部分
    stat_template_path = os.path.join(baImgPath, 'source/cardsrc/boss/boss_stat.png')
    background2 = BuildImage(0, 0, background=stat_template_path, font=font_SC, font_size=36, font_color=font_color_white)

    # (y+85)

    maxHP = str(base_info['MaxHP1'])  # 生命值
    if base_info_2 and base_info['MaxHP1'] != base_info_2['MaxHP1']:
        maxHP = f"{int(base_info['MaxHP1'] / 1000)}k/{int(base_info_2['MaxHP1'] / 1000)}k"
    background2.text((589, 63), maxHP, anchor='rs', fill=font_color_white)

    attackPower = str(base_info['AttackPower1'])  # 攻击力
    if base_info_2 and base_info['AttackPower1'] != base_info_2['AttackPower1']:
        attackPower = f"{base_info['AttackPower1']}/{base_info_2['AttackPower1']}"
    background2.text((1160, 63), attackPower, anchor='rs', fill=font_color_white)

    defensePower1 = str(base_info['DefensePower1'])  # 防御力
    background2.text((589, 149), defensePower1, anchor='rs', fill=font_color_white)

    damagedRatio = str(int((base_info['DamagedRatio'] - 10000) / 100)) + '%'
    background2.text((1160, 149), damagedRatio, anchor='rs', fill=font_color_white)

    accuracyPoint = str(base_info['AccuracyPoint'])  # 命中值
    background2.text((589, 235), accuracyPoint, anchor='rs', fill=font_color_white)

    dodgePoint = str(base_info['DodgePoint'])  # 闪避值
    background2.text((1160, 235), dodgePoint, anchor='rs', fill=font_color_white)

    criticalPoint = str(base_info['CriticalPoint'])  # 暴击值
    background2.text((589, 320), criticalPoint, anchor='rs', fill=font_color_white)

    criticalResistPoint = str(base_info['CriticalResistPoint'])  # 暴击抵抗力
    background2.text((1160, 320), criticalResistPoint, anchor='rs', fill=font_color_white)

    criticalDamageRate = str(int(base_info['CriticalDamageRate'] / 100)) + '%'  # 暴击伤害
    background2.text((589, 405), criticalDamageRate, anchor='rs', fill=font_color_white)

    criticalDamageResistRate = str(int(base_info['CriticalDamageResistRate'] / 100)) + '%'  # 暴伤抵抗率
    background2.text((1160, 405), criticalDamageResistRate, anchor='rs', fill=font_color_white)

    stabilityPoint = str(base_info['StabilityPoint'])  # 安定值
    background2.text((589, 490), stabilityPoint, anchor='rs', fill=font_color_white)

    _range = str(base_info['Range'])  # 射程
    background2.text((1160, 490), _range, anchor='rs', fill=font_color_white)

    groggyGauge = str(base_info['GroggyGauge'])  # 虚弱量表
    if base_info_2 and base_info['GroggyGauge'] != base_info_2['GroggyGauge']:
        groggyGauge = f"{int(base_info['GroggyGauge'] / 1000)}k/{int(base_info_2['GroggyGauge'] / 1000)}k"
    background2.text((589, 573), groggyGauge, anchor='rs', fill=font_color_white)

    groggyTime = str(int(base_info['GroggyTime'] / 1000)) + '秒'  # 虚弱持续时间
    background2.text((1160, 573), groggyTime, anchor='rs', fill=font_color_white)


    # 技能部分
    skills_info = boss_base_info['RaidSkill']
    template_top_path = os.path.join(baImgPath, 'source/cardsrc/boss/skill_template_top.png')
    template_middle_path = os.path.join(baImgPath, 'source/cardsrc/boss/skill_template_middle.png')
    template_bottom_path = os.path.join(baImgPath, 'source/cardsrc/boss/skill_template_bottom.png')
    boss_card_path = os.path.join(baImgPath, 'source/cardsrc/boss/boss_card.jpg')
    boss_card = BuildImage(0, 0, background=boss_card_path)

    skill_list = []  # 存放BuildImage
    total_height = 0
    for skill in skills_info:

        if skill['SkillType'] == 'raidautoattack':
            continue
        if skill['SkillType'] == 'normal':
            continue
        if 'MinDifficulty' in skill.keys():
            if diff_int < skill['MinDifficulty']:
                continue
        if 'MaxDifficulty' in skill.keys():
            if diff_int > skill['MaxDifficulty']:
                continue
        # print(skill)
        template_top = BuildImage(0, 0, background=template_top_path, is_alpha=True)
        template_middle = BuildImage(0, 0, background=template_middle_path, is_alpha=True)
        template_bottom = BuildImage(0, 0, background=template_bottom_path, is_alpha=True)

        icon_name = skill['Icon']  # 技能图标
        icon_path = os.path.join(baImgPath, f'source/raid/skill/{icon_name}.png')
        if not os.path.exists(icon_path):
            continue
        icon = BuildImage(0, 0, background=icon_path, is_alpha=True)

        parameters = skill['Parameters'] if 'Parameters' in skill.keys() else None  # 技能描述
        skillDesc = skill['Desc']
        if parameters:
            skillDesc = re.sub(r'<\?(\d+)>', desc_param_transform, skillDesc)  # <?d>类型转换
        skillDesc = re.sub(r'<(\w):(\w+)>', desc_type_transform, skillDesc)  # <?:?>类型转换
        skillDesc = skillDesc.replace('</b>', ' ').replace('<b>', ' ')  # 去掉<b>和</b>
        desc_text = BuildImage(0, 0, multiline_text=skillDesc, font_size=30, is_alpha=True, font_color=font_color_white, font=font_SC, color=(255, 255, 255, 0))
        if desc_text.w > 1890:
            skillDesc = skillDesc[:-6] + '\n' + skillDesc[-6:]
            desc_text = BuildImage(0, 0, multiline_text=skillDesc, font_size=30, is_alpha=True, font_color=font_color_white, font=font_SC, color=(255, 255, 255, 0))
        skillName = skill['Name']  # 技能名称
        name = BuildImage(0, 0, plain_text=skillName, font_size=50, font_color=font_color_white, font=font_SC_Bold, is_alpha=True)

        skillType = BossSkillType[skill['SkillType']]  # 技能类型
        atgCost = skill['ATGCost']  # 消耗ATG数量
        type_and_cost_text = f"{skillType}·ATG: {atgCost}" if atgCost else skillType
        type_and_cost = BuildImage(0, 0, plain_text=type_and_cost_text, font_color=font_color_white, font_size=25, font=font_SC)

        template_middle.resize(w=template_middle.w, h = desc_text.h + 135)
        template_middle.paste(icon, (12, 10), alpha=True)
        template_middle.paste(name, (148, 10), alpha=True)
        template_middle.paste(type_and_cost, (156, 81), alpha=True)
        template_middle.paste(desc_text, (26, 125), alpha=True)

        template_bg = BuildImage(0, 0, background=os.path.join(baImgPath, 'source/cardsrc/boss/skill_template_bg.png'))
        template_bg.paste(template_top, (0, 0), alpha=True)
        template_bg.paste(template_middle, (0, 10), alpha=True)
        template_bg.paste(template_bottom, (0, desc_text.h + 145), alpha=True)
        template_bg.crop((0, 0, template_bg.w, desc_text.h + 155))
        # template_bg.save(os.path.join(baImgPath, 'template.png'))
        skill_list.append(template_bg)
        total_height = total_height + desc_text.h + 170
    boss_card.resize(w = boss_card.w, h = total_height + 713)
    boss_card.paste(background1, (48, 42), alpha=True)
    boss_card.paste(background2, (798, 42), alpha=True)

    height = 0
    for i in range(len(skill_list)):
        boss_card.paste(skill_list[i], (48, 688 + height), alpha=True)
        height += skill_list[i].h + 15

    # 最后水印
    mark_path = baImgPath + f"/source/cardsrc/markdown.png"
    mark_ds_path = baImgPath + f"/source/cardsrc/mark_datasource.png"
    mark_text = BuildImage(0, 0, background = mark_path)
    mark_ds_text = BuildImage(0, 0, background = mark_ds_path)
    boss_card.paste(mark_text, (int(boss_card.w - mark_text.w), int(boss_card.h - mark_text.h)), alpha=True)
    boss_card.paste(mark_ds_text, (0, int(boss_card.h - mark_text.h)), alpha=True)

    if debug_mode:
        boss_card.save(os.path.join(baImgPath, 'boss_card.png'))

    imageToSend = f"[CQ:image,file=base64://{boss_card.pic2bs4()}]"

    # === bgm部分 ===
    bgm_list = json.load(open(os.path.join(database_path, 'bossbgm.json'), encoding='utf-8'))
    boss_bgm = bgm_list[int(boss_id) - 1]

    # === boss描述 ===
    boss_profile = boss_base_info['Profile']

    return imageToSend, boss_bgm, boss_profile


def desc_param_transform(match):
    global parameters, diff_int
    if not parameters:
        return "UNKNOWN"
    try:
        desc_param = parameters[int(match.group(1)) - 1][diff_int]
    except:
        desc_param = 'ERROR'
    return desc_param


def desc_type_transform(match):
    localization_data = json.load(open(os.path.join(database_path, 'localization.json'), encoding='utf-8'))
    buffName = localization_data["BuffName"]  # localization里的译文

    buff_types = {"b": "Buff_", "d": "Debuff_", "c": "CC_", "s": "Special_"}
    if match.group(1) not in buff_types:
        return match.group()

    buff_name = buff_types[match.group(1)] + match.group(2)

    # print(buff_name)
    if buff_name not in buffName.keys():
        return match.group()
    return buffName[buff_name]


if __name__ == '__main__':
    _id = get_boss_raids_id('黑白')
    print(_id)
    diff = get_difficulty_id('tm')
    print(diff)
    result = get_boss_info(_id, diff)
