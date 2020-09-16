import re
from PDFCollect.recognizePDF.formPDF import formPDF
from PDFCollect.serverPDF.matchAecname import aecName
from PDFCollect.serverPDF.getAecdict import getAecdict
from PDFCollect.serverPDF.getRule import getRule
from PDFCollect.recognizePDF.judgePDF import judgePDF
from PDFCollect.recognizePDF.docPDF import docPDF
from PDFCollect.config.configPDF import configPDF
"""
    从formList中提取form参数,独立提取，跟all和new分开
    提取表格信息-表格定位-表格上一行内容-对比表格名的关键词-确定参数或新参数-返回
    输入：formList = [[table],]
         ruleDatas = [{id,name,type,lastType,keyWord,re,default}]
    输出：formCSList = [{}]
"""

class formCS:

    def __init__(self, pdfPath, newpdfText):
        self.formList = formPDF(pdfPath).formList
        self.aecDict = getAecdict().aecDict
        self.csRules = getRule().ruleDatas
        self.newpdfText = newpdfText
        self.formKeyword = configPDF().formKeywords
        self.formCSList = self.getForm()

    # 考虑类型不确定，对全部参数关键词进行判断
    # 不同于文本,先关键词,再文本匹配;而是先表格,再关键词匹配
    def getForm(self):
        formCSList = []
        for pdfForm in self.formList:
            print("pdf表格", pdfForm)
            # self.ruleJudge(pdfForm)
            formCS = self.formName(pdfForm)
            if formCS != "":
                formCSList.append(formCS)
        return formCSList

    # 表格定位，定位到该行的标题内容，作为表格参数名，截取到第一个句号为止
    def formName(self, pdfForm):
        pdfRows = self.newpdfText
        formCS = ""
        # 表格首行数据
        row = pdfForm[0]
        # 表格单元格
        formNum = 0
        for pdfRow in pdfRows:
            j = 0
            for cell in row:
                if cell != None:
                    if cell in pdfRow[2]:
                        j += 1
                if j == 3:
                    print("表格所在行为：", pdfRow)
                    break
            if j > 2:
                formNameRow = pdfRow
                (formName, word) = self.ruleName(formNameRow[2])
                formCS = self.formCS(formName, formNameRow, word, pdfForm)
                formNum += 1
                formCS["id"] = "formCS%s" % formNum
                return formCS

    # 获取表格参数名,rule已匹配情况下
    def ruleName(self, row):
        formWords = self.formKeyword
        formName = "unknown"
        word = ""
        row = re.split('\s', row)
        for word in formWords:
            if word in row[0]:
                formName = word
                print("formName", word)
                return formName, word
        return formName, word

        # 正则提取名称，效果不理想，难以精准
        # row = re.split('\s', row)
        # print("row", row)
        # rp = re.compile('(.+)%s' % word)
        # newName = rp.findall(row[0])
        # print(newName)
        # 判断是否为中文，不精准
        # for s in row[0]:
        #     if s != "":
        #         if '\u4e00' <= s <= '\u9fa5':
        #             ruleName = ruleName + s
        #     else:
        #         break
        # print(ruleName)
        # return ruleName

    # 构造参数格式：cs = {id,name,type,lastType,keyWord,re,default,value,oldrowID,rowID,rowData}
    def formCS(self,formName, formNameRow, word, pdfForm):
        formCS = {}
        formCS["id"] = ""
        formCS["name"] = formName
        formCS["type"] = "表格"
        formCS["lastType"] = ""
        formCS["keyWord"] = word
        formCS["re"] = ""
        formCS["default"] = ""
        formCS["value"] = [pdfForm]
        formCS["oldrowID"] = [formNameRow[0]]
        formCS["rowID"] = [formNameRow[1]]
        formCS["rowData"] = [formNameRow[2]]
        print(formCS)
        return formCS

# 测试
# f = "F:\\项目代码\\Python代码\\CBIM设计说明文档识别\\PDFCollect\\resources\\pdf文本\\崇礼度假区\\崇礼度假区（建筑单专业） H建施-001 - 设计说明及图纸目录.pdf"
# pdfPath = f
# pdfText = docPDF(pdfPath).getpdfminer()
# newpdfText = judgePDF(pdfText).newpdfText
# formCS(pdfPath, newpdfText)