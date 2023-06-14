import hoshino, random, os, re, filetype
from hoshino import Service, priv, aiorequests
from hoshino.typing import CQEvent
from hoshino.util import DailyNumberLimiter
import ujson
from .._R import imgPath, pic2b64
from ..config import foods_whitelist


sv_help = '''
[今天吃什么] 看看今天吃啥
'''.strip()

sv = Service(
    name='今天吃什么',  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.ADMIN,  # 管理权限
    visible=True,  # 可见性
    enable_on_default=True,  # 默认启用
    bundle='娱乐',  # 分组归类
    help_=sv_help  # 帮助说明
)

_lmt = DailyNumberLimiter(5)
foodsPath = os.path.join(imgPath, 'whattoeat/foods')



async def download_async(url: str, name: str):
    resp = await aiorequests.get(url, stream=True)
    if resp.status_code == 404:
        raise ValueError('文件不存在')
    content = await resp.content
    try:
        extension = filetype.guess_mime(content).split('/')[1]
    except:
        raise ValueError('不是有效文件类型')
    abs_path = os.path.join(foodsPath, f'{name}.{extension}')
    with open(abs_path, 'wb') as f:
        f.write(content)


@sv.on_rex(r'(今|今天|今儿)?(早|早上|早餐|早饭)(吃|恰)(甚|甚么|什么|啥|点啥)(.+)?')
async def random_breakfast(bot, ev: CQEvent):
    uid = ev.user_id
    if not _lmt.check(uid):
        await bot.finish(ev, '你今天吃的已经够多的了！', at_sender=True)
    with open(os.path.join(foodsPath, 'config.json'), 'r+', encoding = 'utf-8') as f:
        user_config = ujson.load(f)
    if str(uid) in user_config.keys():
        user_mode = int(user_config[str(uid)])
    else:
        user_mode = 0
    if user_mode == 1:
        food = random.choice(os.listdir(os.path.join(foodsPath, 'extra')))
    elif user_mode == 2:
        food = random.choice(os.listdir(os.path.join(foodsPath, 'upload')))
    else:
        food = random.choice(os.listdir(os.path.join(foodsPath, 'breakfast')))
    name = food.split('.')
    to_eat_text = f'早上去吃{name[0]}吧~'
    await bot.send(ev, to_eat_text, at_sender=True)
    try:
        if user_mode == 1:
            foodimg = os.path.join(foodsPath, f'extra/{food}')
        elif user_mode == 2:
            foodimg = os.path.join(foodsPath, f'upload/{food}')
        else:
            foodimg = os.path.join(foodsPath, f'breakfast/{food}')
        imgToSend = f'[CQ:image,file=base64://{pic2b64(foodimg)}]'
        to_eat_image = str(imgToSend)
        await bot.send(ev, to_eat_image)
    except Exception as e:
        hoshino.logger.error(f'读取食物图片时发生错误{type(e)}')
    with open(os.path.join(foodsPath, 'config.json'), 'r+', encoding = 'utf-8') as f:
        f.truncate(0)
        ujson.dump(user_config, f, ensure_ascii = False, indent = 2)
    _lmt.increase(uid)


