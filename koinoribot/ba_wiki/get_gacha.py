import json
import ujson
import os
import random
from .student_info import *

from ..build_image import BuildImage

from .._R import imgPath, userPath

save_gacha_pic = 0

recordPath = os.path.join(userPath, 'gacha/userdata.json')
gachaPath = os.path.join(os.path.dirname(__file__), 'db/gacha.json')
studentPath = os.path.join(os.path.dirname(__file__), 'db/students.json')
plugin_path = os.path.join(os.path.dirname(__file__))
baImgPath = os.path.join(imgPath, 'ba_wiki')

gacha_pool = json.load(open(gachaPath, encoding='utf-8'))
student_data = json.load(open(studentPath, encoding='utf-8'))

stone_addnum = [1, 5, 30, 100]
flag_list = ['', 'new_flag.png', 'pickup_flag.png', 'new_and_pickup.png']

white = (255, 255, 255)


def get_10_gacha(uid, mode):
    userid = str(uid)
    result_list = gacha_10(mode = mode)
    user_dict = loadData(recordPath)

    if userid not in user_dict:
        user_dict[userid] = {
            'stone': 0,
            'gacha_count': 0,
            'point': 0,
            'students': {}
        }
        saveData(user_dict, recordPath)
        return 0

    if user_dict[userid]['stone'] < 1200:
        return 0

    bg = BuildImage(1100, 900, color = white)
    flag_num = []
    for i in range(10):
        result = result_list[i]
        _flag = 0
        charid = str(result[0])
        if result[-1] == 4:
            _flag += 2
        if charid not in user_dict[userid]['students']:
            user_dict[userid]['students'][charid] = {
                'star': min(3, result[-1]),
                'stone': 0
            }
            _flag += 1
        else:
            user_dict[userid]['students'][charid]['stone'] += stone_addnum[result[-1] - 1]
        flag_num.append(_flag)
        # === 绘图 ===
        # === 头像 ===
        base_info = get_item(student_data, 'Id', result[0])
        dev_name = base_info['DevName']
        collection_file_path_webp = baImgPath + f'/source/student/collection/{base_info["CollectionTexture"]}.webp'
        collection_file_path = baImgPath + f'/source/student/collectionpng/{base_info["CollectionTexture"]}.png'
        if not os.path.exists(collection_file_path):
            image_exist_check(collection_file_path_webp, f'https://raw.githubusercontent.com/lonqie/SchaleDB/main/images/student/collection/{base_info["CollectionTexture"]}.webp')
            collection_png = Image.open(collection_file_path_webp)
            collection_png.load()
            collection_png.save(collection_file_path)
        collection_icon = BuildImage(0, 0, background = collection_file_path)
        row = i % 5
        array = int(i / 5)
        bg.paste(collection_icon, (54 + row * 200, 131 + array * 300), alpha=True)

    # 中间层背景
    blue_bg_path = os.path.join(baImgPath + '/source/gacha/background.png')
    blue_bg = BuildImage(0, 0, background=blue_bg_path)
    bg.paste(blue_bg, (0, 0), alpha=True)

    for i in range(10):
        result = result_list[i]
        _flag = flag_num[i]
        row = i % 5
        array = int(i / 5)
        # 边框
        stu_star = min(3, result[-1])
        frame_path = os.path.join(baImgPath + f'/source/gacha/star_grade_{stu_star}.png')
        frame = BuildImage(0, 0, background=frame_path)
        bg.paste(frame, (30 + row * 200, 49 + array * 300), alpha=True)

        # 新角色或up
        flag_type = flag_list[_flag]
        if flag_type:
            flag_path = os.path.join(baImgPath + f'/source/gacha/{flag_type}')
        #93, 116
            flag = BuildImage(0, 0, background=flag_path)
            bg.paste(flag, (93 + row * 200, 116 + array * 300), alpha=True)

    #point
    point_text = BuildImage(0, 0, plain_text=str(user_dict[userid]['point'] + 10),
                            font_size=22,
                            font_color=white,
                            font='arialbd.ttf')
    bg.paste(point_text, (int(949 - point_text.w / 2), 823), alpha=True)

    #stone
    stone_text = BuildImage(0, 0, plain_text=f"{user_dict[userid]['stone'] - 1200}",
                            font_size=24,
                            font_color=(31, 87, 129),
                            font='arialbd.ttf')
    bg.paste(stone_text, (int(198 - stone_text.w / 2), 814), alpha=True)

    #抽卡信息:
    if mode == 99:
        mode_text = 'Normal'
    else:
        mode_text = mode + 1
    info_text = BuildImage(0, 0, plain_text=f'Gacha QQ:{uid}, ID:{mode_text}',
                           font_size=24,
                           font_color=(31, 87, 29),
                           font='arialbd.ttf')
    bg.paste(info_text, (1, 1), alpha=True)

    user_dict[userid]['stone'] -= 1200
    user_dict[userid]['gacha_count'] += 10
    user_dict[userid]['point'] += 10
    saveData(user_dict, recordPath)

    if save_gacha_pic:
        bg.save(os.path.join(baImgPath, 'gacha.png'))
    imageToSend = f"[CQ:image,file=base64://{bg.pic2bs4()}]"
    return imageToSend


