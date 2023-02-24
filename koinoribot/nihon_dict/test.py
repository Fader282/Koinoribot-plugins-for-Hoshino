import re

text = '今天你是什么少女[CQ:at,qq=2530075673][CQ:at,qq=2530075673]'

match = re.match(r'(今天你是什么少女)\[CQ:at,qq=(\d+?)\]',text)

creep_id = match.group(2)

print(type(creep_id))