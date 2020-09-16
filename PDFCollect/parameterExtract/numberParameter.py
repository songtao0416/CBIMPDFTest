import re

"""
    判断数值型参数，通过参数的type判断
    对数值类参数值进行正则处理
    输入：pdf行数据：pd=rowdata
    输出：正则处理后的数值
"""

class numberCS:

    def __init__(self, pd, patter):
        self.pdfData = pd
        self.rePatter = patter
        self.csValue = self.numberRE()

    def numberRE(self):
        rp = re.compile(self.rePatter)
        numberValues = rp.findall(self.pdfData)
        # 去除list中的空白项
        numberValues = list(filter(None, numberValues))
        numberValue = ""
        # 获取第一个不为空的值
        for num in numberValues:
            if num != "":
                numberValue = num
                break
        return numberValue



# 测试
# numberCS("3.建设单位：崇礼县太舞旅游度假有限公司", '[:|：|为|是](.*)')