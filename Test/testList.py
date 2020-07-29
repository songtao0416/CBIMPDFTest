import re

a=['市规划', '国土函']
b ="市规划国土函"
str = "1.1市规划国土函 xx市(县）规划和国土资源管理委员会《关于xxxx项目规划国土意见的函》 市规划国土函（20xx）xxxx号"
for aa in a:
    if aa in str:
        print(1)
    else:
        print(2)
if b in str:
    print(3)