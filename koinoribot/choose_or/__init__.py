import random
from hoshino import Service, priv

sv_help = '''
遇事不决问问冰祈吧~
！rd A还是B还是C
'''.strip()

sv = Service(
    name='A还是B',  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.ADMIN,  # 管理权限
    visible=True,  # False隐藏
    enable_on_default=True,  # 是否默认启用
    bundle='通用',  # 属于哪一类
    help_=sv_help  # 帮助文本
)


@sv.on_prefix(('!rd', '！rd'))
async def hp_choose(bot, ev):
    message = ev.raw_message.extract_plain_text().strip()

    msg = message[0:].split('还是')  # 将消息分割
    if len(msg) == 1:
        return
    choices = list(filter(lambda x: len(x) != 0, msg))  # 过滤出为空的元素
    if not choices:
        await bot.send(ev, '选项不能全部为空哦', at_sender=True)
        return
    msgs = ['冰祈的选择: ']
    if random.randrange(1000) <= 100:
        msgs.append('“全都要”')
    else:
        final = random.choice(choices)  # 随机选出分割字符前后的字符串
        msgs.append(f'{final}')
    await bot.send(ev, '\n'.join(msgs), at_sender=True)
