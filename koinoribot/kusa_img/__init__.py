from hoshino import Service
from aiocqhttp.exceptions import ActionFailed
from hoshino.typing import CQEvent
from hoshino.util import escape
from ..build_image import BuildImage
import requests
import warnings
import time
import uuid
import hashlib
import os
import re

from .._R import get
from ..utils import get_net_img
from ..config import youdao_secret, youdao_appkey

no = f"{get('emotion/no.png').cqcode}"
sv_help = '''
生成黑白草图，带上图片与文字
'''.strip()

sv = Service('黑白草图', visible = True, enable_on_default = True, help_ = sv_help)
length_of_text = 19
true = "true"
false = "flse"
YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = youdao_appkey
APP_SECRET = youdao_secret
data = {}


@sv.on_prefix('黑白图')
async def black_white_image(bot, ev):
    message = ev.message
    text = ''  # 检查文字
    image_check = 0  # 检查图片数
    bimg = ''
    for raw_dict in message:
        if raw_dict['type'] == 'text':
            text += raw_dict['data']['text']
        if raw_dict['type'] == 'image':
            image_check += 1
            if image_check > 1:
                await bot.send(ev, '只可以使用一张图片' + no)
                return
            image = raw_dict['data']['url']
            bimg = await get_net_img(image)
            '''r = requests.get(image)
            with open(os.path.join(os.path.dirname(__file__), f"picture/{ev.user_id}.jpg"), "wb") as f:
                f.write(r.content)'''
    if len(text) >= length_of_text:
        await bot.send(ev, '字数不能超过十五个字' + no)
        return
    if len(text) == 0 or image_check == 0:
        await bot.send(ev, '请将图片与文字一起附上~')
        return
    data['to'] = 'ja'
    imageFile = os.path.join(os.path.dirname(__file__), f'picture/{ev.user_id}.jpg')
    trans_msg = str(sconnect(escape(text)))
    msg = text + '<|>' + trans_msg
    black_img = bimg
    black_img.convert("L")
    msg_sp = msg.split("<|>")
    w, h = black_img.size
    add_h, font_size = init_h_font_size(h)
    bg = BuildImage(w, h + add_h, color="black", font_size=font_size * 1.5, font = "HYWenHei-85W.ttf")
    bg.paste(black_img)
    chinese_msg = formalization_msg(msg)
    cn_size = bg.getsize(msg_sp[0])[0]
    jp_size = bg.getsize(msg_sp[1])[0]
#    if not bg.check_font_size(chinese_msg):
#        if len(msg_sp) == 1:
#            centered_text(bg, chinese_msg, add_h)
#            hoshino.logger.info("A")
#        else:
#            centered_text(bg, chinese_msg + "<|>" + msg_sp[1], add_h)
#            hoshino.logger.info("B")
#    elif not bg.check_font_size(msg_sp[0]):
#        centered_text(bg, msg, add_h)
#        hoshino.logger.info("C")
#    else:
        #ratio = (bg.getsize(msg_sp[0])[0] + 20) / bg.w
    ratio = (max(cn_size, jp_size, w) + 20) / bg.w
    add_h = add_h * ratio
    bg.resize(ratio)
    centered_text(bg, msg, add_h)
    imageToSend = f"[CQ:image,file=base64://{bg.pic2bs4()}]"
    try:
        await bot.send(ev, imageToSend)
    except ActionFailed:
        await bot.send(ev, '结果发送失败，冰祈可能被风控...')


@sv.on_message('group')  # 回复制图
async def replymbwimage(bot, ev: CQEvent):
    mid = ev.message_id
    uid = ev.user_id
    ret = re.search(r"\[CQ:reply,id=(-?\d*)\](.*)黑白图(.*)", str(ev.message))
    if not ret:
        return
    replyMessageId = ret.group(1)
    cmdContent = ret.group(3)
    try:
        replyMessage = await bot.get_msg(self_id=ev.self_id, message_id=int(replyMessageId))
    except ActionFailed:
        await bot.finish(ev, '该消息已过期，请重新转发~')
    ret = re.search(r"\[CQ:image,file=(.*)?,url=(.*)\]", str(replyMessage["message"]))
    if not ret:
        await bot.send(ev, '未找到图片~')
        return
    url = ret.group(2)
    text = cmdContent.strip()  # 检查文字
    bimg = await get_net_img(url)
    if len(text) >= length_of_text - 4:
        await bot.send(ev, '字数不能超过十五个字' + no)
        return
    if len(text) == 0:
        await bot.send(ev, '请附上文字~')
        return
    data['to'] = 'ja'
    trans_msg = str(sconnect(escape(text)))
    msg = text + '<|>' + trans_msg
    black_img = bimg
    black_img.convert("L")
    msg_sp = msg.split("<|>")
    w, h = black_img.size
    add_h, font_size = init_h_font_size(h)
    bg = BuildImage(w, h + add_h, color="black", font_size=font_size * 1.5, font = "HYWenHei-85W.ttf")
    bg.paste(black_img)
    chinese_msg = formalization_msg(msg)
    cn_size = bg.getsize(msg_sp[0])[0]
    jp_size = bg.getsize(msg_sp[1])[0]
