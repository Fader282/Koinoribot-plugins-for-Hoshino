import time,sys
import random
import numpy as np

pai_m = list(range(1,10))
pai_s = list(range(11,20))
pai_p = list(range(21,30))
pai_z = list(range(31,38,2))
pai_y = list(range(41,46,2))
lao_tou = [1,9,11,19,21,29]
lv_pai = [12,13,14,16,18,43]
pai_shun = list(range(1,8))+list(range(11,18))+list(range(21,28))
pai_all = pai_m + pai_s + pai_p + pai_z + pai_y
zi_pai = pai_z + pai_y
yi_zhong = ['所含役满有：']

def if_zi_yi_se(dan_pai): # 单牌
	number = 0
	for i in dan_pai:
		if i in zi_pai:
			number += 1
	if number == len(dan_pai):
		yi_zhong.append('- 字一色')

def if_qing_lao_tou(dan_pai):
	number = 0
	for i in dan_pai:
		if i in lao_tou:
			number += 1
	if number == len(dan_pai):
		yi_zhong.append('- 清老头')

def if_si_xi(dan_pai): # 四暗刻专用
	number = 0
	if dan_pai[-1] in pai_z:
		number += 1
	for i in dan_pai[:4]:
		if i in pai_z:
			number += 2
	if number == 7:
		yi_zhong.append('- 小四喜')
	elif number == 8:
		yi_zhong.append('- 大四喜')

def if_lv_yi_se(dan_pai):
	number = 0
	for i in dan_pai:
		if i in lv_pai:
			number += 1
	if number == len(dan_pai):
		yi_zhong.append('- 绿一色')

def redraw(a:list):
	pai_pic = {
		0:'🀫',1:'🀇',2:'🀈',3:'🀉',4:'🀊',5:'🀋',6:'🀌',7:'🀍',8:'🀎',9:'🀏',
		11:'🀐',12:'🀑',13:'🀒',14:'🀓',15:'🀔',16:'🀕',17:'🀖',18:'🀗',19:'🀘',
		21:'🀙',22:'🀚',23:'🀛',24:'🀜',25:'🀝',26:'🀞',27:'🀟',28:'🀠',29:'🀡',
		31:'🀀',33:'🀁',35:'🀂',37:'🀃',41:'🀄',43:'🀅',45:'🀆'
	}
	b = [pai_pic[i] if i in pai_pic else i for i in a]
	final = ''.join(b)
	return final

def si_an_ke(): # 四暗刻
	dan_pai = random.sample(pai_all,5) # 随机选出五张牌
	shou_pai = []
	a = list(np.repeat(dan_pai[:4],3)) # 前4张做刻子
	b = list(np.repeat(dan_pai[-1],2)) # 后1张做雀头
	shou_pai = a + b
	yi_zhong.append('- 四暗刻')
	if_zi_yi_se(dan_pai)
	if_qing_lao_tou(dan_pai)
	if_si_xi(dan_pai)
	return sorted(shou_pai)

def jiu_lian(): # 九莲宝灯
	pai_xing = [1,1,1,2,3,4,5,6,7,8,9,9,9]
	shou_pai = []
	pai_xing.append(random.choice(pai_m)) # 再补一张和牌
	if random.randrange(100)<=33: # 分三类，万条饼的九莲
		shou_pai = pai_xing
	elif random.randrange(100)<=66:
		for i in pai_xing:
			shou_pai.append(i + 10)
	else:
		for i in pai_xing:
			shou_pai.append(i + 20)
	yi_zhong.append('- 九莲宝灯')
	return sorted(shou_pai)

def guo_shi(): # 国士无双
	pai_xing = [1,9,11,19,21,29,31,33,35,37,41,43,45]
	pai_xing.append(random.choice(pai_xing))
	yi_zhong.append('- 国士无双')
	return sorted(pai_xing)

def lv_yi_se(): # 绿一色
	dan_pai = []
	shou_pai = []
	if random.randrange(100)<=70:
		dan_pai = random.sample(lv_pai,5) # 不带顺子，4刻1雀头
		a = list(np.repeat(dan_pai[:4],3))
		b = list(np.repeat(dan_pai[-1],2))
		shou_pai = a + b
	else:
		shun_zi = [12,12,13,13,14,14] # 带顺子
		a = list(np.repeat(random.choice([12,13,14]),2))
		b = list(np.repeat(random.sample([16,18,43],2),3))
		shou_pai = shun_zi + a + b
	yi_zhong.append('- 绿一色')
	return sorted(shou_pai)

def xiao_si_xi(): # 小四喜
	si_xi = list(np.repeat([31,33,35,37],3))
	del si_xi[random.randrange(12)] # 大四喜随机抠一张
	if random.randrange(100) <= 25:
		a = list(np.repeat(random.choice(pai_m + pai_s + pai_p + pai_y),3))
		yi_zhong.append('- 四暗刻')
	else:
		shun_zi = int(random.choice(pai_shun))
		a = [shun_zi, shun_zi + 1, shun_zi + 2]
	shou_pai = si_xi + a
	yi_zhong.append('- 小四喜')
	if_zi_yi_se(list(set(shou_pai)))
	return sorted(shou_pai)
 
