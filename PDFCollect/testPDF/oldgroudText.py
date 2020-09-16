import re

"""
    获取参数的上下文信息，为固定字段
    输入：参数值，参数所在行，全部参数
    输出：参数上下文, str
"""


class getgroudText:

    def __init__(self, csValue, rowData):
        self.csValue = csValue
        self.rowData = rowData
        self.lastText, self.nextText = self.getText()
        self.groudText = (self.lastText, self.nextText)

    # 提取参数的上下文,行数据去掉参数值，即得到参数上下文
    # 优化：需读取完所有参数后，针对每一行定位参数，以参数为界限提取上下文
    # todo 目前上下文提取模糊，未解决同一行多个参数时，参数的上下文包含其他参数
    def getText(self):
        (rowData, csValue) = self.rowData, self.csValue
        lenRow = len(rowData)
        lenCS = len(csValue)
        # 确定参数在rowData中的index
        csIndex = rowData.find(str(csValue))
        lastText = rowData[0:csIndex]
        nextText = rowData[csIndex + lenCS:lenRow]
        return lastText, nextText

# rowData = "1)本工程防火设计执行《建筑设计防火规范》（GB 50016—2006）、《建筑内部装修设计防火规范》（GB 50222—95）、《汽车库、修车库、停车场设计防火规范》（GB 50067-97）" \
#           "等现行国家规范的要求。"
# csValue = "《建筑内部装修设计防火规范》（GB 50222—95）"
# (lastText,nextText) = getgroudText(csValue, rowData).groudText
#
# print("上下文复现", lastText + "【" + csValue + "】" + nextText)