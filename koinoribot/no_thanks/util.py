from ..build_image import BuildImage


def text2CQimg(text: str):
    """
        文字转图片，并转成CQ码
    """
    img = BuildImage(0, 0, multiline_text=text, font_size=20)
    cqimg = f"[CQ:image,file=base64://{img.pic2bs4()}]"
    return cqimg


async def get_user_name(bot, user_id):
    """
        获取用户名称
    """
    stranger_info = await bot.get_stranger_info(user_id=user_id, no_cache=True)
    nickname = stranger_info['nickname']
    return nickname


def get_score(usercard: list):
    """
        计算得分，返回有效点数列表与最终得分
    """
    vaild = []
    for i in usercard:
        if (i - 1) not in usercard:
            vaild.append(i)
    return vaild, sum(vaild)