#    if not bg.check_font_size(chinese_msg):
#        if len(msg_sp) == 1:
#            centered_text(bg, chinese_msg, add_h)
#            hoshino.logger.info("A")
#        else:
#            centered_text(bg, chinese_msg + "<|>" + msg_sp[1], add_h)
#            hoshino.logger.info("B")
#    elif not bg.check_font_size(msg_sp[0]):
#        centered_text(bg, msg, add_h)
#        hoshino.logger.info("C")
#    else:
        #ratio = (bg.getsize(msg_sp[0])[0] + 20) / bg.w
    ratio = (max(cn_size, jp_size, w) + 20) / bg.w
    add_h = add_h * ratio
    bg.resize(ratio)
    centered_text(bg, msg, add_h)
    imageToSend = f"[CQ:image,file=base64://{bg.pic2bs4()}]"
    try:
        await bot.send(ev, imageToSend)
    except ActionFailed:
        await bot.send(ev, '结果发送失败，冰祈可能被风控...')


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def sconnect(q):
    warnings.simplefilter('ignore',ResourceWarning)
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['from'] = 'auto'
    data['appKey'] = APP_KEY
    data['q']=q
    data['salt'] = salt
    data['sign'] = sign
    data['vocabId'] = "您的用户词表ID"

    response = do_request(data)
    contentType = response.headers['Content-Type']
    if contentType == "audio/mp3":
        pass
        millis = int(round(time.time() * 1000))
        filePath = "合成的音频存储路径" + str(millis) + ".mp3"
        fo = open(filePath, 'wb')
        fo.write(response.content)
        fo.close()
    else:
        ssr=response.content
        str1=str(ssr, encoding = "utf-8")
        sss=eval(str1)
        if not 'basic' in sss.keys():
            return sss['translation'][0]

        return sss['basic']['explains']

'''
async def get_translate(msg: str) -> str:
    url = f"http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null"
    data = {
        "type": "ZH_CN2JA",
        "i": msg,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true",
    }
    data = (await AsyncHttpx.post(url, data=data)).json()
    if data["errorCode"] == 0:
        translate = data["translateResult"][0][0]["tgt"]
        msg += "<|>" + translate
    return msg
'''

def formalization_msg(msg: str) -> str:
    rst = ""
    for i in range(len(msg)):
        if is_chinese(msg[i]):
            rst += msg[i] + " "
        else:
            rst += msg[i]
        if i + 1 < len(msg) and is_chinese(msg[i + 1]) and msg[i].isalpha():
            rst += " "
    return rst.strip()


def is_chinese(word: str) -> bool:
    """
    说明：
        判断字符串是否为纯中文
    参数：
        :param word: 文本
    """
    for ch in word:
        if not "\u4e00" <= ch <= "\u9fff":
            return False
    return True


def init_h_font_size(h):
    #       高度      字体
    if h < 400:
        return init_h_font_size(400)
    elif 400 < h < 800:
        return init_h_font_size(800)
    return h * 0.2, h * 0.05


def centered_text(img: BuildImage, text: str, add_h: int):
    top_h = img.h - add_h + (img.h / 100)
    bottom_h = img.h - (img.h / 100)
    text_sp = text.split("<|>")
    w, h = img.getsize(text_sp[0])
    if len(text_sp) == 1:
        w = int((img.w - w) / 2)
        h = int(top_h + (bottom_h - top_h - h) / 2)
        img.text((w, h), text_sp[0], (255, 255, 255))
    else:
        br_h = int(top_h + (bottom_h - top_h) / 2)
        w = int((img.w - w) / 2)
        h = int(top_h + (br_h - top_h - h) / 2)
        img.text((w, h), text_sp[0], (255, 255, 255))
        w, h = img.getsize(text_sp[1])
        w = int((img.w - w) / 2)
        h = int(br_h + (bottom_h - br_h - h) / 2)
        img.text((w, h), text_sp[1], (255, 255, 255))
