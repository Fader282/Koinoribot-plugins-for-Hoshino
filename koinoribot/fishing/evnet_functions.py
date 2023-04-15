import random
from .get_fish import increase_value, getUserInfo, decrease_value
from .. import money


async def ev1_1(bot, ev, uid):
    choose = random.randint(1, 4)
    if choose == 4:
        await bot.send(ev, '美人鱼点了点头，将金饭团递给了你！(金币+80)', at_sender = True)
        money.increase_user_money(uid, 'gold', 100)
        return
    else:
        await bot.send(ev, '美人鱼发现了你的谎言，收走了你钱包里的金币！(金币-40)', at_sender = True)
        money.reduce_user_money(uid, 'gold', 50)
        return


async def ev1_2(bot, ev, uid):
    choose = random.randint(1, 3)
    if choose == 3:
        await bot.send(ev, '美人鱼点了点头，将银饭团递给了你！(金币+50)', at_sender = True)
        money.increase_user_money(uid, 'gold', 50)
        return
    else:
        await bot.send(ev, '美人鱼发现了你的谎言，收走了你钱包里的金币！(金币-30)', at_sender = True)
        money.reduce_user_money(uid, 'gold', 30)
        return


async def ev1_3(bot, ev, uid):
    await bot.send(ev, '美人鱼点了点头，将饭团递给了你。(鱼饵+2)', at_sender = True)
    increase_value(uid, 'fish', '🍙', 2)
    return


async def ev1_4(bot, ev, uid):
    choose = random.randint(1, 8)
    if choose == 8:
        await bot.send(ev, '你的诚实打动了美人鱼，她将所有的饭团都递给了你！(金币+150，🍙+2)', at_sender = True)
        money.increase_user_money(uid, 'gold', 150)
        increase_value(uid, 'fish', '🍙', 2)
        return
    else:
        if choose > 2:
            await bot.send(ev, '美人鱼表扬了你的诚实，将鱼饵饭团送给了你。(🍙+2)', at_sender = True)
            increase_value(uid, 'fish', '🍙', 2)
            return
        else:
            await bot.send(ev, '美人鱼点了点头，道谢后回到了水里。')
            return


async def ev2_1(bot, ev, uid):
    user_gold = money.get_user_money(uid, 'gold')
    if user_gold > 15:
        bait_num = random.randint(2, 3)
        money.reduce_user_money(uid, 'gold', 15)
        increase_value(uid, 'fish', '🍙', bait_num)
        await bot.send(ev, f'他显得很高兴，在自己的口袋里摸索了半天，"瞧瞧我今天为你准备了什么！给你啦！"(🍙+{bait_num})', at_sender = True)
        return
    else:
        money.increase_user_money(uid, 'gold', 15)
        await bot.send(ev, '你表示自己的手头也很紧，他苦笑了一下，"今天还是算了吧，那希望我的这点钱能帮你度过难关！"(金币+15)', at_sender = True)
        return


async def ev2_2(bot, ev, uid):
    user_lucky = money.get_user_money(uid, 'luckygold')
    if user_lucky > 2:
        crystal_num = random.randint(1, 3)
        money.reduce_user_money(uid, 'luckygold', 2)
        increase_value(uid, 'fish', '🔮', crystal_num)
        await bot.send(ev, f'他显得很高兴，在自己的口袋里摸索了半天，"瞧瞧我今天为你准备了什么！给你啦！"(🔮+{crystal_num})', at_sender = True)
        return
    else:
        money.increase_user_money(uid, 'gold', 15)
        await bot.send(ev, '你表示自己的手头也很紧，他苦笑了一下，"今天还是算了吧，那希望我的这点钱能帮你度过难关！"(金币+15)', at_sender = True)
        return


async def ev2_3(bot, ev, uid):
    choose = random.randint(1, 3)
    if choose == 1:
        await bot.send(ev, '“你推我做什么!!哎呀你这人!”他大喊大叫着走了。回到竿前，你发现鱼饵已经被鱼吃掉了。', at_sender = True)
        return
    else:
        fish = random.choice(['🐟', '🦐', '🦀', '🐡', '🐠'])
        increase_value(uid, 'fish', fish, 1)
        increase_value(uid, 'statis', 'total_fish', 1)
        await bot.send(ev, f'“你推我做什么!!哎呀你这人!”他大喊大叫着走了。回到竿前，你发现一条鱼正在咬钩。({fish}+1)', at_sender = True)
        return


