import re
import operator

a = '15 + ((3 + 3) * 4)'
l = {'a': ['3', '15', '3', '4']}
c = ['3', '4', '3', '15']

replace_dict = {
    ' ': '',
    '＋': '+',
    '－': '-',
    '＊': '*',
    '×': '*',
    'x': '*',
    '／': '/',
    '÷': '/',
    '[': '(',
    ']': ')',
    '{': '(',
    '}': ')',
    '（': '(',
    '）': ')',
    '【': '(',
    '】': ')',
}

def format_expression(string: str):
    """
        将表达式格式化
    """
    for k, v in replace_dict.items():
        string = string.replace(k, v)
    return string

if __name__ == '__main__':
    b = eval(format_expression(a))
    match = re.findall(r'(\d+)', a)
    print(round(b, 2))
    match.sort()
    b = l['a']
    b.sort()
    print(l['a'])
    print(match)
    print(operator.eq(match, b))
    print(match == b)