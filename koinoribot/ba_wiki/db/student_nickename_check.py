import json

with open('students_nickname.json', 'r', encoding='utf-8') as f:
    students_data = json.load(f)

with open('students.json', 'r', encoding='utf-8') as f:
    students_info = json.load(f)


chara_name = students_data['CHARA_NAME']
student_code_list = []
student_code_list_update = []


for i in chara_name.keys():
    student_code_list.append(i)


for i in students_info:
    student_code_list_update.append(str(i['Id']))

'''print(student_code_list)
print(student_code_list_update)'''

for i in student_code_list_update:
    if i not in student_code_list:
        print(f'缺失学生代码：{i}')
