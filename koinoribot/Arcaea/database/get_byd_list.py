import os

import ujson

file = ujson.load(open(os.path.join(os.path.dirname(__file__), 'database/rating_dict.json'), 'r', encoding='utf-8'))

byd_list = []

for i, j in file.items():
    if len(j) == 4:
        byd_list.append(i)

with open(os.path.join(os.path.dirname(__file__), 'database/byd_list.json'), 'w', encoding='utf-8') as f:
    ujson.dump(byd_list, f, ensure_ascii=False)