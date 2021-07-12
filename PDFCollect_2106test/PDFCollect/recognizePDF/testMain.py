import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
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
from serverPDF.tagMould import tagMould
from serverPDF.evaluationIndex import evaluationIndex

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
    # 接口，json格式
    apiJson ={"newpdfText": newParameter, "getCSlist": getCSList, "titleList":titleList}


if __name__ == '__main__':

    pdfName = "崇礼度假区（建筑单专业） K建施-001 - 设计说明及图纸目录.pdf"
    pdfPath = "F:\\项目代码\\Python代码\\CBIM设计说明文档识别\\PDFCollect\\resources\\pdf文本\\崇礼度假区\\%s" % pdfName
    # "F:\\项目代码\\Python代码\\CBIM设计说明文档识别\\PDFCollect\\resources\\pdf文本\\崇礼度假区\\崇礼度假区（建筑单专业） K建施-001 - 设计说明及图纸目录.pdf"

    # 识别PDF
    (allpdfText, ftitleList, formRows, cspdfText) = getPDF()

    # 提取框架
    (firsttitleList, othertitleList) = getTitle(allpdfText, ftitleList)
    titleList = firsttitleList + othertitleList

    # 提取参数
    getCSList, formList = getParameter(cspdfText, formRows, othertitleList)

    # 保存数据
    # savePDF(allpdfText, getCSList, titleList)

    # 复现PDF文档
    indexDict = tagMould(getCSList, titleList, pdfName, formList, formRows).indexDict

    # 计算量化指标
    evaluationIndex(indexDict,pdfName)

    print("*" * 10, "已完成，正在待机ing, 100s", "*" * 10)
    time.sleep(100)