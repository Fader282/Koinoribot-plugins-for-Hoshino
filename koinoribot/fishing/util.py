import random

from importlib import reload

import time
from . import serif


def update_serif():
    reload(serif)


def set_serif(_serif):
    """
    随机选择语录
    """
    return random.choice(_serif)


def shift_time_style(timestamp):
    timeArray = time.localtime(timestamp)
    otherStyleTime = time.strftime("%m月%d日%H时%M分", timeArray)
    return otherStyleTime