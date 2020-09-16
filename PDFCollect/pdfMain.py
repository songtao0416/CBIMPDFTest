import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from PDFCollect.serverPDF.readFile import readFile
from PDFCollect.recognizePDF.docPDF import docPDF
from PDFCollect.recognizePDF.judgePDF import judgePDF
from PDFCollect.parameterExtract.allParameter import allCSHandle
from PDFCollect.parameterExtract.newParameter import newParameter
from PDFCollect.serverPDF.saveTXT import saveTxt
from PDFCollect.serverPDF.saveExcel import saveExcel
from PDFCollect.parameterExtract.rightFormCS import rightForm
from PDFCollect.parameterExtract.formParameter import formCS
import time
from PDFCollect.recognizePDF.firstTitle import getfirstTitle
from PDFCollect.recognizePDF.otherTitle import getotherTitle
from PDFCollect.recognizePDF.formPDF import formPDF
from PDFCollect.serverPDF.tagMould import tagMould
from PDFCollect.serverPDF.evaluationIndex import evaluationIndex

"""
    测试:单个PDF文档的解析效果
    建议使用pdfplumber扩展包来解析PDF文档的文本和表格
    如果只解析文本内容，也可以使用pdfminer 
    而解析英文文档内容，可以使用PyPDF2
"""

def getPDF():
    print("*" * 10, "读取PDF数据", "*" * 10)
    pdfText = docPDF(pdfPath).pdfText
    print("*" * 10, "处理PDF数据", "*" * 10)
    allpdfText, ftitleList, formRows, cspdfText = judgePDF(pdfText).pdfTitleText
    return allpdfText, ftitleList, formRows, cspdfText

def getTitle(nnewpdfText, ftitleList):
    # 获取一级标题结构和二级标题结构
    print("*" * 10, "获取一级标题结构和二级标题结构", "*" * 10)
    firsttitleList = getfirstTitle().getTitleDict(nnewpdfText, ftitleList)
    othertitleList = getotherTitle(nnewpdfText, ftitleList, firsttitleList).othertitleList
    return firsttitleList, othertitleList

def getParameter(newpdfText, formRows, othertitleList):
    forms = formPDF(pdfPath).forms
    formList = forms[0]
    rightformList = forms[1]
    print("*" * 10, "表格提取", "*" * 10)
    formCSList = formCS(formRows, formList).formCSList
    print("*" * 10, "右侧明细表中参数提取", "*" * 10)
    rightCSList = rightForm(rightformList).rightCSList
    print("*" * 10, "参数库对应参数提取", "*" * 10)
    csList, unPdfs = allCSHandle(newpdfText, othertitleList).csLists
    print("*" * 10, "新参数提取", "*" * 10)
    newCSList = newParameter(unPdfs).newCSList
    # print("*" * 10, "整合所有参数", "*" * 10)
    getCSList = csList + newCSList + formCSList + rightCSList
    return getCSList, formList

def savePDF(newpdfText, getCSList, titleList):
    print("*" * 10, "读取结果存入txt", "*" * 10)
    saveTxt("识别PDF_%s" % pdfName, newpdfText)
    print("*" * 10, "爬取结果存入excel", "*" * 10)
    saveExcel("提取参数_%s" % pdfName, getCSList, type=1)
    saveExcel("提取结构_%s" % pdfName, titleList, type=2)

if __name__ == '__main__':
    fileList = readFile().fileList
    fileNames = readFile().fileNames

    # todo 对照testMain完善此处
    for i in range(0, len(fileList)):
        pdfPath = fileList[i]
        pdfName = fileNames[i]

        # 识别PDF
        (allpdfText, ftitleList, formRows, cspdfText) = getPDF()

        # 提取框架
        (firsttitleList, othertitleList) = getTitle(allpdfText, ftitleList)
        titleList = firsttitleList + othertitleList

        # 提取参数
        getCSList, formList = getParameter(cspdfText, formRows, othertitleList)

        # 保存数据
        savePDF(allpdfText, getCSList, titleList)

        # 复现PDF文档
        indexDict = tagMould(getCSList, titleList, pdfName, formList, formRows).indexDict

        # 计算量化指标
        evaluationIndex(indexDict,pdfName)

        print("*" * 10, "已完成，正在待机ing, 100s", "*" * 10)
        time.sleep(5)