def get_1_gacha(uid, mode):
    userid = str(uid)
    result = gacha_1(mode = mode)
    user_dict = loadData(recordPath)
    _flag = 0

    if userid not in user_dict:
        user_dict[userid] = {
            'stone': 0,
            'gacha_count': 0,
            'point': 0,
            'students': {}
        }
        return 0

    if user_dict[userid]['stone'] < 120:
        return 0

    charid = str(result[0])
    if charid not in user_dict[userid]['students']:
        user_dict[userid]['students'][charid] = {
            'star': min(3, result[-1]),
            'stone': 0
        }
        _flag += 1
    else:
        user_dict[userid]['students'][charid]['stone'] += stone_addnum[result[-1] - 1]

    # === 绘图 ===
    bg = BuildImage(1100, 900, color = white)
    # === 头像 ===
    base_info = get_item(student_data, 'Id', result[0])
    dev_name = base_info['DevName']
    collection_file_path_webp = baImgPath + f'/source/student/collection/{base_info["CollectionTexture"]}.webp'
    collection_file_path = baImgPath + f'/source/student/collectionpng/{base_info["CollectionTexture"]}.png'
    if not os.path.exists(collection_file_path):
        image_exist_check(collection_file_path_webp, f'https://raw.githubusercontent.com/lonqie/SchaleDB/main/images/student/collection/{base_info["CollectionTexture"]}.webp')
        collection_png = Image.open(collection_file_path_webp)
        collection_png.load()
        collection_png.save(collection_file_path)
    collection_icon = BuildImage(0, 0, background = collection_file_path)
    bg.paste(collection_icon, (int(550 - collection_icon.w / 2), int(460 - collection_icon.h / 2)), alpha=True)

    # 中间层背景
    blue_bg_path = os.path.join(baImgPath + '/source/gacha/background_1.png')
    blue_bg = BuildImage(0, 0, background=blue_bg_path)
    bg.paste(blue_bg, (0, 0), alpha=True)

    # 边框
    stu_star = min(3, result[-1])
    frame_path = os.path.join(baImgPath + f'/source/gacha/star_grade_{stu_star}.png')
    frame = BuildImage(0, 0, background=frame_path)
    bg.paste(frame, (425, 262), alpha=True)

    # 新角色或up
    flag_type = flag_list[_flag]
    if flag_type:
        flag_path = os.path.join(baImgPath + f'/source/gacha/{flag_type}')
    #93, 116
        flag = BuildImage(0, 0, background=flag_path)
        bg.paste(flag, (488, 329), alpha=True)

    #point
    point_text = BuildImage(0, 0, plain_text=str(user_dict[userid]['point'] + 1),
                            font_size=22,
                            font_color=white,
                            font='arialbd.ttf')
    bg.paste(point_text, (int(949 - point_text.w / 2), 823), alpha=True)

    #stone
    stone_text = BuildImage(0, 0, plain_text=f"{user_dict[userid]['stone'] - 120}",
                            font_size=24,
                            font_color=(31, 87, 129),
                            font='arialbd.ttf')
    bg.paste(stone_text, (int(198 - stone_text.w / 2), 814), alpha=True)

    #抽卡信息:
    if mode == 99:
        mode_text = 'Normal'
    else:
        mode_text = mode + 1
    info_text = BuildImage(0, 0, plain_text=f'Gacha QQ:{uid}, ID:{mode_text}',
                           font_size=24,
                           font_color=(31, 87, 29),
                           font='arialbd.ttf')
    bg.paste(info_text, (1, 1), alpha=True)

    user_dict[userid]['stone'] -= 120
    user_dict[userid]['gacha_count'] += 1
    user_dict[userid]['point'] += 1
    saveData(user_dict, recordPath)

    if save_gacha_pic:
        bg.save(os.path.join(baImgPath, 'gacha.png'))
    imageToSend = f"[CQ:image,file=base64://{bg.pic2bs4()}]"
    return imageToSend


