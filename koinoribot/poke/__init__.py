#-*- coding:utf-8 -*-
import hoshino
import os
import random
from hoshino import Service, util
from hoshino.typing import MessageSegment, NoticeSession, CQEvent
from ..GroupFreqLimiter import *
from ..build_image import BuildImage
from .. import money
from .._R import get, imgPath

sv = Service('戳戳反应', bundle='pcr娱乐', help_='''
戳戳冰祈，冰祈会有回应！
如果冰祈发出了“nya~”，则说明获得了25颗星星
如果冰祈发出了“欸嘿嘿”，则说明获得了10枚金币
'''.strip())

poke_count = {}
poke_limit = {}

POKE_GET = 0.9           # 不回戳的概率

face_o = ['呆_白.jpg', '呆_黑.jpg', '呆_混合.jpg', '呆_黑_2.jpg', '呆_混合_R.jpg']  # O组表情
face_a = ['不可以A_白.jpg', '不可以A_黑.jpg', '不可以A_混合.jpg', '不可以A_混合_R.jpg']  # A组表情
face_b = ['不可以B_白.jpg', '不可以B_黑.jpg', '不可以B_混合.jpg', '不可以B_混合_R.jpg']  # B组表情
feed_back = ['不可以戳戳>_<', '要戳坏掉了>_<']  # 文字表情
poke_back = ['戳_白.jpg', '戳_混合.jpg', '戳_混合_bb.jpg', '戳_混合_wb.jpg', '戳_混合_ww.jpg',
             '戳_黑.jpg', '戳_混合_R.jpg', '戳_混合_Rbb.jpg', '戳_混合_Rwb.jpg', '戳_混合_Rww.jpg',
             '戳_黑.jpg', '戳_白.jpg', '戳_白.jpg', '戳_黑.jpg', '戳_白.jpg', '戳_黑.jpg']  # 反戳表情
good_back = ['欸嘿嘿_白.jpg', '欸嘿嘿_混合.jpg', '欸嘿嘿_混合_bb.jpg', '欸嘿嘿_混合_wb.jpg', '欸嘿嘿_混合_ww.jpg',
             '欸嘿嘿_黑.jpg', '欸嘿嘿_混合_R.jpg', '欸嘿嘿_混合_Rbb.jpg', '欸嘿嘿_混合_Rwb.jpg', '欸嘿嘿_混合_Rww.jpg',
             '欸嘿嘿_白.jpg', '欸嘿嘿_黑.jpg', '欸嘿嘿_白.jpg', '欸嘿嘿_黑.jpg', '欸嘿嘿_白.jpg', '欸嘿嘿_黑.jpg']  # 欸嘿嘿表情
face_ugo = ['戳_动图.gif']

path = os.path.join(imgPath, "poke_emo")


@sv.on_notice('notify.poke')
async def poke_back_function(session: NoticeSession):
    uid = session.ctx['user_id']
    gid = session.ctx['group_id']
    last_time = session.ctx['time']
    if hoshino.priv.check_block_user(uid):
        return
    at_user = MessageSegment.at(session.ctx['user_id'])
    guid = session.ctx['group_id'], session.ctx['user_id']
    if session.ctx['target_id'] != session.event.self_id:
        return

    if check_reload_group(group_id = gid, _type = 'boolean'):  # 整个群的冷却
        remain_time = check_reload_group(group_id = gid, _type = 'number')
        force_awake = random.random()
        if force_awake >= remain_time / 180:
            set_reload_group(group_id = gid, _time = 0)
            await session.send(get('poke_emo/惊醒.jpg').cqcode)
        return
    else:
        if str(gid) not in poke_limit.keys():
            poke_limit[str(gid)] = last_time
        else:
            if int(last_time) < int(poke_limit[str(gid)]) + 3:
                return
            else:
                poke_limit[str(gid)] = last_time
        if str(gid) in poke_count.keys():
            poke_count[str(gid)]['count'] += 1
        else:
            poke_count[str(gid)] = {}
            poke_count[str(gid)]['count'] = 1
            poke_count[str(gid)]['max'] = random.randint(10, 20)
        if poke_count[str(gid)]['count'] > poke_count[str(gid)]['max']:
            cool_time = random.randint(180, 360)
            set_reload_group(group_id = gid, _time = cool_time)
            poke_count[str(gid)]['count'] = 0
            poke_count[str(gid)]['max'] = random.randint(10, 20)
            await session.send(f'坏...掉了...')
            await session.send(get('poke_emo/昏倒.jpg').cqcode)
            return

    if random.random() > POKE_GET:
        await session.send("戳回去")
        pokeBackImg = random.choice(poke_back)
        image_file = BuildImage(0, 0, background=f"{os.path.join(path,pokeBackImg)}", ratio = 0.5)
        poke = MessageSegment(type_='poke',
                              data={
                                  'qq': str(session.ctx['user_id']),
                              })
        await session.send(poke)
        await session.bot.send_group_msg(group_id = gid, message = f'[CQ:image,file=base64://{image_file.pic2bs4()}]')
#        await session.send(R.img(random.choice(face_back)).cqcode)
    else:
        if True:
            a = random.random()
            if a < 0.1:
                money.increase_user_money(uid,"starstone",50)
                await session.send(f'nya~')
            elif a < 0.3:
                face_o_img = random.choice(face_o)
                image_file = BuildImage(0, 0, background=f"{os.path.join(path,face_o_img)}", ratio = 0.5)
                await session.bot.send_group_msg(group_id = gid, message = f'[CQ:image,file=base64://{image_file.pic2bs4()}]')
    #            await session.send(R.img(face_o_choice).cqcode)
            elif a <= 0.496:
                face_a_img = random.choice(face_a)
                image_file = BuildImage(0, 0, background=f"{os.path.join(path,face_a_img)}", ratio = 0.5)
                await session.bot.send_group_msg(group_id = gid, message = f'[CQ:image,file=base64://{image_file.pic2bs4()}]')
    #            await session.send(R.img(face_a_choice).cqcode)
            elif a > 0.496 and a < 0.504:
                bonus_gold = random.randint(25, 100)
                money.increase_user_money(uid,"gold", bonus_gold)
                money.increase_user_money(uid, "luckygold", 2)
                await session.send(f"戳到了一个彩蛋~获得了{bonus_gold}枚金币与两枚幸运币!{get('emotion/震惊.png').cqcode}")
            elif a <= 0.7:
                face_b_img = random.choice(face_b)
                image_file = BuildImage(0, 0, background=f"{os.path.join(path,face_b_img)}", ratio = 0.5)
                await session.bot.send_group_msg(group_id = gid, message = f'[CQ:image,file=base64://{image_file.pic2bs4()}]')
    #            await session.send(R.img(face_b_choice).cqcode)
            elif a > 0.7 and a < 0.9:
                feed_back_choice = random.choice(feed_back)
                await session.send(feed_back_choice)
            elif a >= 0.9:
                money.increase_user_money(uid,"gold",10)
                goodBackImg = random.choice(good_back)
                image_file = BuildImage(0, 0, background=f"{os.path.join(path,goodBackImg)}", ratio = 0.5)
                good_image_file = f"[CQ:image,file=base64://{image_file.pic2bs4()}]"
                await session.send(f'诶嘿嘿')
                await session.send(good_image_file)
            else:
                return
