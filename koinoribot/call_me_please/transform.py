import json
import os
import random

txt = '请不要匿名使用botuuuuu'
lenTxt = len(txt)
lenTxt_utf8 = len(txt.encode('utf-8'))
size = int((lenTxt_utf8 - lenTxt)/2 + lenTxt)
if size > 20:
    txt_split = ''
    for i in txt:
        txt_split += i
        lenTxt = len(txt_split)
        lenTxt_utf8 = len(txt_split.encode('utf-8'))
        txt_size = int((lenTxt_utf8 - lenTxt)/2 + lenTxt)
        if txt_size >= 20:
            break
else:
    txt_split = txt


sample_num = random.randint(5, 11)
name = ''.join(random.sample(txt, sample_num))


if __name__ == '__main__':
    print(name)
    '''print(size)
    print(txt.encode('utf-8'))
    print(lenTxt_utf8)
    print(txt_split)'''
    '''new_dict = {}
    with open(os.path.join(os.path.dirname(__file__), 'user.json'), 'r+', encoding='utf-8') as file:
        nickname_dict = json.load(file)
    for i, j in nickname_dict.items():
        new_dict[i] = {"switch": 1, "other": "", "self": j}
    with open(os.path.join(os.path.dirname(__file__), 'nickname.json'), 'w', encoding='utf-8') as file:
        json.dump(new_dict, file, ensure_ascii=False, indent=2)'''

