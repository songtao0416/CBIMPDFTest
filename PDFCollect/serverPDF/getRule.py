import xlrd
from config.configPDF import configPDF

"""
    读取excel中的参数提取规则
    按五种一级单元进行存储
    输入：参数库规则excel表的path
         sheet：参数ID	参数父级模块	参数名称	参数类型	关键词	正则表达式	取值范围	参数默认值	备注 	是否对应校验规则
    输出：self.ruleDatas，self.gfRules, self.textRules, self.numRules, self.formRules, self.imgRules
        =[{id,name,type,lastType,keyWord,re,default},{}]
"""
class getRule:
    # todo 修改读取字段，已优化参数xlsx表
    def __init__(self):
        self.rulePath = configPDF().rulePath
        self.sheetIndex = configPDF().rulesheetIndex
        self.ruleDatas = self.openXls()

    # 获取excle中的关键词列，包括四种单元的关键词
    def openXls(self):
        ruleDatas = []
        xlsData = xlrd.open_workbook(self.rulePath)
        keyTable = xlsData.sheet_by_index(self.sheetIndex)
        # 获取各行数据
        ruleRows = keyTable.nrows
        for i in range(1, ruleRows):
            ruleDict = {}
            # print(type(keyTable.cell_value(i, 1)))
            ruleDict["id"] = str(int(keyTable.cell_value(i, 0)))
            # print(keyTable.cell_value(i, 0))
            ruleDict["name"] = str(keyTable.cell_value(i, 2))
            ruleDict["type"] = str(keyTable.cell_value(i, 3))
            ruleDict["lastType"] = str(keyTable.cell_value(i, 1))
            ruleDict["keyWord"] = str(keyTable.cell_value(i, 4))
            ruleDict["re"] = str(keyTable.cell_value(i, 5))
            ruleDict["default"] = str(keyTable.cell_value(i, 7))
            ruleDatas.append(ruleDict)
            # print(ruleDict)
        print("ruleDatas:", ruleDatas)
        return ruleDatas


# getRule()



