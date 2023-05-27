import json
import os


def loadData(fp, is_list = False):
    """
        加载json，不存在则创建
    """
    if os.path.exists(fp):
        file = json.load(open(fp, 'r', encoding='utf-8'))
        return file
    else:
        if not is_list:
            empty_dict = {}
            with open(fp, 'w', encoding='utf-8') as file:
                json.dump(empty_dict, file, ensure_ascii=False)
            return empty_dict
        else:
            empty_list = []
            with open(fp, 'w', encoding='utf-8') as file:
                json.dump(empty_list, file, ensure_ascii=False)
            return empty_list


def saveData(obj, fp):
    """
    保存数据

    :param obj: 将要保存的数据
    :param fp: 文件路径
    """
    with open(fp, 'w', encoding="utf-8") as file:
        file.truncate(0)
        json.dump(obj, file, ensure_ascii=False)
