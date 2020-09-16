import re
from recognizePDF.formPDF import formPDF
from config.configPDF import configPDF
from collections import Counter
import string

"""
    处理PDF右侧标题栏中的数据
    不需要获取表结构，只需要参数
    输入参数：rightTable = [[]]
    输出参数：csList =[{name,value,rowData}] 
"""

class rightForm:

    def __init__(self, rightformList):
        self.tables = rightformList
        self.csidStart = 1
        # todo 右侧明细表可建立参数词表对应参数名称,需丰富明细表中的参数名
        self.rightCSNames = configPDF().rightCSNames
        self.rightCSList = self.readTbale()

        # 遍历表格
    def readTbale(self):
        rightCSList = []
        for table in self.tables:
            newRighttable = self.handleTable(table)
            CSList = self.getrightCS(newRighttable)
            rightCSList = rightCSList + CSList
        return rightCSList

    def handleTable(self, table):
        # 第一行第一项为全文本，去除多余文本，保留firstLine
        table[0][0] = None
        newTable = []
        for line in table:
            newRow = self.handleRow(line)
            if newRow != "":
                newTable.append(newRow)
        # for x in newTable:
        #     print(x)
        return newTable

    # 处理每行数据，先去掉空值，再切割list
    def handleRow(self, line):
        newRow = []
        row = list(filter(None, line))
        # print("row", row)
        for r in row:
            # print("r", r)
            r = re.split(r'\n',r)
            for i in range(0, len(r)):
                r[i] = re.sub(r'\s','', r[i])
            # r =[]
            # if len(r) > 1:
            #     # todo 一个[]中两个人名，需要分开，再分行，暂不处理
            #     newRow.append(r)
            # elif r != "":
            #     newRow.append(''.join(r))
            for rr in r:
                if rr != "":
                    newRow.append(rr)
        #  [['设计制图人', 'DRAFTINGDESIGNER', '审定', 'APPROVEDBY'], ['樊珣', '熊承新']]
        newRow =':'.join(newRow)
        return newRow

    # 提取参数
    def getrightCS(self, newRighttable):
        pdfTexts = newRighttable
        csNames = self.rightCSNames
        csList = []
        print("*" * 10, "提取右侧参数", "*" * 10)
        i = 0
        for word in csNames:
            for pdfRow in pdfTexts:
                if word in pdfRow:
                    i += 1
                    # 通过距离判断word是接着：，存在则re=：，不存在则re=word
                    # wordIndex = pdfRow.find(word)+len(word)-1
                    # mIndex = pdfRow.find(":")
                    # res = Counter(pdfRow)
                    # if res[":"] > 1:
                    #     # 距离大于1则未连接
                    #     if mIndex - wordIndex > 1:
                    #         rp = re.compile(r'%s(.+):' % word)
                    #     else:
                    #         rp = re.compile(r'[:|：](.+)')
                    # else:
                    #     # 距离大于1则未连接
                    #     if mIndex - wordIndex > 1:
                    #         rp = re.compile(r'%s(.+)' % word)
                    #     else:
                    #         rp = re.compile(r'%s[:|：]?(.+)' % word)
                    rp = re.compile(r'%s[:|：]?(.+)' % word)
                    csREList = rp.findall(pdfRow)
                    if csREList != []:
                        csValue = csREList[0]
                        csValue = self.cutEN(csValue)
                    else:
                        csValue =""
                    csDict = self.creatCS(word,csValue,-i,pdfRow)
                    print("明细表参数", csDict)
                    csList.append(csDict)
        return csList

    # if 第二个字符是字母，则去掉全部字母
    def cutEN(self, row):
        e = row[1]
        if e not in string.ascii_lowercase+string.ascii_uppercase:
            return row
        else:
            newRow = re.sub(r'[a-zA-Z]','',row)
            return newRow

    # 构建参数
    def creatCS(self,word,csValue,rowID,pdfRow):
        csDict = {}
        csDict["ID"] = "rightCS" +str(self.csidStart)
        csDict["fcsID"] = "rightCS"
        csDict["fcsName"] = "明细表"
        csDict["csName"] = word
        csDict["csValue"] = csValue
        csDict["csType"] = "表格"
        csDict["titleID"] = "-1"
        csDict["lastText"] = ""
        csDict["nextText"] = ""
        csDict["rowID"] = rowID
        csDict["rowData"] = pdfRow
        self.csidStart +=1
        return csDict




# # 测试
# f = "F:\\项目代码\\Python代码\\CBIM设计说明文档识别\\PDFCollect\\resources\\pdf文本\\崇礼度假区\\崇礼度假区（建筑单专业） H建施-001 - 设计说明及图纸目录.pdf"
# rightForm(f)

"""
    测试结果：
        ['项目经理', '魏篙川']
        ['设计部门负责人', '樊珣']
        ['会签栏']
        ['专业', '签字', '日期']
        ['总图']
        ['建筑']
        ['结构']
        ['给排水']
        ['暖通']
        ['动力']
        ['电气']
        ['电讯']
        ['签章区']
        ['合作方名称区', 'ZEHREN', 'ANDASSOCIATES', 'ARCHITECTURE•PLANNING', 'INTERIORS•LANDSCAPEARCHITECTURE', 'Avon,Colorado(970)949-0257', 'SantaBarbara,California(805)963-6890', 'www.zehren.com', '迈进工程设计咨询（北京）有限公司', 'Meinhardt(beijing)LTD', '23/FHuaTengPlaza,No.302Jia,', 'JinsongZone3,ChaoyangDistrict,', 'Beijing,100021,China', 'Telephone:(8610)85997976', 'Fax:(8610)85997186']
        ['平面示意', 'KEYPLAN']
        ['工程名称崇礼太舞四季文化旅游度假区', 'PROJECT一期工程第一部分项目']
        ['子项', 'H座酒店', 'SUBITEM']
        ['设计号', '12267', 'PROJECTNO.']
        ['图号', '建施-001', 'DWG.NO']
        ['比例', '——', 'SCALE', '日期', '2015-01-13', 'DATE']
        ['图名', '设计说明及图纸目录', 'TITLE']
        ['设计主持人', 'DESIGNCHIEF', '魏篙川/樊珣']
        ['工种负责人', 'DISCIPLINECHIEF', '樊珣']
        ['设计制图人', 'DRAFTINGDESIGNER', '审定', 'APPROVEDBY', '樊珣', '熊承新']
        ['审核', '张波', 'VERIFIEDBY', '校对', '杜双', 'CHECKEDBY', '设计部门', '国际设计咨询所', 'DESIGNDEPT']
        ['设计证书号：A111002193', '本图纸版权归本院所有，不得用于本工程以外范围', 'Thisdrawing&designarecopyrightandnoportionmaybe', 'reproducedwithoutthewrittenpermissionoftheCAG']
        
        Process finished with exit code 0

"""