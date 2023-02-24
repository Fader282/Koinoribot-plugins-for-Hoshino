# 冰祈插件相关配置文件


# 腾讯api
# 密钥可前往https://console.cloud.tencent.com/cam/capi/网站进行获取
TXSecretId = ''
TXSecretKey = ''

# 天行api，
# 密钥可前往https://www.tianapi.com/获取
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

# 今天吃什么
foods_whitelist = []  # 可以添加菜谱的群聊，为空则所有人都能添加

# 网络代理
proxies = {
    'http': 'http://127.0.0.1:7890',
}




# 钓鱼
ADMIN_GROUP = 0  # 漂流瓶审核群(必须有一个)
COOL_TIME = 600  # 钓鱼冷却时长
BAIT_PRICE = 10  # 鱼饵的价格
FRAG_TO_CRYSTAL = 100  # 碎片转化为水之心的数量
CRYSTAL_TO_BOTTLE = 3  # 水之心转化为漂流瓶的数量
FISH_PRICE = {'🍙': 10, '🐟': 5, '🦐': 10, '🦀': 15, '🐡': 20, '🐠': 30, '🔮': 75}  # 鱼的价格
DEBUG_MODE = 0  # 调试模式
STATIC_FC = 200  # 调试模式时可以固定first_choose的值，如果为0则不固定
# (A, B, C, D) 0-A:没钓到鱼/ A-B:随机事件/ B-C:钓到鱼/ C-D:钓到金币/ D-1000:钓到漂流瓶
PROBABILITY = [(150, 230, 780, 880), (0, 80, 780, 880), (100, 200, 650, 750)]
# 海之眷顾 五种鱼的上钩概率
PROBABILITY_2 = [(300, 550, 750, 900), (300, 550, 750, 900), (100, 250, 450, 700)]