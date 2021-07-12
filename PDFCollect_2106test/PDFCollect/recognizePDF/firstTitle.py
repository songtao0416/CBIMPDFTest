from recognizePDF.docPDF import docPDF
from config.configPDF import configPDF
import re

"""
    提取pdf文本中的模板结构
    输入：pdfText = [[rowID, data]]  未拼接
    输出：
        self.judgeFirstTitle():
            输入：无
            输出：fTitleList = [[rowid,title],[]]
        self.firstTitleList（）：
            输入：newpdfText = [[rowID, data]]
                 fTitleList = [[rowid,title],[]]
            输出：titleList = [{titleID,titleName，titlePid, titleLV, titleText}]
"""


class getfirstTitle:

    def __init__(self):
        self.titleNames = configPDF().titleNames
        # self.firstTitleIndex = self.judgeFirstTitle()   # firstTitleIndex = 1
        # self.fTitleList = self.getTitle()   # fTitleList = [[rowid,title],[]]
        # self.firstTitleList = self.getTitleDict()   # titleList = [{titleID,titleName，titlePid, titleLV, titleText}]


    """
        # 遍历文本，获取所有类型的标题格式，判断标题层级
        # 先验知识：哪些标题格式，一一匹配
        # 存在非数字标识的标题，关键词识别
    一级标题格式识别：
        一级标题可能有index，可能无index
            NO:直接根据预定义的一级标题获取所有一级标题不可行，因为可能在pdf中为二级标题，然后被获取；
            根据预定义格式，判断第一级标题的格式；再获取所有一级标题；
    多级标题识别：
        NO:多级标题都有index，可以按预定义的序号list，顺序读取;
        不需要识别多级标题，只需要切分一级标题，其它各级桉行数识别即可，拼接行；
    """
    # 获取一级标题的index
    def judgeFirstTitle(self, pdfText):
        firstTitleIndexs = ["", "一", "一.", "一、", "1", "1.", "1、"]
        # 获取pdf总标题
        if pdfText[0][1] == configPDF().pdfName:
            pdfName = pdfText[0]
            print("预定义的pdfName", pdfName)
        else:
            print("读取的pdfName", pdfText[0][1])
        # 判断一级标题的index，默认第2行为一级标题
        firstTitle = pdfText[1][1]
        print("第一个firstTitle：", firstTitle)
        firstTitleIndex = 0
        for i in range(1,len(firstTitleIndexs)):
            fti = firstTitleIndexs[i]
            # 需区分”一“和”一、“,遍历即可
            if fti in firstTitle:
                firstTitleIndex = i
        print("一级标题的格式为：", firstTitleIndexs[firstTitleIndex])
        ftitleList = self.getTitle(firstTitleIndex, pdfText)
        return ftitleList


    # 按照标题层级，获取所有一级标题所在行数
    # 输出：titleList = {titleID,titleName，titlePid, titleLV, titleText}
    def getTitle(self, firstTitleIndex, pdfText):
        tIndex = firstTitleIndex
        firstTitleIndexs = ["", "一", "一.", "一、", "1", "1.", "1、"]
        firstTitleRES = ["", r'[一二三四五六七八九十](.+)', r'[一二三四五六七八九十](.+)', r'[一二三四五六七八九十](.+)',
                    r'\d+[^.)）、]\w+', r'\d+\.\D\w+', r'\d+\、\D\w+']
        fTitleList = []
        # 遍历所有行数，判断长度，判断字符，匹配预定义标题，分割内容
        for pt in pdfText:
            ptstr = pt[1]
            if len(ptstr) <= 9:
                # 分割无index的一级标题
                if tIndex == 0:
                    if u'\u4e00' <= ptstr <= u'\u9fff':
                        for tname in self.titleNames:
                            if tname == ptstr:
                                fTitleList.append(pt)
                else:
                    # 分割有index的一级标题
                    titleRE = firstTitleRES[tIndex]
                    ptMatch = re.match(titleRE, ptstr)
                    if ptMatch != None:
                        tName = ptMatch.group()
                        fTitleList.append(pt)
        print("fTitleList", fTitleList)
        return fTitleList


    # 根据定位的一级标题，获取标题下内容,fTitleList = [id,data]
    def getTitleDict(self, newpdfText, fTitleList):
        pdfText = newpdfText
        titleList = []
        for i in range(0, len(fTitleList)):
            titleDict = {}
            if i < len(fTitleList)-1:
                indexStart = fTitleList[i][0]-1
                indexEnd = fTitleList[i+1][0]-1
                titleContext = []
                # todo bug,表格多行，导致标题结构提取出错，应修改为判断其行号
                for pd in pdfText:
                    if indexStart < pd[0] <= indexEnd:
                        titleContext.append(pd)
                # for j in range(indexStart, indexEnd):
                #     titleContext.append(pdfText[j])
            else:
                titleContext = []
                for pd in pdfText:
                    if fTitleList[i][0]-1 < pd[0] <= len(pdfText):
                        titleContext.append(pd)
                # for j in range(fTitleList[i][0]-1, len(pdfText)):
                #     titleContext.append(pdfText[j])
            titleDict["titleID"] = i+1
            titleDict["ftID"] = 0
            titleDict["titleName"] = fTitleList[i][1]
            titleDict["titlePid"] = fTitleList[i][0]
            titleDict["titleLV"] = 1
            titleDict["titleText"] = titleContext
            titleList.append(titleDict)
        print("*" * 10, "一级标题结构", "*" * 10)
        for t in titleList:
            print(t)
        return titleList







# # 测试
# pdfPath = "F:\\项目代码\\Python代码\\CBIM设计说明文档识别\\PDFCollect\\resources\\pdf文本\\崇礼度假区\\崇礼度假区（建筑单专业） F建施-001 - 设计说明及图纸目录.pdf"
# pdfText = docPDF(pdfPath).pdfText
# getStructure(pdfText)