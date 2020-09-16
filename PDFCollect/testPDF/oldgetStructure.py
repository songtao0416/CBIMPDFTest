from PDFCollect.recognizePDF.docPDF import docPDF
from PDFCollect.config.configPDF import configPDF
import re

"""
    提取pdf文本中的模板结构
    输入：pdfText = [rowID, data]
    传出：titleList = [{titleID,titleName，titlePid, titleLV, titleText}]
"""


class getStructure:

    def __init__(self, pdfText):
        self.titleNames = configPDF().titleNames
        self.pdfText = self.pdfHandle(pdfText)
        self.firstTitleIndex = self.judgeFirstTitle()
        self.fTitleList = self.getTitle()
        self.firstTitleList = self.getTitleDict()
        self.otherTitleList = self.otherTitleIndex()
        self.pdfTitleList = self.firstTitleList + self.otherTitleList

    # 将PDF片段处理为单独行
    def pdfHandle(self,pdfText):
        pdfText = pdfText
        newpdfText = []
        i = 1
        for pt in pdfText:
            pt = re.split('\n', pt)
            for tt in pt:
                if len(tt) >= 2:
                    newpdfText.append([i, tt])
                    i += 1
        print(newpdfText)
        return newpdfText

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
    def judgeFirstTitle(self):
        pdfText = self.pdfText
        firstTitleIndexs = ["", "一", "一.", "一、", "1", "1.", "1、"]
        # 获取pdf总标题
        if pdfText[0][1] == configPDF().pdfName:
            pdfName = pdfText[0]
            print("pdfName", pdfName)
        # 判断一级标题的index，默认第2行为一级标题
        firstTitle = pdfText[1][1]
        print("firstTitle", firstTitle)
        firstTitleIndex = 0
        for i in range(1,len(firstTitleIndexs)):
            fti = firstTitleIndexs[i]
            # 需区分”一“和”一、“,遍历即可
            if fti in firstTitle:
                firstTitleIndex = i
        print("一级标题的格式为：", firstTitleIndexs[firstTitleIndex])
        return firstTitleIndex


    # 按照标题层级，获取所有一级标题所在行数
    # 输出：titleList = {titleID,titleName，titlePid, titleLV, titleText}
    def getTitle(self):
        tIndex = self.firstTitleIndex
        pdfText = self.pdfText
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
        print(fTitleList)
        return fTitleList


    # 根据定位的一级标题，获取标题下内容,fTitleList = [id,data]
    def getTitleDict(self):
        fTitleList = self.fTitleList
        pdfText = self.pdfText
        titleList = []
        for i in range(0, len(fTitleList)):
            titleDict = {}
            if i < len(fTitleList)-1:
                indexStart = fTitleList[i][0]-1
                indexEnd = fTitleList[i+1][0]-1
                titleContext = []
                for j in range(indexStart, indexEnd):
                    titleContext.append(pdfText[j])
            else:
                titleContext = []
                for j in range(fTitleList[i][0]-1, len(pdfText)):
                    titleContext.append(pdfText[j])
            titleDict["titeleID"] = i+1
            titleDict["titeleName"] = fTitleList[i][1]
            titleDict["titelePid"] = fTitleList[i][0]
            titleDict["titeleLV"] = 1
            titleDict["titeleText"] = titleContext
            print(titleDict)
            titleList.append(titleDict)
        return titleList

    # 获取二级标题的结构，返回[{titleID,titleName，titlePid, titleLV, titleText}]
    # 获取二级标题的index
    def otherTitleIndex(self):
        pdfText = self.pdfText
        otherTitleIndexs = ["1", "1.", "1、", "a)", "1)", "1.1", "(1)"]
        # 判断一级标题的index，默认第3行为一级标题
        firstTitle = pdfText[2][1]
        print("firstTitle", firstTitle)
        otherTitleIndex = 0
        for i in range(1, len(otherTitleIndexs)):
            fti = otherTitleIndexs[i]
            if fti in firstTitle:
                otherTitleIndex = i
        print("二级标题的格式为：", otherTitleIndexs[otherTitleIndex])
        otherList = self.otherTitleLine(otherTitleIndex)
        titleList = self.otherTitleCon(otherList)
        return titleList

    # 根据二级标题的index，遍历获取所有二级标题的line
    def otherTitleLine(self, tIndex):
        pdfText = self.pdfText
        otherList = []
        otherTitleIndexs = ["1", "1.", "1、", "a.", "a)", "1)", "1.1", "(1)"]
        otherTitleRES = [r'\d+[^.、)]\w+', r'\d+\.\D\w+', r'\d+\、\D\w+', r'[a-z]\.\W\w+', r'[a-z]\)\W\w+',
                         r'\d+\)\D\w+', r'\d+\.\d+[^.、)]\w+', r'[(（]\d+[)）].+']
        # 遍历所有行数，判断长度，判断字符，匹配预定义标题，分割内容
        for pt in pdfText:
            ptstr = pt[1]
            # 去掉：，举例【1.设计委托合同：《崇礼太舞四季文化旅游度假区一期工程第一部分项目设计合同》】
            ptstr = re.split(r'[:：(（]', ptstr)[0]
            # if len(ptstr) <= 9:
            titleRE = otherTitleRES[tIndex]
            ptMatch = re.match(titleRE, ptstr)
            if ptMatch != None:
                tName = ptMatch.group()
                print(tName)
                otherList.append([pt[0], tName])
        print(otherList)
        return otherList

    # 获取二级标题下的con
    def otherTitleCon(self, otherList):
        pdfText = self.pdfText
        titleList = []
        for i in range(0, len(otherList)):
            titleDict = {}
            if i < len(otherList) - 1:
                indexStart = otherList[i][0]-1
                indexEnd = otherList[i + 1][0]-1
                titleContext = []
                for j in range(indexStart, indexEnd):
                    # 排除一级标题重复加入
                    tc = pdfText[j]
                    judgeOT = self.judgeOT(tc[0])
                    # print(judgeOT)
                    if judgeOT != 2:
                        titleContext.append(tc)
            else:
                titleContext = []
                for j in range(otherList[i][0]-1, len(pdfText)):
                    # 排除一级标题重复加入
                    tc = pdfText[j]
                    judgeOT = self.judgeOT(tc[0])
                    if judgeOT != 2:
                        titleContext.append(tc)
            titleDict["titeleID"] = i + 1
            titleDict["titeleName"] = otherList[i][1]
            titleDict["titelePid"] = otherList[i][0]
            titleDict["titeleLV"] = 2
            titleDict["titeleText"] = titleContext
            print(titleDict)
            titleList.append(titleDict)
        return titleList

    # 判断一去除标题
    def judgeOT(self, twoID):
        judgeOT = 0
        for fn in self.fTitleList:
            firstID = fn[0]
            if twoID == firstID:
                judgeOT = 2
                break
            else:
                judgeOT = 1
        return judgeOT






# # 测试
# pdfPath = "F:\\项目代码\\Python代码\\CBIM设计说明文档识别\\PDFCollect\\resources\\pdf文本\\崇礼度假区\\崇礼度假区（建筑单专业） F建施-001 - 设计说明及图纸目录.pdf"
# pdfText = docPDF(pdfPath).pdfText
# getStructure(pdfText)