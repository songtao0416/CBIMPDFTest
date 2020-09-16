import os
from config.configPDF import configPDF
"""
    保存为txt格式
"""

class saveTxt:

    def __init__(self, fileName, dataList):
        self.dataList = dataList
        self.path = configPDF().txtPath + "\\%s.txt" % fileName
        self.savetxt()

    def savetxt(self):
        with open(self.path, "w") as f:
            for da in self.dataList:
                print(da)
                f.write(str(da)+"\n")


