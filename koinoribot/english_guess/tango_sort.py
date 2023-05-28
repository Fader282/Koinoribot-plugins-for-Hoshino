import json
import re

from util import loadData, saveData
import os


dict_path = os.path.join(os.path.dirname(__file__), 'data/japanese')


'''def kana_yomi_splt(word: str):
    """
        将假名与读音分开
    """
    rematch = re.findall(r'([\u30a1-\u30f6\u3041-\u3093\uFF00-\uFFFF\u4e00-\u9fa5]+)([⓪①②③④⑤⑥⑦⑧⑨⑩]+(或[⓪①②③④⑤⑥⑦⑧⑨⑩]+)?)?', word)
    kana = rematch[0][0]
    yomi = rematch[0][1]
    return kana, yomi


def find_kana(word: str):
    rematch = re.findall(r'([\u3040-\u3098\u30a1-\u30fa\u30fc]+)', word)'''



'''def get_list(input_file, output_file):
    _list = []
    _dict = loadData(os.path.join(dict_path, input_file))
    for i in _dict:
        if '/' in i['kana']:
            kana = i['kana'].split('/')
        else:
            kana  = [i['kana']]
        jpword = i['jpword']
        if 'mean' in i.keys():
            mean = i['mean']
        else:
            mean = ''
            print(f'{kana}没有中文释义')
        if 'sample' in i.keys():
            sample = i['sample']
        else:
            sample = ''
            print(f'{kana}没有例句')
        tango = {
            'jpword': jpword,
            'kana': kana,
            'mean': mean,
            'sample': sample
        }
        _list.append(tango)
    saveData(_list, os.path.join(dict_path, output_file))'''


'''def get_check_list():
    _list = []
    _dict = loadData(os.path.join(dict_path, 'all_list_jp.json'))
    for i in _dict:
        for j in i['kana']:
            kana, yomi = kana_yomi_splt(j)
            if kana not in _list:
                _list.append(kana)
    saveData(_list, os.path.join(dict_path, 'check_list_jp_2.json'))'''


if __name__ == '__main__':
    # get_list('n45/n45.json', 'n45/n45_list.json')
    # get_check_list()
    #_list = loadData(os.path.join(dict_path, 'check_list_jp_2.json'))
    #print(len(_list))
    '''find_kana('コントロール')'''