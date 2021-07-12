import re
from serverPDF.saveTXT import saveTxt
from config.configPDF import configPDF

"""
    目的：量化PDF识别算法的性能
    评价指标：9个
            变量                     量化指标	     计算公式
            csrowNumRate            参数行比率	 = 参数行数量/PDF总行数
            uncsrowNumRate          非参数行比率	 = 非参数行检出率/PDF总行数
            ruleCSJCRate            参数检准率	 = 检出的参数库参数数量 / PDF中全部参数库参数数量
            ruleCSJQRate            参数检全率	 = 检出的参数库参数数量 / 全部检出的参数数量
            ruleCSF1                参数检出F1值	 = 2*参数检准率*参数检全率 /（参数检出率+参数检准率）
            ruleCSJZRate            参数值精准率	 = 检出精准参数值数量 / 全部检出参数库参数数量
            newCSNumRate            新参数占比率	 = 新参数的数量 / 所有提取参数的数量
            formCSJZRate            表格参数检准率	 = 检出的表格参数中参数库参数数量/表格中全部参数库参数数量
            formCSJQRate            表格参数检全率	 = 检出的表格参数中参数库参数数量/表格中全部参数数量
    输入：indexDict =indexDict = {pdfRowNum, H1Num, H2Num, ruleCSNum, ruleCSRowNum, formRowNum, formNum, formCSNum, 
                                newCSNum, rightCSNum, unCSRowNum, formRuleCSNum}
    输出：
        txt格式
"""

class evaluationIndex:

    def __init__(self, indexDict, pdfName):
        self.indexDict = indexDict
        print(indexDict)
        self.pdfName = pdfName
        self.evaluationIndexTitle = configPDF().evaluationIndex
        self.evaluationIndexList = self.csIndex()
        self.saveIndex2TXT()

    # 计算参数相关评价指标
    def csIndex(self):
        allCSNum = self.indexDict["ruleCSNum"]+self.indexDict["formCSNum"]+self.indexDict["newCSNum"]+self.indexDict["rightCSNum"]
        ruleCSNum = self.indexDict["ruleCSNum"] + self.indexDict["formRuleCSNum"]
        # 计算评价指标
        csrowNumRate = self.indexDict["ruleCSNum"]/self.indexDict["pdfRowNum"]
        uncsrowNumRate = self.indexDict["unCSRowNum"]/self.indexDict["pdfRowNum"]
        ruleCSJCRate = ruleCSNum /ruleCSNum
        ruleCSJQRate = ruleCSNum /allCSNum
        ruleCSF1 = 2*ruleCSJCRate*ruleCSJQRate/(ruleCSJCRate+ruleCSJQRate)
        ruleCSJZRate = ruleCSNum/ruleCSNum
        newCSNumRate = self.indexDict["newCSNum"]/allCSNum
        formCSJZRate = self.indexDict["formRuleCSNum"]/ruleCSNum
        formCSJQRate = self.indexDict["formRuleCSNum"]/allCSNum
        evaluationIndexList = ["指标值", csrowNumRate, uncsrowNumRate, ruleCSJCRate, ruleCSJQRate, ruleCSF1, ruleCSJZRate,
                               newCSNumRate, formCSJZRate, formCSJQRate]
        return evaluationIndexList

    # 存入txt
    def saveIndex2TXT(self):
        fileName = "pdfIndex_" + self.pdfName
        valueList = self.evaluationIndexList
        dataList = []
        # 构造每行文本
        for i in range(0,len(self.evaluationIndexTitle)):
            indexTitle = self.evaluationIndexTitle[i]
            indexTitle.insert(1, str(valueList[i]))
            dataList.append('         '.join(indexTitle))
        saveTxt(fileName, dataList)