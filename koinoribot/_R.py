import io
import os
from urllib.parse import urljoin
from urllib.request import pathname2url
import base64

import aiohttp
from PIL import Image
from aiocqhttp import MessageSegment
from hoshino import util
try:
    from .build_image import BuildImage
except:
    from build_image import BuildImage

import hoshino

res_dir = os.path.join(os.path.dirname(__file__), 'src/')
imgPath = os.path.join(res_dir, 'img')  # 图片数据
userPath = os.path.join(res_dir, 'database')  # 用户数据

class ResObjKoi:
    def __init__(self, res_path):
        fullpath = os.path.abspath(os.path.join(res_dir, res_path))
        if not fullpath.startswith(os.path.abspath(res_dir)):
            raise ValueError('Cannot access outside RESOUCE_DIR')
        self.__path = os.path.normpath(res_path)

    @property
    def url(self):
        """资源文件的url，供酷Q（或其他远程服务）使用"""
        return urljoin(hoshino.config.RES_URL, pathname2url(self.__path))

    @property
    def path(self):
        """资源文件的路径，供bot内部使用"""
        return os.path.join(res_dir, self.__path)

    @property
    def exist(self):
        return os.path.exists(self.path)


class ResImg(ResObjKoi):
    @property
    def cqcode(self) -> MessageSegment:
        if hoshino.config.RES_PROTOCOL == 'http':
            return MessageSegment.image(self.url)
        elif hoshino.config.RES_PROTOCOL == 'file':
            return MessageSegment.image(f'base64://{pic2b64(os.path.abspath(self.path))}')
        else:
            try:
                return MessageSegment.image(util.pic2b64(self.open()))
            except Exception as e:
                hoshino.logger.exception(e)
                return MessageSegment.text('[图片出错]')

    def open(self) -> Image:
        try:
            return Image.open(self.path)
        except FileNotFoundError:
            hoshino.logger.error(f'缺少图片资源：{self.path}')
            raise


def get(path, *paths):  # 获取图片
    return ResImg(os.path.join('img', path, *paths))


def check_path_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)


def pic2b64(path):
    decoded = base64.b64encode(open(path, 'rb').read()).decode()
    return decoded


async def get_user_icon(uid) -> BuildImage:  # 最好使用utils里的
    imageUrl = f'https://q1.qlogo.cn/g?b=qq&nk={uid}&src_uin=www.jlwz.cn&s=0'
    async with aiohttp.ClientSession() as session:
        async with session.get(imageUrl) as r:
            content = await r.read()
    iconFile = io.BytesIO(content)
    icon = BuildImage(0, 0, background = iconFile)
    return icon