def increase_value(uid: int, key: str, count: int):
    """
        增加 数量

    :param uid: QQ号
    :param key: 键：stone/gacha_count/point
    :param count: 正数增加，负数减少
    """
    user_dict = loadData(recordPath)
    userid = str(uid)
    if str(uid) not in user_dict:
        user_dict[userid] = {
            'stone': 0,
            'gacha_count': 0,
            'point': 0,
            'students': {}
        }
    user_dict[userid][key] = user_dict[userid][key] + count
    if user_dict[userid][key] < 0:
        user_dict[userid][key] = 0
    saveData(user_dict, recordPath)


def change_mode(uid: int, mode: int):
    mode_dict = loadData(os.path.join(os.path.dirname(__file__), 'gacha/modedata.json'))
    mode_dict[str(uid)] = mode
    saveData(mode_dict, os.path.join(os.path.dirname(__file__), 'gacha/modedata.json'))


def check_mode(uid: int):
    mode_dict = loadData(os.path.join(os.path.dirname(__file__), 'gacha/modedata.json'))
    if str(uid) not in mode_dict:
        mode_dict[str(uid)] = 99
        saveData(mode_dict, os.path.join(os.path.dirname(__file__), 'gacha/modedata.json'))
        return 99
    else:
        return mode_dict[str(uid)]


def gacha_1(mode: int):
    randnum = random.randint(1, 1000)
    if randnum < 765:
        get_id = random.choice(gacha_pool['star1_0'])
        star = 1
    elif 765 <= randnum < 950:
        get_id = random.choice(gacha_pool['star2_0'])
        star = 2
    else:
        if mode < 10:
            picknum = random.randint(1, 300)
            if picknum < 230:
                get_id = random.choice(gacha_pool['star3_0'])
                star = 3
                if get_id == gacha_pool['pickup'][mode]:
                    star = 4
            else:
                get_id = gacha_pool['pickup'][mode]
                star = 4
        else:
            get_id = random.choice(gacha_pool['star3_0'])
            star = 3
    return get_id, star


def gacha_10(mode: int):
    result_list = []
    for num in range(9):
        randnum = random.randint(1, 1000)
        if randnum < 775:
            get_id = random.choice(gacha_pool['star1_0'])
            star = 1
        elif 775 <= randnum < 960:
            get_id = random.choice(gacha_pool['star2_0'])
            star = 2
        else:
            if mode < 10:
                picknum = random.randint(1, 300)
                if picknum < 230:
                    get_id = random.choice(gacha_pool['star3_0'])
                    star = 3
                    if get_id == gacha_pool['pickup'][mode]:
                        star = 4
                else:
                    get_id = gacha_pool['pickup'][mode]
                    star = 4
            else:
                get_id = random.choice(gacha_pool['star3_0'])
                star = 3
        result_list.append((get_id, star))

    num10th = random.randint(1, 1000)
    if num10th < 970:
        get_id = random.choice(gacha_pool['star2_0'])
        star = 2
    else:
        if mode < 10:
            picknum = random.randint(1, 300)
            if picknum < 230:
                get_id = random.choice(gacha_pool['star3_0'])
                star = 3
                if get_id == gacha_pool['pickup'][mode]:
                    star = 4
            else:
                get_id = gacha_pool['pickup'][mode]
                star = 4
        else:
            get_id = random.choice(gacha_pool['star3_0'])
            star = 3
    result_list.append((get_id, star))
    return result_list


def get_item(_dict, key, value):
    """
    根据键获取特定对象信息

    :param _dict: 需要检索的字典
    :param key: 需要检索的键
    :param value: 需要匹配的键
    """
    for item in _dict:
        if item[key] == value:
            return item


def saveData(obj, fp):
    """
        保存文件
    """
    with open(fp, 'w', encoding='utf-8') as file:
        ujson.dump(obj, file, ensure_ascii=False)


def loadData(fp):
    """
        加载json，不存在则创建
    """
    if os.path.exists(fp):
        file = ujson.load(open(fp, 'r', encoding='utf-8'))
        return file
    else:
        empty_dict = {}
        with open(fp, 'w', encoding='utf-8') as file:
            ujson.dump(empty_dict, file, ensure_ascii=False)
        return empty_dict


if __name__ == '__main__':
    # increase_value(10001, 'stone', 1000000)
    get_1_gacha(10001, 1)
    '''for i in range(201):
        _id, star = gacha_1(1)
        name = get_student_name(_id)
        _dict[f'star{star}_count'] += 1
        print(f'{name},{star}星')
    print(_dict)'''