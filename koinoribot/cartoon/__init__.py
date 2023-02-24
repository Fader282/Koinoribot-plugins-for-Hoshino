import json
from ..config import TXSecretId, TXSecretKey
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ft.v20200304 import ft_client, models

import hoshino
from asyncio import sleep
from hoshino import Service
from datetime import datetime, timedelta
from hoshino.util import DailyNumberLimiter, FreqLimiter
from nonebot import MessageSegment

sv = Service('人物卡通化')
DAILY_LIMIT = 10
SEARCH_TIMEOUT = 60
lmtd = DailyNumberLimiter(50)
flmt = FreqLimiter(30)


def faceCartoonImagePost(imageUrl):
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey,此处还需注意密钥对的保密

        cred = credential.Credential(TXSecretId, TXSecretKey)
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ft.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = ft_client.FtClient(cred, "ap-chengdu", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.FaceCartoonPicRequest()
        params = {
            "Url": imageUrl
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个FaceCartoonPicResponse的实例，与请求对象对应
        resp = client.FaceCartoonPic(req)
        # 输出json格式的字符串回包
        return resp.to_json_string()

    except TencentCloudSDKException as err:
        hoshino.logger.error(f"人物卡通化出错：{err}")


class PicListener:
    def __init__(self):
        self.on = {}
        self.count = {}
        self.limit = {}
        self.timeout = {}

    def get_on_off_status(self, gid):
        return self.on[gid] if self.on.get(gid) is not None else False

    def turn_on(self, gid, uid):
        self.on[gid] = uid
        self.count[gid] = 0
        self.limit[gid] = DAILY_LIMIT-lmtd.get_num(uid)
        self.timeout[gid] = datetime.now()+timedelta(seconds=SEARCH_TIMEOUT)

    def turn_off(self, gid):
        self.on.pop(gid)
        self.count.pop(gid)
        self.limit.pop(gid)
        self.timeout.pop(gid)

    def count_plus(self, gid):
        self.count[gid] += 1


piclstn = PicListener()


@sv.on_prefix(('3to2', '卡通化'))
async def image_to_cartoon(bot, ev):
    uid = ev.user_id
    gid = ev.group_id
    message = ev.message
    msgId = ev.message_id
    image_check = 0
    imageUrl = ''
    if piclstn.get_on_off_status(gid):
        if uid == piclstn.on[gid]:
            piclstn.timeout[gid] = datetime.now()+timedelta(seconds=15)
            await bot.finish(ev, f"冰祈正在等待将要卡通化的图片~")
        else:
            await bot.finish(ev, f"本群[CQ:at,qq={piclstn.on[gid]}]正在使用卡通化功能，请耐心等待~")
    if not flmt.check(uid):
        await bot.send(ev, f'卡通绘板正在重新准备中，休息一下再来吧~({round(flmt.left_time(uid))}s)')
        return
    for raw_dict in message:
        if raw_dict['type'] == 'image':
            image_check += 1
            imageUrl = raw_dict['data']['url']
            hoshino.logger.info(imageUrl)
    if image_check > 1:
        await bot.finish(ev, '一次只能给一张图片做卡通化喔')
    elif image_check == 1:
        await bot.send(ev, '正在卡通化，请稍候...')
        try:
            result = json.loads(faceCartoonImagePost(imageUrl))
        except Exception:
            await bot.send(ev, f'木有检测出三次元的人脸...')
            return
        imageBs64 = result['ResultImage']
        flmt.start_cd(uid)
        await bot.send(ev, f'[CQ:image,file=base64://{imageBs64}]')
    elif image_check == 0:
        await bot.send(ev, '收到，请发送要卡通化的图片~')
        piclstn.turn_on(gid, uid)
        await sleep(SEARCH_TIMEOUT)
        if piclstn.get_on_off_status(gid):
            if datetime.now() < piclstn.timeout[gid]:
                piclstn.turn_off(gid)
                await bot.finish(ev, "好像没有发送任何图片，冰祈稍微休息一下~")


@sv.on_message('group')
async def picture_listener(bot, ev):
    if piclstn.get_on_off_status(ev.group_id):
        message = ev.message
        msgId = ev.message_id
        image_check = 0
        for raw_dict in message:
            if raw_dict['type'] == 'image':
                image_check += 1
                imageUrl = raw_dict['data']['url']
        if image_check > 1:
            piclstn.turn_off(ev.group_id)
            await bot.finish(ev, '一次只能卡通化一张图片喔')
        elif image_check == 1:
            await bot.send(ev, '正在卡通化，请稍候...')
            try:
                result = json.loads(faceCartoonImagePost(imageUrl))
            except Exception:
                piclstn.turn_off(ev.group_id)
                await bot.send(ev, f'木有检测出三次元的人脸...')
                return
            imageBs64 = result['ResultImage']
            piclstn.turn_off(ev.group_id)
            flmt.start_cd(ev.user_id)
            await bot.send(ev, f'[CQ:image,file=base64://{imageBs64}]')