async def ev3_1(bot, ev, uid):
    fish_num = random.randint(2, 5)
    increase_value(uid, 'fish', '🐟', fish_num)
    increase_value(uid, 'statis', 'total_fish', fish_num)
    await bot.send(ev, f'你屏息凝神，发现鱼比往常更加活跃，趁着大雨连续钓到了{fish_num}条鱼！(🐟+{fish_num})', at_sender = True)
    return


async def ev3_2(bot, ev, uid):
    gold_num = random.randint(5, 25)
    money.increase_user_money(uid, 'gold', gold_num)
    await bot.send(ev, f'你找到了一处废弃的小屋躲雨，在屋内休息时发现地上散落着一些钱币。(金币+{gold_num})', at_sender = True)
    return


async def ev4_1(bot, ev, uid):
    choose = random.randint(1, 4)
    if choose == 1:
        await bot.send(ev, '文字散发出白色的光芒，水里的鱼儿开始躁动不安，纷纷往岸边游去。你收获颇丰。(🐟🦐🦀🐡🐠各+1)', at_sender = True)
        for i in ['🐟', '🦐', '🦀', '🐡', '🐠']:
            increase_value(uid, 'fish', i, 1)
        increase_value(uid, 'statis', 'total_fish', 5)
        return
    elif choose == 2:
        gold_num = random.randint(10, 25)
        money.increase_user_money(uid, 'gold', gold_num)
        await bot.send(ev, f'文字散发出红色的光芒，书本随即变成了一堆金币。(金币+{gold_num})', at_sender = True)
        return
    elif choose == 3:
        money.increase_user_money(uid, 'luckygold', 3)
        await bot.send(ev, f'文字散发出蓝色的光芒，你感觉你的幸运提升了。果然不久之后，你钓上了装有幸运币的布包。(幸运币+3)', at_sender = True)
        return
    else:
        gold_num = random.randint(1, 10)
        money.reduce_user_money(uid, 'gold', gold_num)
        await bot.send(ev, f'文字散发出黑色的光芒，你感觉书本正在你的身上寻找着什么。(金币-{gold_num})', at_sender = True)
        return


async def ev4_2(bot, ev, uid):
    choose = random.randint(1, 2)
    if choose == 1:
        increase_value(uid, 'fish', '🔮', 1)
        await bot.send(ev, '你默默阅读着文字。书中的魔力引导着你的思绪，使你仿佛徜徉于海底。回过神来，发现手中已没有了书，而是握着一颗水之心。(水之心+1)', at_sender = True)
        return
    else:
        await bot.send(ev, '你默默阅读着文字。书中的魔力引导着你的思绪，使你仿佛翱翔于天际。回过神来，发现自己正躺在地上，那本书也没有了踪迹。(🍙+1)', at_sender = True)
        increase_value(uid, 'fish', '🍙', 1)
        return


async def ev4_3(bot, ev, uid):
    fish = random.choice(['🐟', '🦐', '🦀'])
    increase_value(uid, 'fish', fish, 1)
    increase_value(uid, 'statis', 'total_fish', 1)
    await bot.send(ev, f'你感觉到书本散发的能量超出了自己的认知，还是尽快脱手为好。不久后你钓上了一条{fish}。', at_sender = True)
    return


async def ev5_1(bot, ev, uid):
    msg = '你将一枚金币放入投币口，拉下拉杆，一阵响动后，'
    money.reduce_user_money(uid, 'gold', 1)
    choose = random.randint(1, 4)
    if choose == 1:
        gold_num = random.randint(5, 15)
        money.increase_user_money(uid, 'gold', gold_num)
        await bot.send(ev, msg + f'从出货口里掉出了一些金币。(金币+{gold_num})', at_sender = True)
        return
    elif choose == 2:
        money.increase_user_money(uid, 'luckygold', 1)
        await bot.send(ev, msg + f'从出货口里掉出了一枚幸运币。(幸运币+1)', at_sender = True)
        return
    elif choose == 3:
        bait_num = random.randint(2, 3)
        increase_value(uid, 'fish', '🍙', bait_num)
        await bot.send(ev, msg + f'出货口掉出了一袋鱼饵。(鱼饵+{bait_num})', at_sender = True)
        return
    else:
        fish = random.choice(['🦐', '🦀', '🐡', '🐠'])
        increase_value(uid, 'fish', fish, 1)
        increase_value(uid, 'statis', 'total_fish', 1)
        await bot.send(ev, msg + f'什么事也没有发生。你感觉受到了欺骗，丢掉老虎机后继续钓起了鱼。({fish}+1)', at_sender = True)
        return


