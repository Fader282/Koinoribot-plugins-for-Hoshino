import json
from .student_info import *


student_list = json.load(open(os.path.join(database_path, 'students_nickname.json'), encoding="utf-8"))["CHARA_NAME"]
msg = ''
i = 0
msglist = []
for name_list in student_list.values():
    name = name_list[1:]
    msg += '、'.join(name)
    msg += '\n'
    i += 1
    if i >= 10:
        msglist.append(msg)
        i = 0
        msg = ''


if __name__ == '__main__':
    print(msglist)