@sv.on_rex(r'^(.+)?(今天|[中午晚][饭餐午上]|夜宵|今晚)(吃|恰)(甚|甚么|什么|啥|点啥)(.+)?')
async def net_ease_cloud_word(bot, ev: CQEvent):
    uid = ev.user_id
    if not _lmt.check(uid):
        await bot.finish(ev, '你今天吃的已经够多的了！', at_sender=True)
    match = ev['match']
    time = match.group(2).strip()
    with open(os.path.join(foodsPath, 'config.json'), 'r+', encoding = 'utf-8') as f:
        user_config = ujson.load(f)
    if str(uid) in user_config.keys():
        user_mode = int(user_config[str(uid)])
    else:
        user_mode = 0
    if user_mode == 1:
        food = random.choice(os.listdir(os.path.join(foodsPath, 'extra')))
    elif user_mode == 2:
        food = random.choice(os.listdir(os.path.join(foodsPath, 'upload')))
    else:
        food = random.choice(os.listdir(os.path.join(foodsPath, 'dinner')))
    name = food.split('.')
    to_eat_text = f'{time}去吃{name[0]}吧~'
    await bot.send(ev, to_eat_text, at_sender=True)
    try:
        if user_mode == 1:
            foodimg = os.path.join(foodsPath, f'extra/{food}')
        elif user_mode == 2:
            foodimg = os.path.join(foodsPath, f'upload/{food}')
        else:
            foodimg = os.path.join(foodsPath, f'dinner/{food}')
        imgToSend = f'[CQ:image,file=base64://{pic2b64(foodimg)}]'
        to_eat_image = str(imgToSend)
        await bot.send(ev, to_eat_image)
    except Exception as e:
        hoshino.logger.error(f'读取食物图片时发生错误{type(e)}')

    _lmt.increase(uid)


@sv.on_prefix(('添菜', '添加菜品'))
@sv.on_suffix(('添菜', '添加菜品'))
async def add_food(bot, ev: CQEvent):
#    if not priv.check_priv(ev, priv.SUPERUSER):
#        return
    if len(foods_whitelist):
        if ev.group_id not in foods_whitelist:
            return
    food = ev.message.extract_plain_text().strip()
    ret = re.search(r"\[CQ:image,file=(.*)?,url=(.*)\]", str(ev.message))
    if not ret:
        await bot.send(ev, '请附带美食图片~')
        return
    url = ret.group(2)
    try:
        await download_async(url, food)
    except:
        hoshino.logger.error('有人加菜不写名字？')
        return
    await bot.send(ev, '食谱已增加~')


@sv.on_prefix('换菜单')
@sv.on_suffix('换菜单')
async def change_menu(bot, ev: CQEvent):
    uid = str(ev.user_id)
    with open(os.path.join(foodsPath, 'config.json'), 'r+', encoding = 'utf-8') as f:
        user_config = ujson.load(f)
    if uid not in user_config.keys():
        user_config[uid] = 0

    ret = re.search(r"(正常模式|来点硬菜|用户模式)", str(ev.message))
    if not ret:
        return
    command = ret.group(1)
    if command == '正常模式':
        if int(user_config[uid]) == 0:
            await bot.send(ev, '已经是正常菜式了哦')
            return
        elif int(user_config[uid]) == 1:
            user_config[uid] = 0
            yami = f"[CQ:image,file=base64://{pic2b64(os.path.join(foodsPath, 'yami.png'))}]"
            await bot.send(ev, f'切换成功，果然还是正常的好吃呢~{yami}')
        else:
            user_config[uid] = 0
            await bot.send(ev, '已经换回正常菜式了~')
    elif command == '来点硬菜':
        if int(user_config[uid]) != 1:
            user_config[uid] = 1
            kowai = f"[CQ:image,file=base64://{pic2b64(os.path.join(foodsPath, 'kowai.png'))}]"
            await bot.send(ev, f'切...切换成功...{kowai}')
        else:
            jii = f"[CQ:image,file=base64://{pic2b64(os.path.join(foodsPath, 'jii.png'))}]"
            await bot.send(ev, f'您已经站在了食物链的顶端！{jii}')
            return
    elif command == '用户模式':
        if int(user_config[uid]) != 2:
            user_config[uid] = 2
            message = '已经切换到用户自定义模式了~'
            if (not len(foods_whitelist)) or (ev.group_id in foods_whitelist):
                message += '使用"添菜"添加菜肴~'
            await bot.send(ev, message)
        else:
            await bot.send(ev, '已经在自定义模式里了~')
            return
    with open(os.path.join(foodsPath, 'config.json'), 'r+', encoding = 'utf-8') as f:
        f.truncate(0)
        ujson.dump(user_config, f, ensure_ascii = False, indent = 2)