async def ev5_2(bot, ev, uid):
    msg = '你将一枚幸运币放入投币口，拉下拉杆，一阵响动后，'
    money.reduce_user_money(uid, 'luckygold', 1)
    increase_value(uid, 'fish', '🔮', 1)
    await bot.send(ev, msg + '老虎机渐渐被柔和的光包围，与此同时其形状也开始发生变化，最终化为了一颗水之心，静静地躺在你的手里。(🔮+1)', at_sender = True)
    return


async def ev5_3(bot, ev, uid):
    choose = random.randint(1, 2)
    if choose == 1:
        fish = random.choice(['🦐', '🦀', '🐡', '🐠'])
        increase_value(uid, 'fish', fish, 1)
        increase_value(uid, 'statis', 'total_fish', 1)
        await bot.send(ev, f'你感觉这个在水里泡过的老虎机并不会正常工作，于是将它丢回了水里并继续钓起了鱼。({fish}+1)')
        return
    else:
        money.increase_user_money(uid, 'gold', 15)
        await bot.send(ev, f'你感觉这个在水里泡过的老虎机并不会正常工作，但其本身应该还能换点钱。你回去后将它卖了出去。(金币+15)')
        return


async def ev5_4(bot, ev, uid):
    money.increase_user_money(uid, 'luckygold', 1)
    await bot.send(ev, '出于好奇，你将老虎机拆开，发现里面有一枚幸运币，是其他人投进去的吧？(幸运币+1）')
    return


async def ev6_1(bot, ev, uid):
    choose = random.randint(1, 2)
    if choose == 1:
        fishes = []
        for i in range(3):
            fish = random.choice(['🐟', '🦐', '🦀', '🐡', '🐠'])
            fishes.append(fish)
            increase_value(uid, 'fish', fish, 1)
        increase_value(uid, 'statis', 'total_fish', 3)
        await bot.send(ev, f'喝下水后，你感觉自己的感官变得十分敏锐，短时间内连续钓上了三条鱼。(获得{fishes[0]}{fishes[1]}{fishes[2]})')
        return
    else:
        await bot.send(ev, f'喝下水后，你感觉自己的感官变得迟钝起来，很长时间里都让咬钩的鱼跑掉了。')
        return


async def ev6_2(bot, ev, uid):
    fish = random.choice(['🐟', '🦐', '🦀', '🐡', '🐠'])
    increase_value(uid, 'fish', fish, 1)
    increase_value(uid, 'statis', 'total_fish', 1)
    await bot.send(ev, f'你感觉这个水并不卫生，倒了一些出来研究了一番，无果后将水瓶扔回了水里，随后继续钓起了鱼。({fish}+1)')
    return


async def ev7_1(bot, ev, uid):
    user_info = getUserInfo(uid)
    fish = random.choice(['🐟', '🦐', '🦀', '🐡', '🐠'])
    increase_value(uid, 'statis', 'total_fish', 1)
    increase_value(uid, 'fish', '🔮', 1)
    await bot.send(ev, f'你将正好钓上来的{fish}分给了猫咪，它竖着尾巴快速跑开了。正要回去时你看到刚才的猫咪叼着一颗水之心，似乎想要将它送给你。(🔮+1)')
    return


async def ev7_2(bot, ev, uid):
    user_info = getUserInfo(uid)
    if not user_info['fish']['🍙']:
        fish = random.choice(['🐟', '🦐'])
        increase_value(uid, 'fish', fish, 1)
        await bot.send(ev, f'你发现包里已经没有了饭团，只好摸了摸猫咪的头，猫咪恋恋不舍地离开了。你继续钓起了鱼。({fish}+1)')
        return
    decrease_value(uid, 'fish', '🍙', 1)
    money.increase_user_money(uid, 'luckygold', 1)
    await bot.send(ev, '你将一颗饭团分给了猫咪，它竖着尾巴快速跑开了。正要回去时你看到刚才的猫咪叼着一枚幸运币，似乎想要将它送给你。(幸运币+1)')
    return


