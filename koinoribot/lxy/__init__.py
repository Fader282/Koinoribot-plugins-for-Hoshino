import random
from hoshino import Service,priv

sv_help = '''
遇事不决问问冰祈吧~
'''.strip()

sv = Service(
    name = '遇事不决',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #False隐藏
    enable_on_default = True, #是否默认启用
    bundle = '通用', #属于哪一类
    help_ = sv_help #帮助文本
    )

@sv.on_fullmatch(["帮助遇事不决"])
async def bangzhu(bot, ev):
    await bot.send(ev, sv_help, at_sender=True)


@sv.on_prefix(('!or', '！or'))
async def hp_choose(bot, ev):
    message = ev.message.extract_plain_text().strip()
    message = message.replace('能否','能不能').replace('是否','是不是')
    msg = message[0:].split('不',1)
    msg1 = msg[0]
    msg2 = msg[-1]
    yes_or_no = ''
    if random.randrange(100)<=50:
        yes_or_no = '不'
    msgs = ['冰祈的选择：']
    if msg1[-1] == msg2[0]:  # A不A型
        final = str(msg1[:-1] + yes_or_no + msg2)
        msgs.append(final)
        await bot.send(ev,'\n'.join(msgs),at_sender=True)
    elif msg1[-2:] == msg2[:2]: # AB不AB型
        final = str(msg1[:-2] + yes_or_no + msg2)
        msgs.append(final)
        await bot.send(ev,'\n'.join(msgs),at_sender=True)
    else:
        await bot.send(ev,'给冰祈整不会了QAQ',at_sender=False)


'''
@sv.on_prefix(('###','###'))
async def ly_choose(bot, ev):
    message = ev.message.extract_plain_text().strip()

    msg = message[0:].split('要不要' or '是否要')
    if len(msg) == 1:
        return
    choices=list(filter(lambda x:len(x)!=0,msg))
    if not choices:
        await bot.send(ev,'给我整不会了...',at_sender=True)
        return 
    msgs=['建议选择: ']
    if random.randrange(1000)<=500:
        final=random.choice(choices)
        msgs.append(f'{final}')
        await bot.send(ev,'要'.join(msgs),at_sender=True)
    else:
        final=random.choice(choices)
        msgs.append(f'{final}')
        await bot.send(ev,'不要'.join(msgs),at_sender=True)
'''