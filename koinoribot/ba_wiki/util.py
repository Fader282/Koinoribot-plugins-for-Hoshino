import os

import requests
import ujson

proxies = {'http': 'http://127.0.0.1:7890'}

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Origin': 'https://www.ltool.net',
        'Referer': 'https://www.ltool.net/chinese-simplified-and-traditional-characters-pinyin-to-katakana-converter-in-simplified-chinese.php',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }


def get_json_data(url):
    """
    从url获取json文本
    """
    for i in range(3):
        try:
            res = requests.get(url, headers=headers, proxies=proxies)
            if res.status_code == 200:
                return res.json()
        except Exception as e:
            print(f'第{i+1}次下载数据失败：{e}')
            continue
    return None


def get_item(_dict, key, value):
    """
    根据键获取特定对象信息

    :param _dict: 需要检索的字典
    :param key: 需要检索的键
    :param value: 需要匹配的键
    """
    for item in _dict:
        if item[key] == value:
            return item


def space_amount(str_, extra = 0):
    """
    为了对齐描述文本
    """
    string = str(str_)
    length = len(string) if '←' not in string and '→' not in string else len(string) + 0.75
    space = ''
    for i in range(int(39 - 2.4 * length) + extra):
        space += ' '
    return space


def saveData(obj, fp):
    """
        保存文件
    """
    with open(fp, 'w', encoding='utf-8') as file:
        ujson.dump(obj, file, ensure_ascii=False)


def loadData(fp):
    """
        加载json，不存在则创建
    """
    if os.path.exists(fp):
        file = ujson.load(open(fp, 'r', encoding='utf-8'))
        return file
    else:
        empty_dict = {}
        with open(fp, 'w', encoding='utf-8') as file:
            ujson.dump(empty_dict, file, ensure_ascii=False)
        return empty_dict


if __name__ == '__main__':
    resp = get_json_data('https://lonqie.github.io/SchaleDB/data/cn/students.json')
    print(resp)