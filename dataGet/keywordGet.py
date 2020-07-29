from configCBIM.fileConfig import fileConfig
import xlrd


class keyWordGet:
    """
    功能：获取参数对应的关键词抽取规则和正则抽取规则
    逻辑：
    返回结果：[{'parameID': 1.0, 'parameName': '市规划国土函', 'parameType': '文本', 'parameUnitType': 3.0, 'parameKeyword': '市规划局||国土函', 'parameRE': '《(.*?)》'}]
    """
    def __init__(self):
        self.file = fileConfig().keywordAddress["keyWord"]
        self.data = self.openXlsx()
        self.cutRuleList = self.readXlsx()

    def openXlsx(self):
        data = xlrd.open_workbook(self.file)
        return data

    # 获取excel中的抽取规则，关键词+正则
    def readXlsx(self):
        tableKeyword = self.data.sheet_by_index(3)
        cutRuleList = []
        print(tableKeyword.ncols)
        print(tableKeyword.nrows)
        for i in range(1, tableKeyword.nrows):
        # for i in range(1, 100):
            parameID = tableKeyword.col_values(0)[i]
            parameName = tableKeyword.col_values(1)[i]
            parameType = tableKeyword.col_values(2)[i]
            parameUnitType = tableKeyword.col_values(3)[i]
            parameKeyword = tableKeyword.col_values(4)[i]
            parameRE = tableKeyword.col_values(5)[i]
            cutRule = dict(parameID=parameID, parameName=parameName, parameType=parameType, parameUnitType=parameUnitType,
                           parameKeyword=parameKeyword, parameRE=parameRE)
            cutRuleList.append(cutRule)
        print(cutRuleList)
        return cutRuleList

# keyWordGet()

