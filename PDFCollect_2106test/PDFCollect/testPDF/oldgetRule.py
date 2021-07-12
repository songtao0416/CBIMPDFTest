import xlrd
from PDFCollect.config.configPDF import configPDF

"""
    读取excel中的参数提取规则
    按五种一级单元进行存储
    输入：参数库规则excel表的path
    输出：self.ruleDatas，self.gfRules, self.textRules, self.numRules, self.formRules, self.imgRules
        =[{id,name,type,lastType,keyWord,re,default},{}]
"""
class getRule:
    # todo 修改读取字段，已优化参数xlsx表
    def __init__(self):
        self.rulePath = configPDF().rulePath
        self.ruleDatas = self.openXls()
        (self.gfRules, self.textRules, self.numRules, self.formRules, self.imgRules) = self.firstRule()

    # 获取excle中的关键词列，包括四种单元的关键词
    def openXls(self):
        ruleDatas = []
        xlsData = xlrd.open_workbook(self.rulePath)
        keyTable = xlsData.sheet_by_index(3)
        # # 获取各列数据
        # nameCols = keyTable.col_values(1)
        # typeCols = keyTable.col_values(2)
        # lastTypeCols = keyTable.col_values(3)
        # keyCols = keyTable.col_values(4)
        # reCols = keyTable.col_values(5)
        # defaultCols = keyTable.col_values(8)
        # 获取各行数据
        ruleRows = keyTable.nrows
        for i in range(1, ruleRows):
            ruleDict = {}
            # print(type(keyTable.cell_value(i, 1)))
            ruleDict["id"] = str(int(keyTable.cell_value(i, 0)))
            ruleDict["name"] = str(keyTable.cell_value(i, 1))
            ruleDict["type"] = str(keyTable.cell_value(i, 2))
            ruleDict["lastType"] = str(keyTable.cell_value(i, 3))
            ruleDict["keyWord"] = str(keyTable.cell_value(i, 4))
            ruleDict["re"] = str(keyTable.cell_value(i, 5))
            ruleDict["default"] = str(keyTable.cell_value(i, 8))
            ruleDatas.append(ruleDict)
        print("ruleDatas:", ruleDatas)
        return ruleDatas

    # 提取各一级单元的规则信息
    def firstRule(self):
        gfRules = []
        textRules = []
        numRules = []
        formRules = []
        imgRules = []
        for i in range(0, len(self.ruleDatas)):
            ruleRow = self.ruleDatas[i]
            lastType = ruleRow["lastType"]
            if lastType == '1.0':
                textRules.append(ruleRow)
            if lastType == '2.0':
                numRules.append(ruleRow)
            if lastType == '3.0':
                gfRules.append(ruleRow)
            if lastType == '4.0':
                formRules.append(ruleRow)
            if lastType == '5.0':
                imgRules.append(ruleRow)
        # print(gfRules, textRules, numRules, formRules, imgRules)
        return gfRules, textRules, numRules, formRules, imgRules


