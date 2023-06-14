# 冰祈插件相关配置文件


# 好友、群聊管理
white_list_group = 123456  # 白名单群聊
group_auto_approve = False  # 是否自动同意进群(需进入白名单群）
friend_auto_approve = False   # 是否自动同意好友邀请（需进入白名单群）
star_cost_mode = False  # 是否需要消耗星星来获得bot好友


SEND_FORWARD = True  # 是否启用合并转发（应对风控）
PUBLIC_BOT = False  # 是否启用云bot模式（一般可忽略）


# 腾讯api
# 密钥可前往 https://console.cloud.tencent.com/cam/capi 网站进行获取
TXSecretId = ''
TXSecretKey = ''

# 天行api，使用范围：土味情话，彩虹屁，可前往 https://www.tianapi.com/ 获取
tianxing_apikey = ''

# 有道翻译api
youdao_appkey = ''
youdao_secret = ''

# 随机美图
AUTO_SAVE = True  # 是否保存到本地
AUTO_DELETE = False  # 是否撤回
DELETE_TIME = 30  # 撤回的等待时间

# arcaeaAPI
api_url = ''
token = ''

# danbooru
SAVE_MODE = False  # 是否保存到本地
DELETE_MODE = False  # 是否自动撤回

# 今天吃什么
foods_whitelist = []  # 可以添加菜谱的群聊，为空则所有人都能添加

# 网络代理
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https:': 'https://127.0.0.1:7890'
}

# openai api
OPEN_API = ''
OPEN_ORG = ''


# 钓鱼
ADMIN_GROUP = 123456  # 漂流瓶审核群(必须有一个)
COOL_TIME = 600  # 钓鱼冷却时长
THROW_COOL_TIME = 300  # 扔漂流瓶冷却时长
SALVAGE_COOL_TIME = 300  # 捡漂流瓶冷却时长
BAIT_PRICE = 10  # 鱼饵的价格
FRAG_TO_CRYSTAL = 75  # 碎片转化为水之心的数量
CRYSTAL_TO_BOTTLE = 2  # 水之心转化为漂流瓶的数量
CRYSTAL_TO_NET = 2  # 捞漂流瓶需要的水之心数量
FISH_PRICE = {'🍙': 10, '🐟': 5, '🦐': 10, '🦀': 15, '🐡': 20, '🐠': 30}  # 鱼的价格

# (A, B, C, D) 0-A:没钓到鱼/ A-B:随机事件/ B-C:钓到鱼/ C-D:钓到金币/ D-1000:钓到水之心
PROBABILITY = [(50, 150, 800, 850), (0, 80, 780, 880), (100, 200, 650, 750)]
# 海之眷顾 五种鱼的上钩概率
PROBABILITY_2 = [(250, 500, 700, 900), (300, 550, 750, 900), (100, 250, 450, 700)]

DEBUG_MODE = 0  # 调试模式
STATIC_FC = 200  # 调试模式时可以固定first_choose的值，如果为0则不固定
