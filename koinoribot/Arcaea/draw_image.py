import asyncio
import os

import hoshino
from ..build_image import BuildImage
from typing import Union, Optional
from .get_info import getUserInfo, getUserBest, getSongPic, getIcon, getUserBest30
from .get_info import srcPath, songPath, rootPath, iconPath, layoutsPath, dbPath
from .util import call_count, clearType2icon, clearType2bar, diffTrans, score2icon, ptt2icon, loadData, timeTrans

save_image = False
debug_mode = False

fontBR = 'Beatrice.ttf'
fontExo = 'Exo-Medium.ttf'
fontKaze = 'Kazesawa-Regular.ttf'
fontGeo = 'GeosansLight.ttf'
fontNotoBold = 'NotoSansCJKtc-Bold.otf'
ftColorWhite = (243, 243, 243)
ftColorDarkGrey = (74, 73, 73)
ftColorGrey = (107, 107, 107)
ftColorBlack = (21, 21, 21)

ftColorGold = (254, 187, 65)
ftColorSilver = (179, 178, 183)
ftColorBronze = (245, 149, 107)

ftColorPure = (38, 151, 191)
ftColorFar = (255, 133, 9)
ftColorLost = (217, 11, 72)


async def getOneRecord(
        user: Union[str, int],
        mode: str = 'recent',
        is_hide: int = 0,
        song_id: Optional[str] = None,
        difficulty: Optional[str] = None):
    """
        单曲成绩图

        :param user: 玩家名称，或玩家好友码(建议)
        :param mode: recent/best 模式
        :param is_hide: 是否隐藏个人信息
        :param song_id: 曲目id，如果mode为best则必填
        :param difficulty: 曲目难度，如果mode为best则必填
    """
    #后面在这里加try-except
    #user_info = loadData(os.path.join(rootPath, 'user_info.json'))                                                    #########
    hoshino.logger.info(f'查询{user}单曲成绩...')
    call_count(1)
    if mode == 'recent':
        user_info = await getUserInfo(user=user, recent = 1, with_song_info='true')
    else:
        user_info = await getUserBest(user=user, song=song_id, difficulty=difficulty, with_song_info='true')
    if user_info['status'] != 0:
        hoshino.logger.info(f"查询成绩失败,{user_info['message']}")
        return f"冰祈搞砸了QAQ，只带回来了这个：{user_info['message']}"
    hoshino.logger.info(f'查询单曲成绩成功')
    acc_info = user_info['content']['account_info']
    username = acc_info['name']  # 玩家名
    user_rating = acc_info['rating']  # 玩家ptt
    if is_hide:
        user_rating = -1
        username = f'{username[0]}####{username[-1]}'
    user_icon = acc_info['character']  # 玩家头像

    if mode == 'recent':
        if user_info['content']['recent_score']:
            play_info = user_info['content']['recent_score'][0]
        else:
            return '没有最近游玩成绩...'
    else:
        play_info = user_info['content']['record']
    score = play_info['score']  # 得分
    health = play_info['health']  # 回忆条
    rating = play_info['rating']  # 该曲ptt
    song_id = play_info['song_id']  # 歌曲id
    difficulty = play_info['difficulty']  # 0/1/2/3
    c_type_icon = clearType2icon(play_info['clear_type'])  # 通关类型
    c_type_bar = clearType2bar(play_info['clear_type'])  # 通关类型(tc条)
    _time = play_info['time_played']  # 游玩时间
    far = play_info['near_count']  # far
    lost = play_info['miss_count']  # lost
    pure = play_info['perfect_count']  # pure
    shiny_pure = play_info['shiny_perfect_count']  # 大pure

    song_info = user_info['content']['songinfo'][0]
    song_diff = diffTrans(song_info['difficulty'])  # 难度数值
    song_rating = song_info['rating']  # 铺面定数

    score_icon = score2icon(score)

    # ↓ 下面开始绘图 ↓

    hoshino.logger.info('开始绘制单曲成绩图')

    bgR_path = os.path.join(srcPath, 'score1_bg_r.jpg')
    bgB_path = os.path.join(srcPath, 'score1_bg_b.jpg')

    # === 背景
    if mode == 'recent':
        bg = BuildImage(0, 0,
                        background=bgR_path,
                        font_size=20,
                        font=fontBR)
    else:
        bg = BuildImage(0, 0,
                        background=bgB_path,
                        font_size=20,
                        font_color=fontBR)

    # === 曲封面
    song_pic_resp = await getSongPic(song_id = song_id, difficulty=difficulty)
    if song_pic_resp['status'] == 0:
        song_pic_path = song_pic_resp['message']
    else:
        song_pic_path = os.path.join(songPath, 'unknown.jpg')
    song_pic = BuildImage(0, 0, background=song_pic_path)
    bg.paste(song_pic, (28, 280))

    # === 回忆条百分比
    mmr_rate = BuildImage(0, 0,
                          plain_text=f'{health}%',
                          font_size=30,
                          font=fontBR,
                          font_color=ftColorWhite)
    bg.paste(mmr_rate, (int(867 - mmr_rate.w), 307), True)

    # 游玩时间
    date = timeTrans(str(_time)[:10])
    date_text = BuildImage(0, 0,
                           plain_text=date,
                           font_size=30,
                           font=fontBR,
                           font_color=ftColorWhite)
    bg.paste(date_text, (int(1385 - date_text.w), 307), True)

    # === 得分
    s_1 = str.zfill(str(score), 8)  # 补零09'980'270
    s_2 = list(s_1)
    s_2.insert(2, "'")
    s_2.insert(6, "'")  # 插入分号
    s_format = ''.join(s_2)
    score_text = BuildImage(0, 0,
                            plain_text=s_format,
                            font=fontGeo,
                            font_color=ftColorWhite,
                            font_size=80)
    bg.paste(score_text, (int(967 - score_text.w / 2), 365), True)

    # === 评级
    score_icon_path = os.path.join(layoutsPath, 'grade', f'{score_icon}.png')
    grade = BuildImage(0, 0, background=score_icon_path)
    bg.paste(grade, (1216, 354), True)

    # === 通关类型
    type_icon_path = os.path.join(layoutsPath, 'clear_type', f'{c_type_icon}.png')
    type_icon = BuildImage(0, 0, background=type_icon_path)
    bg.paste(type_icon, (1356, 353), True)

    # === pure数量
    pure_text = BuildImage(0, 0,
                           plain_text=f'{pure} (+{shiny_pure})',
                           font=fontBR,
                           font_size=38,
                           font_color=ftColorGrey,
                           border=2,
                           border_color=ftColorWhite)
    bg.paste(pure_text, (753, 568), True)

    # === far数量
    far_text = BuildImage(0, 0,
                          plain_text=str(far),
                          font=fontBR,
                          font_size=38,
                          font_color=ftColorGrey,
                          border=2,
                          border_color=ftColorWhite)
    bg.paste(far_text, (753, 630), True)

    # === lost数量
    lost_text = BuildImage(0, 0,
                           plain_text=str(lost),
                           font=fontBR,
                           font_size=38,
                           font_color=ftColorGrey,
                           border=2,
                           border_color=ftColorWhite)
    bg.paste(lost_text, (753, 692), True)

    # === 单曲ptt
    ptt_text = BuildImage(0, 0,
                          plain_text=f'{rating:.3f}',
                          font=fontBR,
                          font_size=30,
                          font_color=ftColorWhite
                          )
    bg.paste(ptt_text, (int(868 - ptt_text.w), 471), True)

    # === 定数
    s_rating = list(str(song_rating))
    s_rating.insert(-1, '.')
    _song_rating = ''.join(s_rating)
    rating_text = BuildImage(0, 0,
                             plain_text=f'{_song_rating}',
                             font=fontBR,
                             font_size=30,
                             font_color=ftColorWhite
                             )
    bg.paste(rating_text, (int(1370 - rating_text.w), 471), True)

    # === 用户头像
    user_icon_resp = await getIcon(user_icon)
    if user_icon_resp['status'] == 0:
        user_icon_path = user_icon_resp['message']
    else:
        user_icon_path = os.path.join(iconPath, 'unknown_icon.png')
    _icon = BuildImage(0, 0, background=user_icon_path)
    bg.paste(_icon, (1277, 566), True)

    # === 用户ptt底版
    rating_name = ptt2icon(user_rating)
    rating_icon_path = os.path.join(srcPath, 'rating', f'{rating_name}.png')
    rating_icon = BuildImage(0, 0, background=rating_icon_path)
    bg.paste(rating_icon, (1362, 652), True)

    # ===用户ptt
    if user_rating >= 0:
        if user_rating >= 1000:
            r_1 = list(str(user_rating))
            r_1.insert(2, '.')
            _rating = ''.join(r_1)
        elif user_rating >= 100:
            r_1 = list(str(user_rating))
            r_1.insert(1, '.')
            _rating = ''.join(r_1)
        else:
            user_rating = str.zfill(str(user_rating), 3)
            r_1 = list(user_rating)
            r_1.insert(1, '.')
            _rating = ''.join(r_1)
        user_rating_text = BuildImage(0, 0,
                                      plain_text=_rating,
                                      font_size=40,
                                      font = fontExo,
                                      font_color=ftColorWhite,
                                      border = 3,
                                      border_color=ftColorDarkGrey)
        bg.paste(user_rating_text, (int(1421 - user_rating_text.w / 2), 681), True)

    # === 用户名
    name_text = BuildImage(0, 0,
                           plain_text=username,
                           font_size=40,
                           font=fontBR,
                           font_color=ftColorDarkGrey)
    if name_text.w > 420:
        name_text.resize(w = 420, h = name_text.h)
    bg.paste(name_text, (int(1295 - name_text.w), int(725 - name_text.h)), True)

    # === 通关类型 条 (365, 176)
    type_bar_path = os.path.join(layoutsPath, 'clear', f'clear_{c_type_bar}.png')
    type_bar = BuildImage(0, 0, background=type_bar_path)
    bg.paste(type_bar, (365, int(216.5 - type_bar.h / 2)), True)

    # === 难度框 (0, 25)
    diff_bar_path = os.path.join(layoutsPath, 'difficulty', f'{difficulty}.png')
    diff_bar = BuildImage(0, 0, background=diff_bar_path)
    bg.paste(diff_bar, (0, 25), True)

    # === 难度值 (, 64)
    song_diff_text = BuildImage(0, 0,
                                plain_text=song_diff,
                                font_size=44,
                                font_color=ftColorWhite,
                                font=fontExo)
    bg.paste(song_diff_text, (int(100 - song_diff_text.w / 2), 52), True)

    # === 曲名
    song_name = song_info['name_en']
    song_name_text = BuildImage(0, 0,
                                plain_text=song_name,
                                font_size=50,
                                font_color=ftColorWhite,
                                font=fontKaze)
    bg.paste(song_name_text, (int(769 - song_name_text.w / 2), 35), True)

    # 曲师
    song_artist = song_info['artist']
    song_artist_text = BuildImage(0, 0,
                                  plain_text=song_artist,
                                  font_size=24,
                                  font_color=ftColorWhite,
                                  font=fontKaze)
    bg.paste(song_artist_text, (int(769 - song_artist_text.w / 2), 96), True)

    hoshino.logger.info('单曲成绩绘制完成')

    if save_image:
        bg.save(path = os.path.join(rootPath, f'cache/{user}_1.jpg'))
    imageToSend = f"[CQ:image,file=base64://{bg.pic2bs4()}]"
    return imageToSend


