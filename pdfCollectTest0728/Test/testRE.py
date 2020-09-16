import re

# restr = r"\d.\w+"
# con = "2.各种标高定义"
# line = re.match(restr, con)
# print(line.group())

# restr = r'\《.+?\》'
# # restr = r'《(.*?)》'
# con ='aaa《按时大大大多111问问www、。，按时大》,《公共建筑节能设计标准》北京市地方标准DB11/687-2015,aaaa啊啊啊《民用建筑工程室内环境污染控制规范》GB50325-2010（2013年版）,以及什么标准'
# str = re.findall(restr, con)
# print(str)
# for a in str:
#     print(a)
#     print("\n")


# nameString = "十、市规划国土函"
# nameString = re.sub(r'\w[、]', '', nameString)
# print(nameString)

# a="1.1市规划国土函 xx市(县）规划和国土资源管理委员会《关于xxxx项目规划国土意见的函》 市规划国土函（20xx）xxxx号   "
# print(a.replace(' ', ''.replace(' ','')))
# print(a.strip().replace(' ',''))
# print(re.sub(r'\s', '', a))
# print(re.split(r'\s',a))

# a= dict(aa=1,aaa=2,s=3,c=4)
# print(len(a))



# a= [1,2,3,4,5]
# print(a)
# for i in range(len(a)-1,-1,-1):
#     print(a[i])

# a = ["一", "一.", "一、", "1", "1.", "1、"]
# b = "一、设计说明"
# for aa in a:
#     if aa in b:
#         c = aa
# print(c)

# ptstr = "一撒大多数"
# if u'\u4e00' <= ptstr <= u'\u9fff':
#     print(1)


# 测试提取标题的正则
# aw = ["1", "1.", "1、", "a.", "a)", "1)", "1.1", "(1)"]
# titleRE = [r"\D、\w+", r"\d.\D\w+", r"\d.\d+\w+"]
# titleRE = [r'\d+[^.、)]\w+', r'\d+\.\D\w+', r'\d+\、\D\w+', r'[a-z]\.\W\w+', r'[a-z]\)\W\w+', r'\d+\)\D\w+', r'\d+\.\d+[^.、)]\w+', r'[(（]\d+[)）].+']
# print(titleRE[1])
# str = "1. 我的是什么"
# for tre in titleRE:
#     a = re.match(tre, str)
#     print(a)
#     if a != None:
#         print(a.group())

# str= "1.设计委托合同：《崇礼太舞四季文化旅游度假区一期工程第一部分项目设计合同》】"
# ptstr = re.split(r'[:：]', str)[0]
# print(ptstr)

# a = "1            屋顶          坡屋顶      挤塑苯板        B1       90+90X25%          0.33"
# aa = "asdads"
# p = a.count(' ')
# print(p)


# a = "abcdefg"
# b ="bcd"
# print(a.index(b))
# print(a[1:3])

# a = [1,2]
# b,c=a
# print(b)
# print(c)