def da_si_xi(): # 大四喜
	si_xi = list(np.repeat([31,33,35,37],3))
	a = list(np.repeat(random.choice(pai_m + pai_s + pai_p + pai_y),2))
	shou_pai = si_xi + a
	yi_zhong.append('- 四暗刻')
	if_zi_yi_se(list(set(shou_pai)))
	yi_zhong.append('- 大四喜')
	return sorted(shou_pai)

def qing_lao_tou(): # 清老头
	dan_pai = random.sample(lao_tou,5)
	a = list(np.repeat(dan_pai[:4],3))
	b = list(np.repeat(dan_pai[-1],2))
	shou_pai = a + b
	yi_zhong.append('- 四暗刻')
	yi_zhong.append('- 清老头')
	return sorted(shou_pai)

def da_san_yuan(): # 大三元
	a = list(np.repeat(pai_y,3)) # 三元
	if random.randrange(2) < 1:
		ke_zi = random.sample(pai_m + pai_s + pai_p + pai_z,2) # 四暗刻大三元的剩下的牌
		que_tou = list(np.repeat(ke_zi[0],2)) 
		b = list(np.repeat(ke_zi[1],3))
		yi_zhong.append('- 四暗刻')
	else:
		que_tou = list(np.repeat(random.choice(pai_m + pai_s + pai_p + pai_z),2))
		shun_zi = int(random.choice(pai_shun)) # 顺子第一张
		b = [shun_zi, shun_zi + 1, shun_zi + 2] # 顺子
	shou_pai = a + que_tou + b
	yi_zhong.append('- 大三元')
	if_zi_yi_se(list(set(shou_pai)))
	return sorted(shou_pai)

def zi_yi_se(): # 字一色
	dan_pai = random.sample(pai_z + pai_y,5)
	a = list(np.repeat(dan_pai[:4],3))
	b = list(np.repeat(dan_pai[-1],2))
	shou_pai = a + b
	if_si_xi(dan_pai)
	yuan = 0
	for i in dan_pai[:4]:
		if i in pai_y:
			yuan += 1
	if random.randrange(100) < 10:
		shou_pai = [31,31,33,33,35,35,37,37,41,41,43,43,45,45]
		yuan = 0 # 不计大三元
		yi_zhong.append('- 大七星*')
	if yuan == 3:
		yi_zhong.append('- 大三元')
	yi_zhong.append('- 字一色')
	return sorted(shou_pai)


def si_gang_zi(): # 四杠子
	dan_pai = random.sample(pai_all,5)
	blank = [' ',]
	a = list(np.repeat(dan_pai[0],2)) # 第一张作为雀头
	g1 = list(np.repeat(dan_pai[1],4))
	g2 = list(np.repeat(dan_pai[2],4))
	g3 = list(np.repeat(dan_pai[3],4))
	g4 = list(np.repeat(dan_pai[4],4))
	gang = [g1,g2,g3,g4]
	an_gang = 0
	san_yuan = 0
	si_xi = 0
	for gn in gang:
		if random.randrange(10) <= 2:
			gn[0] = 0
			gn[-1] = 0
			an_gang += 1
	shou_pai = a + blank + g1 + blank + g2 + blank + g3 + blank + g4
	for i in pai_y:
		if i in dan_pai[1:5]:
			san_yuan += 1
	for i in pai_z:
		if i == dan_pai[0]:
			si_xi += 1
		elif i in dan_pai[1:4]:
			si_xi += 2
	if an_gang == 4:
		yi_zhong.append('- 四暗刻')
	if san_yuan == 3:
		yi_zhong.append('- 大三元')
	if si_xi == 7:
		yi_zhong.append('- 小四喜')
	if si_xi == 8:
		yi_zhong.append('- 大四喜')
	if_zi_yi_se(shou_pai)
	yi_zhong.append('- 四杠子')
	return shou_pai

def recipe(yi_zhong):
	a = '\n'.join(yi_zhong)
	return a

def random_yiman():
	if random.randrange(100000) <= 10000:
		yi = si_gang_zi()
	elif random.randrange(100000) <= 20000:
		yi = jiu_lian()
	elif random.randrange(100000) <= 30000:
		yi = da_si_xi()
	elif random.randrange(100000) <= 40000:
		yi = lv_yi_se()
	elif random.randrange(100000) <= 50000:
		yi = qing_lao_tou()
	elif random.randrange(100000) <= 60000:
		yi = xiao_si_xi()
	elif random.randrange(100000) <= 70000:
		yi = zi_yi_se()
	elif random.randrange(100000) <= 80000:
		yi = guo_shi()
	elif random.randrange(100000) <= 90000:
		yi = si_an_ke()
	else:
		yi = da_san_yuan()
	return yi

'''
a = redraw(da_si_xi())
print(a)
b = recipe(yi_zhong)
print(b)
'''