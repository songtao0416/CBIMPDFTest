from config.configPDF import configPDF
from serverPDF.readFile import readFile
from recognizePDF.firstTitle import getfirstTitle
from recognizePDF.otherTitle import getotherTitle
from recognizePDF.docPDF import docPDF
import re

"""
    读取pdf文档，并判断采用哪一种方式进行pdf识别
    处理pdf文本，去除空白行、去除表格文本
        暂不用去除表格，因为参数提取时可以排除掉
    处理pdf文本，识别换行并粘连，先读取一级标题所在行，去掉这些行，再拼接，再读取一级标题内容和二级标题，保证行数一致
    处理pdf文本，返回目录结构
    输入： pdfminer读取的文本
    输出： nnewpdfText = [[拼接后行数，拼接后内容]]
          self.ftitleList = 
          formRows = [[formData,rowID],[]]
"""

class judgePDF:

    def __init__(self, pdfText):
        self.pdfText = pdfText
        # 未拼接的行
        self.newpdfText = self.pdfHandle()
        # 获取一级标题所在行
        self.ftitleIndex = getfirstTitle().judgeFirstTitle(self.newpdfText)  # fTitleList = [[rowid,title],[]]
        # 获取拼接后的行，拼接后一级标题的行
        self.formRows = []
        (self.allpdfText, self.ftitleList, self.cspdfText) = self.joinRow()
        self.pdfTitleText = (self.allpdfText, self.ftitleList, self.formRows, self.cspdfText)



    """
        处理pdf文本，去除空白行
        输入：pdfText = [text]  pdf解析后的原始行
        输出：newpdfText = [[原行数，拼接后行数，拼接后内容]]
    """
    def pdfHandle(self):
        pdfText = self.pdfText
        newpdfText = []
        i = 1
        for pt in pdfText:
            pt = re.split('\n', pt)
            for tt in pt:
                if len(tt) >= 2:
                    newpdfText.append([i, tt])
                    i += 1
        print("*" * 10, "已去除空白行", "*" * 10)
        print(newpdfText)
        return newpdfText


    """
        通过识别最长长度，或最高频次长度确定换行，结果不理想
        通过确定字符串开头的数字/字母标识确定换行，结果不理想
        通过正则判断每行起始位，进行拼接
            先识别一级标题，再拼接，再识别二级标题
        输入：pdf【行数，内容】
        输出：【原行数，拼接后行数，拼接后内容】
    """
    #  拼接行已完成
    def joinRow(self):
        # todo 增加句号判断结束位置，暂不需要
        newpdfText = self.newpdfText
        allpdfText = []
        cspdfText = []
        ftitleList = []
        rowID = 1
        nextTitleIndex = 0
        # 将第一行，默认为文档名称，添加到新的第一行
        allpdfText.append([rowID, newpdfText[0][1]])
        cspdfText.append([rowID, newpdfText[0][1]])
        rowID += 1
        formIndex = 0
        for i in range(0, len(newpdfText)):
            # 将一级标题筛出，并添加到nnpdfText
            for k in range(0, len(self.ftitleIndex)):
                if newpdfText[i][0] == self.ftitleIndex[k][0]:
                    allpdfText.append([rowID, newpdfText[i][1]])
                    ftitleList.append([rowID, newpdfText[i][1]])
                    rowID += 1
                    if k < len(self.ftitleIndex)-1:
                        nextTitleIndex = self.ftitleIndex[k+1][0]
                        # print(newpdfText[i][0], self.ftitleIndex[k][0], self.ftitleIndex[k+1][0])
                    break
            # 非一级标题，进行拼接
            else:
                pt = newpdfText[i][1]
                # # 遇到数字/字母的行，获取其到下一个数字字母的行为止，全部加到该行上
                # if st.isdigit() == True:
                # 通过正则识别1）
                if re.match(r'[\da-z]+[.)）、]', pt):
                    if formIndex == 1:
                        rowID += 1
                        formIndex = 0
                    if pt[2] not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
                        stRow = []
                        # 需要拼接的行一般不会超过6行，遍历接下来的6行
                        for j in range(1, 5):
                            try:
                                nextPt = newpdfText[i+j][1]
                                # 并筛除一级标题
                                if newpdfText[i+j][0] == nextTitleIndex:
                                    break
                                elif re.match(r'\d+[.)）、]', nextPt):
                                    # 避免识别2000）为新的一行，判断第三个字符为数字时，继续拼接
                                    if nextPt[2] not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
                                        break
                                elif re.match(r'[a-z][.)）]', nextPt):
                                    break
                                # 此处去掉表格
                                elif nextPt.count(' ') > 5:
                                    break
                                # print("nextpt", nextPt)
                                stRow.append(nextPt)
                            except:
                                print(1)
                        pdfRow = pt + ''.join(stRow)
                        # print("pdfRow", pdfRow)
                        allpdfText.append([rowID, pdfRow])
                        cspdfText.append([rowID, pdfRow])
                        rowID += 1
                # 并记录表格所在行,cspdfTextz中不加入表格行
                elif pt.count(' ') > 5:
                    self.formRows.append([rowID, pt])
                    allpdfText.append([rowID, pt])
                    formIndex = 1
        print("*" * 10, "已完成拼接", "*" * 10)
        for nnp in allpdfText:
            print(nnp)
        for fp in self.formRows:
            print(fp)
        return allpdfText, ftitleList, cspdfText

    # todo 通过关键词锁定特殊行，处理无法拼接的行，标题等，暂不需要
    def keyRow(self):
        pass

# # 测试
# pdfPath = "F:\\项目代码\\Python代码\\CBIM设计说明文档识别\\PDFCollect\\resources\\pdf文本\\崇礼度假区\\崇礼度假区（建筑单专业） F建施-001 - 设计说明及图纸目录.pdf"
# pdfText = docPDF(pdfPath).pdfText
# pdfText = judgePDF(pdfText)





