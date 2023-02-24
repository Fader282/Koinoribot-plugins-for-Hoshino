import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tiia.v20190529 import tiia_client, models

from ..config import TXSecretId, TXSecretKey
from datetime import datetime, timedelta
from hoshino.util import DailyNumberLimiter, FreqLimiter
from asyncio import sleep
from nonebot import MessageSegment
from hoshino.util import ActionFailed

from hoshino import Service

sv = Service('图片美学评分', enable_on_default = True, help_ = '为图片打分')
testUrl = "https://gchat.qpic.cn/gchatpic_new/2307659105/834815564-2782180523-2547AD9B66F07D422877B405EEC6FA19/0?term=3"
DAILY_LIMIT = 10
SEARCH_TIMEOUT = 60
lmtd = DailyNumberLimiter(50)
flmt = FreqLimiter(30)


def AccessQualityPost(imageurl):
    try:
        cred = credential.Credential(TXSecretId, TXSecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tiia.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tiia_client.TiiaClient(cred, "ap-shanghai", clientProfile)

        req = models.AssessQualityRequest()
        params = {
            "ImageUrl": imageurl
        }
        req.from_json_string(json.dumps(params))

        resp = client.AssessQuality(req)
        return resp.to_json_string()

    except TencentCloudSDKException as err:
        return err


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


@sv.on_prefix(('美学评分', '美图打分', '美学打分', '美图评分'))
async def quality_score(bot, ev):

    uid = ev.user_id
    gid = ev.group_id
    message = ev.message
    msgId = ev.message_id
    image_check = 0
    imageUrl = ''
    if piclstn.get_on_off_status(gid):
        if uid == piclstn.on[gid]:
            piclstn.timeout[gid] = datetime.now()+timedelta(seconds=15)
            await bot.finish(ev, f"您已经在打分模式下啦！")
        else:
            await bot.finish(ev, f"本群[CQ:at,qq={piclstn.on[gid]}]正在打分，请耐心等待~")
    if not flmt.check(uid):
        await bot.send(ev, f'冰祈正在重新领取打分板，休息一下再来吧~({round(flmt.left_time(uid))}s)')
        return
    for raw_dict in message:
        if raw_dict['type'] == 'image':
            image_check += 1
            imageUrl = raw_dict['data']['url']
    if image_check > 1:
        piclstn.turn_off(gid)
        flmt.start_cd(ev.user_id)
        await bot.finish(ev, '一次只能给一张图片打分喔')
    elif image_check == 1:
        await bot.send(ev, '冰祈打分中，请稍候...')
        try:
            result = json.loads(AccessQualityPost(imageUrl))
        except Exception:
            piclstn.turn_off(gid)
            flmt.start_cd(uid)
            await bot.send(ev, f'不支持这种类型喔...')
            return
        clarityScore = result['ClarityScore']
        aestheticScore = result['AestheticScore']
        flmt.start_cd(uid)
        try:
            await bot.send_group_msg(group_id = gid,
                                     message = f'[CQ:reply,id={msgId}]清晰度评分:{clarityScore}\n美学评分:{aestheticScore}')
        except ActionFailed:
            await bot.send(ev, f'{MessageSegment.at(uid)}\n清晰度评分:{clarityScore}\n美学评分:{aestheticScore}')
    elif image_check == 0:
        await bot.send(ev, '了解，请发送需要评分的图片~')
        piclstn.turn_on(gid, uid)
        await sleep(SEARCH_TIMEOUT)
        if piclstn.get_on_off_status(gid):
            if datetime.now() < piclstn.timeout[gid]:
                piclstn.turn_off(gid)
                await bot.finish(ev, "好像没有发送任何图片，冰祈稍微休息一下，想要再次打分请输入'美学评分'~")


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
            flmt.start_cd(ev.user_id)
            piclstn.turn_off(ev.group_id)
            await bot.finish(ev, '一次只能给一张图片打分喔')
        elif image_check == 1:
            await bot.send(ev, '冰祈打分中，请稍候...')
            try:
                result = json.loads(AccessQualityPost(imageUrl))
            except Exception:
                flmt.start_cd(ev.user_id)
                piclstn.turn_off(ev.group_id)
                await bot.send(ev, f'不支持这种类型喔...')
                return
            clarityScore = result['ClarityScore']
            aestheticScore = result['AestheticScore']
            piclstn.turn_off(ev.group_id)
            flmt.start_cd(ev.user_id)
            try:
                await bot.send_group_msg(group_id = ev.group_id,
                                         message = f'[CQ:reply,id={msgId}]清晰度评分:{clarityScore}\n美学评分:{aestheticScore}')
            except ActionFailed:
                await bot.send(ev, f'{MessageSegment.at(ev.user_id)}\n清晰度评分:{clarityScore}\n美学评分:{aestheticScore}')
