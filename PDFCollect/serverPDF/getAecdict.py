import os
import re
from config.configPDF import configPDF
import sys

"""
    获取aecuserdict中的词典list
"""

class getAecdict:

    def __init__(self):
        self.dictPath = configPDF().aecdictPath
        self.aecDict = self.openTxt()

    def openTxt(self):
        aecDict = []
        # 当我们读取的文件或者写入文件时有时候会出现"\ufeff"非法字符，这个时候需要改变编码方式‘UTF-8‘为‘UTF-8-sig‘：
        with open(self.dictPath, encoding='utf-8') as f:
            data = f.readlines()
            for d in data:
                nd = re.sub('\s','',d)
                if len(nd) >= 2:
                    aecDict.append(nd)
        aecList = self.reText(aecDict)
        # print(aecDict)
        # print(len(aecList), len(aecDict))
        return aecDict

    # 处理词典，去掉空值，去重
    def reText(self, aecDIct):
        newaecDict = list(set(aecDIct))
        newaecDict.sort(key=aecDIct.index)
        return newaecDict

# getAecdict()