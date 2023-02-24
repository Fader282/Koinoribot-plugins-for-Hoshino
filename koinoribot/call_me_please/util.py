import os
import ujson

path = os.path.join(os.path.dirname(__file__), "../src/database/call_me_please/nickname.json")


def load_data(fp):
    _dict = ujson.load(open(fp, 'r+', encoding='utf-8'))
    return _dict


def save_data(obj, fp):
    with open(fp, 'r+', encoding='utf-8') as file:
        file.truncate(0)
        ujson.dump(obj, file, ensure_ascii=False, indent=2)


def check_user(uid: str, _dict: dict):
    if uid not in _dict.keys():
        _dict[uid] = {"switch": 1, "other": '', "self": ''}
    return _dict
