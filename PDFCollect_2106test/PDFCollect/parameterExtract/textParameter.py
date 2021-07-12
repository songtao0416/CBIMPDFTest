import re

"""
    判断数值型参数，通过参数的type判断
    对数值类参数值进行正则处理
    输入：pdf行数据：pd=rowdata
    输出：正则处理后的数值
"""

class textCS:

    def __init__(self, pd, patter):
        self.pdfData = pd
        self.rePatter = patter
        self.csValue = self.textRE()

    def textRE(self):
        rp = re.compile(self.rePatter)
        textValues = rp.findall(self.pdfData)
        textValues = list(filter(None, textValues))
        textValue = ""
        for t in textValues:
            if t != "":
                textValue = t
                break
        return textValue

# 测试
# numberCS("3.建设单位：崇礼县太舞旅游度假有限公司", '[:|：|为|是](.*)')