# a = '²'
# print(type(a))
# print(len(a))
# print(a)
#
import re
# aa = '《建筑工程设计文件编制深度规定》（2008年版）,《民用建筑设计通则》GB 50352—2005的'
# aa =re.sub(r'\（','',aa)
# print(aa)
# a = re.findall(r'(《.*?》[\x00-\xff]*)', aa)
# # for aaa in a:
# #     ab = re.findall(r'[\u4e00-\u9fa5]', aaa)
# print(a[0])
# print(type(a))

# a = "12)内外墙留洞：钢筋混凝土梁、垂板侧墙预留洞，见结施和设备施工图纸；非承重墙预留洞见建施和设备施工图纸。墙体预留洞需二次封堵。"
# aa = "钢筋混凝土梁、垂板侧"
# if re.match(r'\d+[.)]', a):
#     print(1)

# st = 'rtfh'
# print(st.isdigit())
# if st.isdigit() == True:
#     print(1)

# aa = {"a":1,"b":1}
# aaa= list(aa.values())
# print(aa["a"])
# print(aaa)

# -*- coding: utf-8 -*-

# import os
#
# file_dir = "F:\\项目代码\\Python代码\\CBIM设计说明文档识别\\PDFCollect\\pdf文本\\崇礼度假区"
# for root, dirs, files in os.walk(file_dir):
#     print(root) #当前目录路径
#     print(dirs) #当前路径下所有子目录
#     print(files) #当前路径下所有非目录子文件

# a =[1]
# b=[2]
# c = a+b
# print(c)
# a=[1]
# if a == []:
#     print(1)

# a = ""
# if a == "":
#     print(1)
# s = "工种负责人DISCIPLINECHIEF:樊珣"
# w = "工种负责人"
# rp = re.compile(r'%s[：|:]?(.+)' % w)
# # rp = re.compile(r'%s(.+)' % w)
# v = rp.findall(s)
# print(v)
# import string
# def isEN(v):
#     for i in v[0]:
#         if i not in string.ascii_lowercase+string.ascii_uppercase:
#             return False
#     return True
# if isEN(v):
    # print(1)


# np = s.find(w)
# np2 = s.find(":")
# print(np2)
# print(np+len(w)-1)
# if np2-(np+len(w)-1) >1:
#     print(1)

# from collections import Counter
# sting ="asd:asd:asD:asd:asd"
# res = Counter(sting)
# print(res)

# a = "4)屋顶、外墙等部位围护结构节能设计序号部位保温材料保温材料厚度（mm）传热系数KW/（m2.K）序号              部位                  保温材料"
# aa=""
# a = re.split('\s',a)
# print(a)
# for s in a[0]:
#     print(s)
#     if '\u4e00' <= s <= '\u9fa5':
#         aa = aa+s
# print(aa)

# 测试字符长度，对齐空格数量
# d = ["哈哈","哈哈哈哈","哈哈哈"]
# for dd in d:
#     a = "【参数行%s】" % dd + " " * (20-len(dd)*2)+ dd
#     print(len(dd))
#     print(len("【参数行%s】" % dd))
#     print(20-len(dd))
#     print(a)

# 测试sub的正则
# rowData= " 2.建设用地规划许可证（地字第130733201400013号【*建设用地规划许可证（地字第）*】字第130733201400013号）"
# a = re.sub(r'[\d.]+', '', rowData)
# print(a)
# b = re.search(r'[(（].+?[)）]', rowData).group()
# print(b)


sss =["d)屋面檐沟纵向坡度不应小于1%","d)屋面檐沟纵向坡度≤1%","d)屋面檐沟纵向坡度1/12"]
for ss in sss:
    rp = re.compile(r'[度]\w*[于≤≥](\d+%)')
    aa = rp.findall(ss)
    print(aa)
