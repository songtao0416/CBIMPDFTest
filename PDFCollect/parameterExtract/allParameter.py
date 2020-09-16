from serverPDF.getRule import getRule
from serverPDF.judgeKey import judgeKey
from parameterExtract.guifaRE import gfRE
from parameterExtract.numberParameter import numberCS
from parameterExtract.textParameter import textCS
from parameterExtract.groudText import getgroudText
import re

"""
    通过关键词，确定所有关键词对应的语句
    获取对应语句中的参数值
    匹配到模板参数中，ID位置对应
    输入：newpdfText = [[拼接后行数，拼接后内容],[]]
         ruleDatas = [{id,name,type,lastType,keyWord,re,default}]
    输出：csLists = [csGetList,csAllList,unpdfTexts]
         csGetList =[{id,name,type,lastType,keyWord,re,default,value,oldrowID,rowID,rowData}]
         csGetList = {'id': '308', 'name': '无障碍设计规范', 'type': '规范', 'lastType': '3.0', 'keyWord': '无障碍设计&规范',
          're': '《(.*?)》','default': '《无障碍设计规范》GB50763-2012', 'value': ['《无障碍设计规范》GB50763', '《无障碍设计规范》
          GB50763'], 'oldrowId':[12, 261], 'rowID': [11, 172], 'rowData': ['f)《无障碍设计规范》GB50763—2012', 
          '1)本工程无障碍设计符合《无障碍设计规范》（GB50763—2012）。']}
"""
class allCSHandle:


    def __init__(self, newpdfText, othertitleList):
        self.ruleDatas = getRule().ruleDatas
        self.pdfText = newpdfText
        self.othertitleList = othertitleList
        self.rowIDindex = 0
        self.rowDataIndex = 1
        self.csidStart = 1
        # csLists = [csGetList, unpdfTexts]
        self.csLists = self.keyJudge()

    # 遍历每一行pdf数据，再遍历每一个关键词,获取参数值；
        # 问题：一个关键词识别到多行，即多个值；一行被对个关键词识别，即包含多个参数；
        # 每个参数单独存一行，对应一个参数值；
        # 先遍历文档，能够获取未识别行数，若先遍历关键词则重复获取未识别行数；
    # 输出1：csAllList=所有参数-参数值；
    # 输出2：csGetList=提取到的参数-参数值；
    # 输出3：未识别的行数
    def keyJudge(self):
        pdfTexts = self.pdfText
        csGetList = []
        unpdfTexts = []
        # todo 优化参数识别的单元代码，识别行 = 上级标题+行文本，再分句识别
        for rowPDF in pdfTexts:
            # judgeCS用于判断该行是否有参数，0为无参数，1为有参数
            judgeCS = 0
            # 获取该行所在父级标题的ID
            fatherTitleID = self.getFatherTitleID(rowPDF[self.rowIDindex])
            pd = rowPDF[self.rowDataIndex]
            # 优化1：分句，优化csValue长度
            cutRows = self.cutRowPDF(pd)
            for cutRow in cutRows:
                rowValues = []
                rowCSList = []
                # 优化2：加标题,优化关键词识别
                csData = self.getRowPDF(fatherTitleID, cutRow)
                # 读取关键词和正则和fcsID，每找到一个值，就存一次
                for i in range(0, len(self.ruleDatas)):
                    csRule = self.ruleDatas[i]
                    keyWord = csRule["keyWord"]
                    keyRE = csRule["re"]
                    fcsType = csRule["type"]
                    # 读取关键词，每找到一个值，就存一次
                    if keyWord != "":
                        # print("*" * 10, "第%s个关键词定位:%s" % (i+1, keyWord), "*" * 10)
                        if judgeKey(keyWord, csData).judge:
                            # 默认参数值为rowdata
                            csValues = [cutRow]
                            # 关键词ture，则判断类型，并选择正则提取参数值
                            # type判断1,是否为规范类参数
                            if fcsType == "2.0":
                                # 提取规范参数值state=1为规范，存入，否则不存入
                                gfValues = gfRE(cutRow, keyWord).gfValue
                                if gfValues != []:
                                    csValues = gfValues
                                # 规范，关键词匹配为《》外的词，导致未提取到该规范；解决方法，遍历完所有关键词，匹配失败立即结束本次
                                else:
                                    continue
                            # typr判断2，是否为数值类参数
                            elif fcsType == "3.0":
                                # 判断有无正则
                                if keyRE != "":
                                    numValues = numberCS(cutRow, keyRE).csValue
                                    csValues = [numValues]
                            # typr判断3，是否为文本类参数
                            elif fcsType == "1.0":
                                # 判断有无正则
                                if keyRE != "":
                                    textValue = textCS(cutRow, keyRE).csValue
                                    if textValue != "":
                                        csValues = [textValue]
                            # 同一行有多个同类的参数，分别存入
                            for csValue in csValues:
                                # 判断该参数是否已存入，一个参数值只能对应一个父类
                                if csValue not in rowValues:
                                    csDict = self.creatCS(rowPDF, csValue, csRule, fatherTitleID)
                                    rowCSList.append(csDict)
                                    judgeCS = 1
                                    rowValues.append(csValue)
                # 提取完该行所有参数后，cut各参数的上下文
                if rowCSList != []:
                    newrowCSList = getgroudText(rowCSList, pd).csList
                    for cs in newrowCSList:
                        print("已提取参数：", cs)
                    csGetList = csGetList + newrowCSList
            # 匹配不成功时，加入unpdfText，用于提取新参数,通过judgeCS判断
            if judgeCS == 0:
                unpdfTexts.append(rowPDF)
        print("*" * 10, "模板参数%s个，共识别参数%s个,未识别的pdf行数为%s" % (len(self.ruleDatas),len(csGetList),len(unpdfTexts)), "*" * 10)
        return csGetList, unpdfTexts

    # 构建参数结构 = [{ID,fcsID,fcsName,csName,csValue,csType,titleID,lastText,nextText,rowID,rowData},{}]
    # csRule = {id,name,type,lastType,keyWord,re,default}
    def creatCS(self, rowPDF, csValue, csRule, fatherTitleID):
        csDict = {}
        csDict["ID"] = str(self.csidStart)
        csDict["fcsID"] = csRule['id']
        csDict["fcsName"] = csRule['name']
        csDict["csName"] = "分项-" + csRule['name']
        csDict["csValue"] = csValue
        # todo 需完善参数类型识别，暂用父参数类别代替
        csDict["csType"] = csRule['type']
        # todo 参数的父级标题所在行 ok
        csDict["titleID"] = fatherTitleID
        csDict["lastText"] = ""
        csDict["nextText"] = ""
        csDict["rowID"] = rowPDF[self.rowIDindex]
        csDict["rowData"] = rowPDF[self.rowDataIndex]
        self.csidStart += 1
        return csDict

    # 获取其父级标题的rowID,二级标题
    # fatherTitles = [{titleID,titleName，titlePid, titleLV, titleText=[rowID,rowData]},{}]
    def getFatherTitleID(self, rowID):
        fatherTitles = self.othertitleList
        fatherID = rowID
        for fTitle in fatherTitles:
            # print("ftitle", fTitle)
            titleIndexs = fTitle["titleText"]
            startIndex = titleIndexs[0][0]
            endIndex = titleIndexs[-1][0]
            if startIndex <= rowID <= endIndex:
                fatherID = fTitle["titleID"]
                break
        return fatherID

    # 优化2：加标题
    def getRowPDF(self, fatherTitleID, pd):
        fatherTitles = self.othertitleList
        rowData = pd
        for ft in fatherTitles:
            if ft["titleID"] == fatherTitleID:
                ftName = ft["titleName"]
                rowData = ftName + pd
        return rowData

    # 优化1：分句
    def cutRowPDF(self, rowData):
        cutRows = re.split(r'。', rowData)
        return cutRows

    # 识别重复参数，相同参数应用同一个ID
    def sameCS(self):
        pass







