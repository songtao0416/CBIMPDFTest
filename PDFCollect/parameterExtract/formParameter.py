import re

from serverPDF.matchAecname import aecName
from serverPDF.getAecdict import getAecdict
from serverPDF.getRule import getRule
from recognizePDF.judgePDF import judgePDF
from recognizePDF.docPDF import docPDF
from config.configPDF import configPDF
from serverPDF.judgeKey import judgeKey

"""
    表格类参数提取步骤：
        获取表格信息——读取表头——参数名、参数值——识别参数父类——构建参数
        定位表内参数——有父类的为参数，无父类的为固定部分——同列参数为多个子级参数
    
    提取表格信息-表格定位-表格上一行内容-对比表格名的关键词-确定参数或新参数-返回
    输入：formList = [[table],]
         ruleDatas = [{id,name,type,lastType,keyWord,re,default}]
         csRules = [{id,name,type,lastType,keyWord,re,default}]
         formRows = [[tablerowData，rowID],[]]
    输出：formCSList = [{}]
"""

class formCS:

    def __init__(self, formRows, formList):
        self.formList = formList
        self.aecDict = getAecdict().aecDict
        self.csRules = getRule().ruleDatas
        self.formRows = formRows
        self.formKeyword = configPDF().formKeywords
        self.csidStart = 1
        self.formCSList = self.getFormList()

    def getFormList(self):
        formCSList = []
        for formData in self.formList:
            print("formData", formData)
            # 获取表中参数名称
            newformCSlist = self.getHeading(formData)
            formCSList = formCSList + newformCSlist
        print(formCSList)
        return formCSList


    # 提取表头为参数名称：csName
    # 考虑一个表头cell对应多个参数，csName = 表头cell + 序号， csValue = cell
    def getHeading(self, formData):
        # 获取表头的信息,默认第一行为表头，且只有一行表头
        formrowID = self.getFormRowID(formData)
        formCSList = []
        headingRow = formData[0]
        fixHeadings = configPDF().formFixHeading
        # 第一列为序号，第二列为rowName，获取列名称
        for i in range(0, len(headingRow)):
            head = headingRow[i]
            if head not in fixHeadings:
                if head == None:
                    head = headingRow[i - 1]
                colName = head
                # 获取行名称
                for j in range(1, len(formData)):
                    rowName = formData[j][1]
                    csName = rowName + "-" + colName
                    csValue = formData[j][i]
                    rowID = [i, j]
                    # 对比规则库，获取其校验父类
                    fcsRule = self.getfatherCS(csName)
                    formCSDict = self.creatCS(csName, csValue, rowID, fcsRule, formData, formrowID)
                    print("表格中参数", formCSDict)
                    formCSList.append(formCSDict)
        return formCSList

    # 确定表格所在行
    def getFormRowID(self,pdfForm):
        # 表格定位，定位到该行的标题内容，作为表格参数名，截取到第一个句号为止
        pdfRows = self.formRows
        formrowID = "unknown"
        # 表格首行数据
        row = pdfForm[0]
        # 遍历表格单元格比较行数据，得到rowID
        for pdfRow in pdfRows:
            j = 0
            for cell in row:
                if cell != None:
                    if cell in pdfRow[1]:
                        j += 1
                if j == 3:
                    print("表格所在行为：", pdfRow)
                    break
            if j > 2:
                formrowID = pdfRow[0]
                return formrowID


    """
        获取cs对应的父类校验参数和校验规则;
            最好方法:表格父类;校验规则为list;其次:表格参数的父类
            其次：参数名。关键词匹配，定位父类参数
            csRules = [{id,name,type,lastType,keyWord,re,default}]
    """
    def getfatherCS(self, csName):
        csRules = self.csRules
        fcsRule = {}
        fcsRule["id"] = "newCS"
        fcsRule["name"] = "新参数"
        for csRule in csRules:
            keyWord = csRule["keyWord"]
            if keyWord != "":
                # 关键词判断，匹配返回csRule,全部不匹配返回none
                if judgeKey(keyWord, csName).judge:
                    fcsRule = csRule
                    break
        return fcsRule


    # 构造formcsDict
    # csList = [{ID,fcsID,fcsName,csName,csValue,csType,titleID,lastText,nextText,rowID,rowData}]
    def creatCS(self,csName,csValue,rowID,csRule, formData, formrowID):
        csDict = {}
        csDict["ID"] = "table" +str(self.csidStart)
        csDict["fcsID"] = csRule['id']
        csDict["fcsName"] = csRule['name']
        csDict["csName"] = csName
        csDict["csValue"] = csValue
        csDict["csType"] = "表格"
        csDict["titleID"] = rowID
        csDict["lastText"] = ""
        csDict["nextText"] = ""
        csDict["rowID"] = formrowID
        csDict["rowData"] = formData
        self.csidStart +=1
        return csDict



# 测试
# f = "F:\\项目代码\\Python代码\\CBIM设计说明文档识别\\PDFCollect\\resources\\pdf文本\\崇礼度假区\\崇礼度假区（建筑单专业） H建施-001 - 设计说明及图纸目录.pdf"
# pdfPath = f
# pdfText = docPDF(pdfPath).getpdfminer()
# nnewpdfText, ftitleList, formRows = judgePDF(pdfText).pdfTitleText
# formCS(pdfPath, formRows)