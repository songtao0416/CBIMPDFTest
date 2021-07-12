import re
from serverPDF.getAecdict import getAecdict


"""
    提取新参数的名称
    通过aecuserdict词典，识别关键词
    匹配词即为新名称
    输入：dataValue
    输出：参数名：newName
"""

class aecName:

    def __init__(self, pdfData, aecDict):
        self.aecDict = aecDict
        self.data = pdfData
        self.newName = self.getNewname()

    # 匹配aecDict,成功返回newName，失败则不生成新参数
    def getNewname(self):
        pdfData = self.data
        for word in self.aecDict:
            if word in pdfData:
                newName = word
                print("发现新参数-名称为", newName)
                return newName

# 测试
# aecDict = getAecdict().aecDict
# aecName("1)室内声环境", aecDict)
