import re

"""
    判断是否包含规范参数，通过《》判断
    对规范类参数值进行正则处理
    输入：pd = rowdata
         keyword = str
    输出：gfValue = []
"""

class gfRE:

    def __init__(self, pd, keyWord):
        self.pdfData = pd
        self.keyWord = re.split(r'&', keyWord)[0]
        self.gfValue = self.csJudge()

    # 判断是否包含规范文本，true则返回提取值，false则返回空值
    def csJudge(self):
        gfValue = []
        rowData = self.pdfData
        if "《" in rowData:
            if "》" in rowData:
                gfValue = self.gfCS(rowData)
        # 非《》的规范
        elif "（" in rowData:
            newrowData = re.sub(r'(\d.)', '', rowData)
            nd = re.search(r'[（(].+?[）)]', rowData)
            if nd != None:
                newrowData = nd.group()
            gfValue = [newrowData]
        return gfValue

    # True，则获取规范参数值《》+
    # todo 规范提取正则需优化
    # 优化：多个匹配正确的参数时，返回list
    def gfCS(self, data):
        # da = re.sub(r'\（', '', data)
        # db = re.findall(r'(《.*?》[\x00-\xff]*)', da)
        db = re.findall(r'(《.*?》[(（\x00-\xff）)-—]*)', data)
        newData = []
        if len(db) > 0:
            # print(data)
            for reData in db:
                if self.keyWord in reData:
                    newData.append(reData)
        return newData

# pd = "1)本工程防火设计执行《建筑设计防火规范》（GB 50016—2006）的、《建筑内部装修设计防火规范》（GB 50222—95）、《汽车库、修车库、停车场设计防火规范》（GB 50067-97）等"
# keyWord = "防火&《"
# pd = "《建筑幕墙》GB/T 21086—2007 "
# keyWord = "幕墙"
# gfRE(pd, keyWord)

