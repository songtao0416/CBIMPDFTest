from recognizePDF.docPDF import docPDF
from config.configPDF import configPDF
import re

"""
    提取pdf文本中的模板结构
    输入：pdfText = [rowID, data]
         ftitleList = [[rowid,title],[]]
         titleList = [{titleID,ftID,titleName，titlePid, titleLV, titleText},{}]
    传出：titleList = [{titleID,titleName，titlePid, titleLV, titleText}]
"""


class getotherTitle:

    def __init__(self, pdfText, fTitleList, firsttitleList):
        self.pdfText = pdfText
        self.fTitleList = fTitleList
        self.fathertitleList = firsttitleList
        self.otherTitleIndex = self.otherTitleIndex()
        self.otherList = self.otherTitleLine()
        self.othertitleList = self.otherTitleCon()


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

    # 获取二级标题的结构，返回[{titleID,titleName，titlePid, titleLV, titleText}]
    # 获取二级标题的index
    def otherTitleIndex(self):
        pdfText = self.pdfText
        otherTitleIndexs = ["1", "1.", "1、", "a)", "1)", "1.1", "(1)"]
        # 判断一级标题的index，默认第3行为一级标题
        firstTitle = pdfText[2][1]
        print("firstTitle", firstTitle)
        otherTitleIndex = 0
        for i in range(0, len(otherTitleIndexs)):
            fti = otherTitleIndexs[i]
            if fti in firstTitle:
                otherTitleIndex = i
        print("二级标题的格式为：", otherTitleIndexs[otherTitleIndex])
        return otherTitleIndex

    # 根据二级标题的index，遍历获取所有二级标题的line
    def otherTitleLine(self):
        pdfText = self.pdfText
        tIndex = self.otherTitleIndex
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
            # print("ptstr", ptstr, titleRE)
            if ptMatch != None:
                tName = ptMatch.group()
                print(tName)
                otherList.append([pt[0], tName])
        print(otherList)
        return otherList

    # 获取二级标题下的con
    def otherTitleCon(self):
        pdfText = self.pdfText
        otherList = self.otherList
        titleList = []
        for i in range(0, len(otherList)):
            titleDict = {}
            if i < len(otherList) - 1:
                indexStart = otherList[i][0]-1
                indexEnd = otherList[i + 1][0]-1
                titleContext = []
                for pd in pdfText:
                    if indexStart < pd[0] <= indexEnd:
                        # 排除一级标题重复加入
                        tc = pd
                        judgeOT = self.judgeOT(tc[0])
                        # print(judgeOT)
                        if judgeOT != 2:
                            titleContext.append(tc)
            else:
                titleContext = []
                for pd in pdfText:
                    if otherList[i][0] - 1 < pd[0] <= len(pdfText):
                        # 排除一级标题重复加入
                        tc = pd
                        judgeOT = self.judgeOT(tc[0])
                        if judgeOT != 2:
                            titleContext.append(tc)
            titleDict["titleID"] = i + 1
            titleDict["ftID"] = self.getFatherTitleID(otherList[i][0])
            titleDict["titleName"] = otherList[i][1]
            titleDict["titlePid"] = otherList[i][0]
            titleDict["titleLV"] = 2
            titleDict["titleText"] = titleContext
            titleList.append(titleDict)
        print("*" * 10, "二级标题结构", "*" * 10)
        for t in titleList:
            print(t)
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

    # 获取父级标题的titleID
    def getFatherTitleID(self, rowID):
        fatherTitles = self.fathertitleList
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