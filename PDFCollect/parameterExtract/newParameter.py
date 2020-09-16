import re
from parameterExtract.guifaRE import gfRE
from serverPDF.matchAecname import aecName
from serverPDF.getAecdict import getAecdict
from parameterExtract.groudText import getgroudText

"""
    获取文档中的新参数
    逻辑：参数库对应提起后，对剩余文本进行新参数提取
    输入：leftPdfText = [[原行数，拼接后行数，拼接后内容]]
    输出：newCSList = [{id,name,type,lastType,keyWord,re,default,value,oldrowID,rowID,rowData}]
"""

class newParameter:

    def __init__(self, unpdfText):
        self.pdfText = unpdfText
        self.aecDict = getAecdict().aecDict
        self.rowIDIndex = 0
        self.rowDataIndex = 1
        self.newcsID = 1
        self.newCSList = self.judgeType()

    """
        遍历每行pdf
        先进行规范判断
            参数名提取
            参数值提取
        再进行数值判断
        再进行文本判断
            参数值提取
    """
    def judgeType(self):
        newCSList = []
        aecDict = self.aecDict
        pdfNum = len(self.pdfText)
        # 遍历每一行，提取参数
        print(self.pdfText)
        for rowPDF in self.pdfText:
            # print("*" * 10, "未匹配PDF共%s行，正在识别第%s行" % (pdfNum, i), "*" * 10)
            pd = rowPDF[self.rowDataIndex]
            # 判断参数名是否匹配
            newName = aecName(pd, aecDict).newName
            # 判断参数名
            if newName == None:
                newName = "unknown"
            else:
                # 判断是否为规范类参数,true返回参数值，false返回空值
                csValues = gfRE(pd, "").gfValue
                if csValues == []:
                    csValues = [pd]
                # 构建参数
                for csValue in csValues:
                    (lastText, nextText) = "",""
                    newCSDict = self.getNewParameter(newName, csValue, rowPDF, lastText, nextText)
                    # todo 增加数值参数/表格参数/文本参数的判断
                    print("发现新参数:", newCSDict)
                    newCSList.append(newCSDict)
        print("*" * 10, "未匹配PDF共%s行，共识别新参数%s个, 未识别%s个" % (pdfNum, self.newcsID, (pdfNum-self.newcsID)), "*" * 10)
        return newCSList

    def getNewParameter(self, newName, csValue, rowPDF, lastText, nextText):
        # csList = [{ID,fcsID,fcsName,csName,csValue,csType,titleID,lastText,nextText,rowID,rowData}]
        csDict = {}
        csDict["ID"] = "newCS%s" % self.newcsID
        csDict["fcsID"] = "newCS"
        csDict["fcsName"] = "新参数"
        csDict["csName"] = newName
        csDict["csValue"] = csValue
        csDict["csType"] = ""
        csDict["titleID"] = rowPDF[self.rowIDIndex]
        csDict["lastText"] = lastText
        csDict["nextText"] = nextText
        csDict["rowID"] = rowPDF[self.rowIDIndex]
        csDict["rowData"] = rowPDF[self.rowDataIndex]
        self.newcsID += 1
        return csDict





