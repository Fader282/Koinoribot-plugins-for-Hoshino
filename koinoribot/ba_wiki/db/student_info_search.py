import json
import os

with open(os.path.join(os.path.dirname(__file__),'students.json'), 'r', encoding='utf-8') as f:
    students_info = json.load(f)
with open(os.path.join(os.path.dirname(__file__),'favor.json'), 'r', encoding='utf-8') as f:
    items_info = json.load(f)


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


base_info = get_item(students_info, "Id", 10038)

FavorItemUniqe_list = []
FavorItem_list = []
WeaponType_list = []

for tags in base_info['FavorItemUniqueTags']:
    for item in items_info:
        if tags in item['Tags'] and item['Icon'] not in FavorItemUniqe_list:
            FavorItemUniqe_list.append(item['Icon'])

for tags in base_info['FavorItemTags']:
    for item in items_info:
        if tags in item['Tags'] and item['Icon'] not in FavorItemUniqe_list and item['Icon'] not in FavorItem_list:
            FavorItem_list.append(item['Icon'])

print(f'喜爱的礼物：{FavorItemUniqe_list}，喜欢的礼物：{FavorItem_list}')


'''for i in students_info:
    if i['WeaponType'] not in WeaponType_list:
        WeaponType_list.append(i['WeaponType'])

print(WeaponType_list)'''


'''FavorStatType_list = []
for i in students_info:
    for j in i['FavorStatType']:
        if j not in FavorStatType_list:
            FavorStatType_list.append(j)

print(FavorStatType_list)'''


#if __name__ == '__main__':