async def get30Record(user: Union[int, str], is_b40 = False, is_hide: int = 0):
    """
        获取b30&b40成绩
    """
    # 后面在这里加try-except
    # jsondata = loadData(os.path.join(rootPath, 'user_best_30.json'))
    hoshino.logger.info(f'开始获取{user}的best30成绩')
    call_count(1)
    jsondata = await getUserBest30(user = user, overflow=9)
    if jsondata['status'] != 0:
        hoshino.logger.info(f"{user}的best30成绩获取失败，{jsondata['message']}")
        return f"冰祈搞砸了QAQ，只带回来了这个：{jsondata['message']}"
    hoshino.logger.info(f'{user}的best30成绩获取成功')
    sidedata = loadData(os.path.join(dbPath, 'side_dict.json'))
    ratingdata = loadData(os.path.join(dbPath, 'rating_dict.json'))
    namedata = loadData(os.path.join(dbPath, 'name_en_dict.json'))
    user_info = jsondata['content']['account_info']
    username = user_info['name']  # 玩家名
    user_rating = user_info['rating']  # 玩家ptt
    user_icon = user_info['character']  # 玩家头像
    user_code = user_info['code']  # 好友码

    if is_hide:
        user_rating = -1
        username = f'{username[0]}####{username[-1]}'
        user_code = f'{str(user_code)[0]}xxxxxxx{str(user_code)[0]}'

    b30_avg = jsondata['content']['best30_avg']
    r10_avg = jsondata['content']['recent10_avg']
    user_best_list = list(jsondata['content']['best30_list'])

    if is_b40:
        user_best_list += list(jsondata['content']['best30_overflow'])
        bg_path = os.path.join(srcPath, 'score_40_bg.jpg')
    else:
        bg_path = os.path.join(srcPath, 'score_30_bg.jpg')

    # ====================== 开始绘图
    hoshino.logger.info('开始绘制best30成绩图')
    # === 背景
    bg = BuildImage(0, 0, background=bg_path)

    # === 用户头像
    user_icon_resp = await getIcon(user_icon)
    if user_icon_resp['status'] == 0:
        user_icon_path = user_icon_resp['message']
    else:
        user_icon_path = os.path.join(iconPath, 'unknown_icon.png')
    _icon = BuildImage(0, 0, background=user_icon_path)
    _icon.resize(ratio = 2)
    bg.paste(_icon, (1383, 100), True)

    # === 用户ptt底版
    rating_name = ptt2icon(user_rating)
    rating_icon_path = os.path.join(srcPath, 'rating', f'{rating_name}.png')
    rating_icon = BuildImage(0, 0, background=rating_icon_path)
    rating_icon.resize(ratio = 2)
    bg.paste(rating_icon, (1545, 258), True)

    # ===用户ptt
    if user_rating >= 0:
        if user_rating >= 1000:
            r_1 = list(str(user_rating))
            r_1.insert(2, '.')
            _rating = ''.join(r_1)
        elif user_rating >= 100:
            r_1 = list(str(user_rating))
            r_1.insert(1, '.')
            _rating = ''.join(r_1)
        else:
            user_rating = str.zfill(str(user_rating), 3)
            r_1 = list(user_rating)
            r_1.insert(1, '.')
            _rating = ''.join(r_1)
        user_rating_text = BuildImage(0, 0,
                                      plain_text=_rating,
                                      font_size=80,
                                      font = fontExo,
                                      font_color=ftColorWhite,
                                      border = 5,
                                      border_color=ftColorDarkGrey)
        bg.paste(user_rating_text, (int(1663 - user_rating_text.w / 2), 315), True)

    # === 用户名
    name_text = BuildImage(0, 0,
                           plain_text=username,
                           font_size=70,
                           font=fontBR,
                           font_color=ftColorDarkGrey)
    if name_text.w > 790:
        name_text.resize(w = 790, h = name_text.h)
    bg.paste(name_text, (int(1450 - name_text.w), int(395 - name_text.h / 2)), True)
    # === 好友码
    user_code_text = BuildImage(0, 0,
                                plain_text=f'ID:{user_code}',
                                font_size=35,
                                font=fontExo,
                                font_color=ftColorDarkGrey)
    bg.paste(user_code_text, (int(1399 - user_code_text.w), int(350 - user_code_text.h)), True)

    # === Best30平均值
    b30_avg = f'{b30_avg:.6f}'
    b30_avg_text = BuildImage(0, 0, plain_text=b30_avg,
                              font_size=50,
                              font_color=ftColorDarkGrey,
                              font=fontBR)
    bg.paste(b30_avg_text, (int(486 - b30_avg_text.w), 205), True)

    # === Recent10平均值
    r10_avg = f'{r10_avg:.6f}'
    r10_avg_text = BuildImage(0, 0, plain_text=r10_avg,
                              font_size=50,
                              font_color=ftColorDarkGrey,
                              font=fontBR)
    bg.paste(r10_avg_text, (int(549 - r10_avg_text.w), 408), True)

    for i in range(len(user_best_list)):
        play_info = user_best_list[i]
        score = play_info['score']  # 得分
        ptt = play_info['rating']  # 该曲ptt
        song_id = play_info['song_id']  # 歌曲id
        difficulty = play_info['difficulty']  # 0/1/2/3
        c_type_icon = clearType2icon(play_info['clear_type'])  # 通关类型(已转换)
        styled_time = timeTrans(str(play_info['time_played'])[:10])  # 游玩时间(已转换)
        far = play_info['near_count']  # far
        lost = play_info['miss_count']  # lost
        pure = play_info['perfect_count']  # pure
        shiny_pure = play_info['shiny_perfect_count']  # 大pure

        song_side = str(sidedata[song_id][difficulty])
        song_name = namedata[song_id][difficulty]
        song_rating = str(ratingdata[song_id][difficulty])
        if len(song_name) >= 20:
            song_name = f"{song_name[:20]}..."
        cell_bg_path = os.path.join(srcPath, f'b30_cell_{difficulty}.png')

        # === 单曲
        cell = BuildImage(0, 0, background=cell_bg_path)

        rank = f'#{i + 1}'
        if i == 0:
            rank_color = ftColorGold
        elif i == 1:
            rank_color = ftColorSilver
        elif i == 2:
            rank_color = ftColorBronze
        else:
            rank_color = ftColorDarkGrey

        # === 第几个曲子
        rank_text = BuildImage(0, 0, plain_text=rank,
                               font=fontNotoBold,
                               font_size=30,
                               font_color=rank_color)
        cell.paste(rank_text, (int(530 - rank_text.w), 0), True)

        # === 曲名
        name_text = BuildImage(0, 0, plain_text=song_name,
                               font=fontKaze,
                               font_size=35,
                               font_color=ftColorBlack)
        cell.paste(name_text, (25, 13), True)  # 曲名

        # === 得分
        s_1 = str.zfill(str(score), 8)  # 补零09'980'270
        s_2 = list(s_1)
        s_2.insert(2, "'")
        s_2.insert(6, "'")  # 插入分号
        s_format = ''.join(s_2)
        score_text = BuildImage(0, 0, plain_text=str(s_format),
                                font=fontBR,
                                font_size=38,
                                font_color=ftColorDarkGrey)
        cell.paste(score_text, (200, 78), True)

        # === pure
        pure_text = BuildImage(0, 0, plain_text=f"{pure} [+{shiny_pure}]",
                               font=fontExo,
                               font_size=20,
                               font_color=ftColorPure)
        cell.paste(pure_text, (254, 123), True)

        # ===
        far_text = BuildImage(0, 0, plain_text=str(far),
                              font=fontExo,
                              font_size=20,
                              font_color=ftColorFar)
        cell.paste(far_text, (254, 145), True)

        # ===
        lost_text = BuildImage(0, 0, plain_text=str(lost),
                               font = fontExo,
                               font_size=20,
                               font_color=ftColorLost)
        cell.paste(lost_text, (254, 167), True)

        # === 单曲ptt
        ptt_text = BuildImage(0, 0, plain_text=f'{round(ptt, 6)}',
                              font=fontExo,
                              font_size=19,
                              font_color=ftColorWhite,
                              border=2,
                              border_color=ftColorGrey)
        cell.paste(ptt_text, (254, 192), True)  # 单曲ptt

        # === 通关类型
        ct_icon_path = os.path.join(layoutsPath, f'clear_type/{c_type_icon}.png')
        if c_type_icon in ['pure', 'full']:
            ct_frame_path = os.path.join(srcPath, f'{c_type_icon}_frame.png')
            clear_frame = BuildImage(0, 0, background=ct_frame_path)
            cell.paste(clear_frame, (0, 0), True)
        clear_type = BuildImage(0, 0, background=ct_icon_path)
        clear_type.resize(ratio = 1.2)
        cell.paste(clear_type, (391, 86), True)  # 通关评级


        # === 曲绘
        song_pic_resp = await getSongPic(song_id = song_id, difficulty=difficulty)
        if song_pic_resp['status'] == 0:
            song_pic_path = song_pic_resp['message']
        else:
            song_pic_path = os.path.join(songPath, 'unknown.jpg')
        song_pic = BuildImage(0, 0, background=song_pic_path)
        song_pic.resize(ratio=0.25)
        cell.paste(song_pic, (55, 89), True)  # 封面

        # === 曲侧
        side_flag_path = os.path.join(srcPath, f'side_{song_side}.png')
        side_flag = BuildImage(0, 0, background=side_flag_path)
        cell.paste(side_flag, (28, 89), True)  # 光侧、对立侧、无色

        # === 定数
        s_rating = list(str(song_rating))
        s_rating.insert(-1, '.')
        _song_rating = ''.join(s_rating)
        song_rating_text = BuildImage(0, 0, plain_text=_song_rating,
                                      font=fontBR,
                                      font_size=25,
                                      font_color=ftColorDarkGrey)
        cell.paste(song_rating_text, (160, 223), True)  # 定数

        # === 游玩时间
        time_text = BuildImage(0, 0, plain_text=styled_time,
                               font = fontBR,
                               font_size=25,
                               font_color=ftColorDarkGrey)
        cell.paste(time_text, (390, 221), True)

        # === 贴上
        row = int(i / 3)
        column = int(i % 3)
        row_extra = int(i / 30)
        bg.paste(cell, (52 + column * 592, 700 + row * 322 + row_extra * 110), True)

    hoshino.logger.info('best30成绩图绘制完成')

    if save_image:
        bg.save(path = os.path.join(rootPath, f'cache/{user}_30.jpg'))
    imageToSend = f"[CQ:image,file=base64://{bg.pic2bs4()}]"
    return imageToSend


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # result = songName2Id('最强')
    result = loop.run_until_complete(
        get30Record(user = 174104696))
    # saveData(result, os.path.join(rootPath, 'user_best_30.json.json'))
    # print(result)

