import os
import sys
sys.path.append("..")
from recognizePDF.docPDF import docPDF
from recognizePDF.judgePDF import judgePDF
from parameterExtract.allParameter import allCSHandle
from parameterExtract.newParameter import newParameter
from serverPDF.saveTXT import saveTxt
from serverPDF.saveExcel import saveExcel
from parameterExtract.rightFormCS import rightForm
from parameterExtract.formParameter import formCS
import time
from recognizePDF.firstTitle import getfirstTitle
from recognizePDF.otherTitle import getotherTitle
from recognizePDF.formPDF import formPDF

"""
    测试:单个PDF文档的解析效果
    建议使用pdfplumber扩展包来解析PDF文档的文本和表格
    如果只解析文本内容，也可以使用pdfminer 
    而解析英文文档内容，可以使用PyPDF2
"""





class apiJson:

    def __init__(self, pdfPath, pdfName):
        self.pdfName = pdfName
        self.pdfPath = pdfPath

        # 识别PDF
        (allpdfText, ftitleList, formRows, cspdfText) = self.getPDF()

        # 提取框架
        (firsttitleList, othertitleList) = self.getTitle(allpdfText, ftitleList)
        titleList = firsttitleList + othertitleList

        # 提取参数
        getCSList, formList = self.getParameter(cspdfText, formRows, othertitleList)

        # 接口，json格式
        self.apiJson = {"newpdfText": allpdfText, "getCSlist": getCSList, "titleList": titleList}
        # self.apiJson = {"newpdfText": allpdfText}
        # self.apiJson = {"test": "aaa"}

        print("*" * 10, "已完成，正在待机ing, 100s", "*" * 10)

    def getPDF(self):
        print("*" * 10, "读取PDF数据", "*" * 10)
        pdfText = docPDF(self.pdfPath).pdfText
        print("*" * 10, "处理PDF数据", "*" * 10)
        allpdfText, ftitleList, formRows, cspdfText = judgePDF(pdfText).pdfTitleText
        return allpdfText, ftitleList, formRows, cspdfText

    def getTitle(self, nnewpdfText, ftitleList):
        # 获取一级标题结构和二级标题结构
        print("*" * 10, "获取一级标题结构和二级标题结构", "*" * 10)
        firsttitleList = getfirstTitle().getTitleDict(nnewpdfText, ftitleList)
        othertitleList = getotherTitle(nnewpdfText, ftitleList, firsttitleList).othertitleList
        return firsttitleList, othertitleList

    def getParameter(self, newpdfText, formRows, othertitleList):
        try:
            forms = formPDF(self.pdfPath).forms
            formList = forms[0]
            rightformList = forms[1]
            print("*" * 10, "表格提取", "*" * 10)
            formCSList = formCS(formRows, formList).formCSList
            print("*" * 10, "右侧明细表中参数提取", "*" * 10)
            rightCSList = rightForm(rightformList).rightCSList
        except:
            formList = []
            formCSList = []
            rightCSList = []
        print("*" * 10, "参数库对应参数提取", "*" * 10)
        csList, unPdfs = allCSHandle(newpdfText, othertitleList).csLists
        print("*" * 10, "新参数提取", "*" * 10)
        newCSList = newParameter(unPdfs).newCSList
        # print("*" * 10, "整合所有参数", "*" * 10)
        getCSList = csList + newCSList + formCSList + rightCSList
        return getCSList, formList


# #  测试
# pdfName = "崇礼度假区（建筑单专业） K建施-001 - 设计说明及图纸目录.pdf"
# pdfPath = "F:\\项目代码\\Python代码\\CBIM设计说明文档识别\\PDFCollect\\resources\\pdf文本\\崇礼度假区\\%s" % pdfName
# apiJson(pdfPath, pdfName)