from PDFCollect.serverPDF.getRule import getRule
from PDFCollect.serverPDF.judgeKey import judgeKey
from PDFCollect.parameterExtract.guifaRE import gfRE
from PDFCollect.parameterExtract.numberParameter import numberCS
from PDFCollect.parameterExtract.textParameter import textCS
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

    def __init__(self, newpdfText):
        self.ruleDatas = getRule().ruleDatas
        self.datas = newpdfText
        self.rowIDindex = 0
        self.rowData = 1
        # (self.csGetList, self.csAllList, self.unpdfTexts) = self.keyJudge()
        self.csLists = self.keyJudge()

    # 遍历每一个关键词,再遍历每一行pdf数据，获取参数值
        # 问题：一个关键词识别到多行，即多个值；一行被对个关键词识别，即包含多个参数；
        # 每个参数单独存一行，对应一个参数值；
    # 输出1：csAllList=所有参数-参数值；
    # 输出2：csGetList=提取到的参数-参数值；
    # 输出3：未识别的行数
    def keyJudge(self):
        csNum = 0
        csAllList = []
        csGetList = []
        unpdfTexts = []
        pdfDatas = self.datas
        for i in range(0, len(self.ruleDatas)):
            allRule = self.ruleDatas[i]
            keyWord = allRule["keyWord"]
            keyRE = allRule["re"]
            if keyWord != "":
                print("*" * 10, "第%s个关键词定位:%s" % (i+1, keyWord), "*" * 10)
                rulevalue = []
                ruleoldrowID = []
                rulerowID = []
                rulerowData = []
                for pd in pdfDatas:
                    # gfParameter = {}
                    d = pd[self.rowData]
                    # 判断文本是否与关键词匹配,匹配填入参数值，不匹配则返回为unpdfText中，用于发现新参数
                    if judgeKey(keyWord, d).judge:
                        # type判断1,是否为规范类参数
                        if allRule["type"] == "规范":
                            # 提取规范参数值state=1为规范，存入，否则不存入
                            csValueList = gfRE(d).gfValueList
                            if csValueList[1] == 1:
                                csValue = csValueList[0]
                                # 考虑一个参数对应多个值，每个key应该存一个数组，包括{value[],oldrowID[],rowID[],rowData[]}
                                rulevalue.append(csValue)
                            else:
                                rulevalue.append(d)
                        # typr判断2，是否为数值类参数
                        elif allRule["type"] == "数值":
                            # 判断有无正则
                            if keyRE != "":
                                numValue = numberCS(d, keyRE).csValue
                                if numValue != "":
                                    rulevalue.append(numValue)
                                    ruleoldrowID.append(pd[0])
                                    rulerowID.append(pd[self.rowIDindex])
                                    rulerowData.append(pd[self.rowData])
                            else:
                                rulevalue.append(d)
                                ruleoldrowID.append(pd[0])
                                rulerowID.append(pd[1])
                                rulerowData.append(pd[2])
                        # typr判断3，是否为文本类参数
                        elif allRule["type"] == "文本":
                            # 判断有无正则
                            if keyRE != "":
                                textValue = textCS(d, keyRE).csValue
                                if textValue != "":
                                    rulevalue.append(textValue)
                                    ruleoldrowID.append(pd[0])
                                    rulerowID.append(pd[1])
                                    rulerowData.append(pd[2])
                            else:
                                rulevalue.append(d)
                                ruleoldrowID.append(pd[0])
                                rulerowID.append(pd[1])
                                rulerowData.append(pd[2])
                        else:
                            rulevalue.append(d)
                            ruleoldrowID.append(pd[0])
                            rulerowID.append(pd[1])
                            rulerowData.append(pd[2])
                    else:
                        if i == 1:
                            unpdfTexts.append(pd)
                # 提取值正确则存入，未提取到则为空
                allRule["value"] = rulevalue
                allRule["oldrowId"] = ruleoldrowID
                allRule["rowID"] = rulerowID
                allRule["rowData"] = rulerowData
                csAllList.append(allRule)
                if len(rulevalue) > 0:
                    print("提取到参数：", allRule)
                    csNum += 1
                    csGetList.append(allRule)
        print("*" * 10, "模板参数%s个，共识别参数%s个" % (len(self.ruleDatas), csNum), "*" * 10)
        return [csGetList, csAllList, unpdfTexts]

    # 构建参数结构 = [{ID,fcsID,csName,csValue,csType,titleID,lastText,nextText,rowData},{}]
    def creatCS(self):
        csDict = {}
        csDict["ID"] = ""
        csDict["fcsID"] = ""
        csDict["csName"] = ""
        csDict["csValue"] = ""
        csDict["csType"] = ""
        csDict["titleID"] = ""
        csDict["lastText"] = ""
        csDict["nextText"] = ""
        csDict["rowData"] = ""
        return csDict