async def ev7_3(bot, ev, uid):
    fish = random.choice(['🐟', '🦐', '🦀', '🐡', '🐠'])
    increase_value(uid, 'fish', fish, 1)
    await bot.send(ev, f'你摸了摸猫咪的头，并继续钓起了鱼，猫咪逗留了一会后离开了。({fish}+1)')
    return


random_event = {
    "随机事件1": {'msg':
        '在钓鱼时，你发现河中出现了一个漩涡，一条美人鱼从中浮起，手中拿着三个饭团:金饭团、银饭团和鱼饵饭团，询问你是否有弄丢过饭团.\n',
        'choice': ['1.选择金饭团.', '2.选择银饭团.', '3.选择鱼饵饭团.', '4.向美人鱼说明自己没有弄丢过饭团.'],
        'result': [ev1_1, ev1_2, ev1_3, ev1_4]},
    "随机事件2": {'msg':
        "“好久不见！原来你在这里钓鱼！”一个男子欢快地从你身边经过，你不认识这个男人。\n“所以今天有什么好东西给我吗？还是说和往常一样？”\n他停在了你的身边，你满腹狐疑地打量着他，开始思考应该怎么做……\n",
        'choice': ['1.给予15金币.', '2.给予2幸运币', '3.赶走他'],
        'result': [ev2_1, ev2_2, ev2_3]},
    "随机事件3": {'msg':
        "在钓鱼的时候，天渐渐暗了下来，感觉有零星的雨点落下，快要下雨了。\n",
        'choice': ['1.继续钓鱼', '2.暂时躲雨'],
        'result': [ev3_1, ev3_2]},
    "随机事件4": {'msg':
        '你钓上来了一本书。看起来已经在水里浸泡了很久。\n书内的文字依稀可辨，似乎是某种神秘的咒语。\n',
        'choice': ['1.大声朗读', '2.默默阅读', '3.扔回水里'],
        'result': [ev4_1, ev4_2, ev4_3]},
    "随机事件5": {'msg':
        '你钓到了一台袖珍老虎机，两只手刚好能拿住，摇起来有叮当的响声，看上去是刚被丢弃不久的。摆弄途中你找到了它的投币口，似乎往里投入硬币就能使用。\n',
        'choice': ['1.投入一枚金币', '2.投入一枚幸运币', '3.扔回水里', '4.砸开看看'],
        'result': [ev5_1, ev5_2, ev5_3, ev5_4]},
    "随机事件6": {'msg':
        '你钓上了一个密封的玻璃瓶，奇怪的是，里面装满了闪着光的水。\n',
        'choice': ['1.尝试喝一口', '2.扔掉可疑的水'],
        'result': [ev6_1, ev6_2]},
    "随机事件7": {'msg':
        '钓鱼时，一只可爱的小猫咪从你的身后窜出，并在你的周围寻找些什么。当它靠近你装鱼的背包时，表现出了明显的兴奋，看来是饿了。\n',
        'choice': ['1.喂一条鱼', '2.喂一份饭团', '3.不理睬'],
        'result': [ev7_1, ev7_2, ev7_3]},
}

'''    
    "随机事件8": {'msg':
        '一名上身赤裸男人跑到了你的身边。\n"你能给我点儿什么吗，求求你了...我只是需要找个地方过夜，我身上有财宝可以交换..."他的手上握着一颗水之心。虽然看起来疯疯癫癫的，但并没有危险。\n',
        'choice': ['1.给予100金币', '2.夺走他的财宝', '3.不帮助他'],
        'result': [ev8_1, ev8_2, ev8_3]},
    "随机事件9": {'msg':
        '你钓到了一块甲骨，发现上面写满了古老的文字。你尝试推理这些奇怪的符号和图案可能的意思，却发现文字开始发起了光。突然之间，文字的意义变得清晰了...原来是关于真理的选择。\n',
        'choice': ['1.简约', '2.质朴'],
        'result': [ev9_1, ev9_2, ev9_3]},'''
