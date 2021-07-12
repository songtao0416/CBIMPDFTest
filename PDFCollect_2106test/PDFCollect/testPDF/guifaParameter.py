import re
from PDFCollect.serverPDF.getRule import getRule
from PDFCollect.serverPDF.judgeKey import judgeKey

"""
    已优化到allParameter.py中，该方法不再使用
    确定数据所在行
    先正则去掉多余字符，避免关键词识别错误
    正则提取参数值，数字结尾
    关键词定位，对应参数
    输入参数：newpdfText = [[原行数，拼接后行数，拼接后内容]]
            gfRules:[{id,name,type,lastType,keyWord,re,default}]
    输出参数：参数值
"""
class guifaCS:

    def __init__(self, newpdfText):
        self.datas = newpdfText
        self.gfRules = getRule().gfRules
        self.csJudge()

    # 通过正则获取所有规范类型的参数
    def csJudge(self):
        guifaList = []
        for content in self.datas:
            rowData = content[-1]
            if "《" in rowData:
                if "》" in rowData:
                    reCon = self.gfRE(rowData)
                    guifaList.append([content[0],content[1],content[2],reCon])
        print(guifaList)
        self.keyJudge(guifaList)

    # 规范的正则处理，获得《》+版本
    def gfRE(self, data):
        da = re.sub(r'\（', '', data)
        db = re.findall(r'(《.*?》[\x00-\xff]*)', da)
        if len(db) > 0:
            # print(data)
            newData = db[0]
            print(newData)
            return newData

    # 规范类型参数的关键词识别
    # datas = gufiaList = [[原id，现行数id，各行内容，re后的内容]]
    # 返回1：gfParameters=[{'name': '规范-装修1', 'value': '《公共建筑节能设计标准》GB 50189-2005', 'keyWord': '污染控制||装饰装修',
    # 'type': '规范', 'lastType': '3.0', 'oldrowId': 13, 'rowID': 12, 'rowData': 'g)《公共建筑节能设计标准》GB 50189-2005',
    # 'default': '《民用建筑工程室内环境污染控制规范》 GB 50325-2010（2013年版）'}]
    # 返回2：gfRules对应的数据list，注意参数的序号
    def keyJudge(self, datas):
        print("关键词定位")
        # print(self.gfRules)
        gfParameters = []
        # 根据关键词，找对应的行，提取参数值
        for i in range(0, len(self.gfRules)):
            gfRule = self.gfRules[i]
            keyWord = gfRule["keyWord"]
            print(keyWord)
            for pd in datas:
                gfParameter = {}
                d = pd[-1]
                if judgeKey(keyWord, d).judge:
                    print("关键词：%s,\t参数名：%s,\t参数值：%s" % (keyWord, gfRule["name"], d))
                    # gfRules:[{name,type,lastType,keyWord,re,default}]
                    # 数据：关键词-参数值（多对多）
                    gfParameter["name"] = gfRule["name"]
                    gfParameter["value"] = pd[3]
                    gfParameter["keyWord"] = keyWord
                    gfParameter["type"] = gfRule["type"]
                    gfParameter["lastType"] = gfRule["lastType"]
                    gfParameter["oldrowId"] = pd[0]
                    gfParameter["rowID"] = pd[1]
                    gfParameter["rowData"] = pd[2]
                    gfParameter["default"] = gfRule["default"]
                    gfParameters.append(gfParameter)
                    # 数据：id-参数-参数值，多对多
                    gfRule["value"] = pd[3]
                    gfRule["oldrowId"] = pd[0]
                    gfRule["rowID"] = pd[1]
                    gfRule["rowData"] = pd[2]
                    print(gfRule)
                else:
                    gfRule["value"] = ""
                    gfRule["oldrowId"] = ""
                    gfRule["rowID"] = ""
                    gfRule["rowData"] = ""
        print("gf全部爬取参数")
        for gf in self.gfRules:
            if gf["value"] != "":
                print(gf)




