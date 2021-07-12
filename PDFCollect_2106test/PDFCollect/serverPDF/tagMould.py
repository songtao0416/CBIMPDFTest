import re
from serverPDF.saveTXT import saveTxt

"""
    复现PDF文档
    输入：参数，结构
         titleList = [{titleID,titleName，titlePid, titleLV, titleText},{}]
         csList = [{ID,fcsID,fcsName,csName,csValue,csType,titleID,lastText,nextText,rowID,rowData}]
    输出：
         pdf模板.txt
         indexDict = {pdfRowNum, H1Num, H2Num, ruleCSNum, ruleCSRowNum, formRowNum, formNum, formCSNum, newCSNum,
                       rightCSNum, unCSRowNum, formRuleCSNum}
    
"""


class tagMould:

    def __init__(self, csList, titleList, pdfName, formList, formRows):
        self.pdfName = pdfName
        self.formList = formList
        self.formRows = formRows
        self.csList = csList
        self.titleList = titleList
        self.indexDict = self.tagParameter()

    """
        多层遍历：先遍历一级标题，再遍历其对应的二级标题，再遍历二级标题下的各行文本，最后遍历二级标题对应的参数，识别参数构造该行文本
        文本构造：分为H1，H2，参数行、非参数行
            参数行中参数，以【*参数值*】的形式标注
        参数遍历细化：共四类参数
            规则库对应参数，直接标注并构造文本；
            表格对应参数，先标注表格所在行，再标注参数
                表格参数分为规则库对应参数，和非对应参数（默认表格中所有有效值均为参数）
            新参数，即不属于规则库的参数，暂不标注；
            右侧明细表参数，构造在文档最尾行；
    """

    # todo 表格行未注明，明细表未注明
    def tagParameter(self):
        dataList = []
        ruleCSRowNum = 0
        formNum = 0
        formRowNum = 0
        H1Num = 0
        H2Num = 0
        for titleDict in self.titleList:
            # 先识别一级标题，再识别其对应的二级标题，再识别有参数的行（遍历的方法和index的方法）
            if titleDict["titleLV"] == 1:
                ftID = titleDict["titleID"]
                dataList.append("【H1】:" + " " * 40 + titleDict["titleName"])
                H1Num += 1
                # 遍历二级标题，提取该一级标题下的二级标题
                for othertitleDict in self.titleList:
                    if othertitleDict["ftID"] == ftID:
                        dataList.append("【H2】:" + " " * 40 + othertitleDict["titleName"])
                        H2Num += 1
                        # 遍历二级标题中各行文本
                        for tt in othertitleDict["titleText"]:
                            rowdataList = []
                            ttType = 0
                            # 通过rowID判断tt是否为表格行，进行表格行重构
                            if self.judgeFormRow(tt[0]):
                                formrowData = tt[1]
                                formTableList = self.judgeFormData(formrowData)
                                if formTableList != []:
                                    # todo 避免表格重复读取，确定为哪个表格，并表格重构
                                    rowList = self.tagFormCS(formTableList)
                                    for rowForm in rowList:
                                        dataList.append(rowForm)
                                        formRowNum += 1
                                    formNum += 1
                            else:
                                # 遍历参数，一行有多个参数
                                for csDict in self.csList:
                                    # 判断是否属于该父级标题
                                    if csDict["titleID"] == othertitleDict["titleID"]:
                                        # 判断是否属于二级标题下的行文本，是即为参数行，进行参数标记
                                        if csDict["rowID"] == tt[0]:
                                            # 判断参数类型，纯数字为参数库参数，表格参数为tableXX，新参数为newXX
                                            if re.match(r'\d', csDict["ID"]):
                                                rowData = self.tagRuleCS(csDict)
                                                rowdataList.append(rowData)
                                                ttType = 1
                                # 判断ttType，并构造该row的文本，已标注所有参数,
                                if ttType == 1:
                                    dataList.append(''.join(rowdataList))
                                    ruleCSRowNum += 1
                                elif ttType == 0:
                                    # 避免标题行重复读取
                                    if tt[1] != othertitleDict["titleName"]:
                                        dataList.append("【非参数行】" + " " * 30 + tt[1])
        # 去除空白行，获得最终文本行的list
        dataList = list(filter(None, dataList))
        self.saveTxt(dataList)
        # 获取参数数量
        ruleCSNum, newCSNum, rightCSNum, formCSNum, formRuleCSNum = self.getCSNum()
        indexDict = self.creatIndexDict(len(dataList), H1Num, H2Num, ruleCSNum, ruleCSRowNum, formRowNum, formNum,
                                        formCSNum, newCSNum, rightCSNum, formRuleCSNum)
        print("PDF总行数：%s；一级标题行数：%s，二级标题行数%s；有参数的行数%s；表格行数%s；无参数的行数%s" %
              (len(dataList), H1Num, H2Num, ruleCSRowNum, formRowNum,
               len(dataList) - ruleCSRowNum - formRowNum - H2Num - H1Num))
        print("PDF识别规则库参数个数：【%s】\nPDF中表格数量：【%s】" % (ruleCSNum, formNum))
        return indexDict

    # 获取各类型参数数量
    def getCSNum(self):
        formCSNum = 0
        formRuleCSNum = 0
        newCSNum = 0
        rightCSNum = 0
        ruleCSNum = 0
        for csDict in self.csList:
            if "table" in csDict["ID"]:
                formCSNum +=1
                if re.match(r'\d', csDict["fcsID"]):
                    formRuleCSNum += 1
            elif "newCS" in csDict["ID"]:
                newCSNum += 1
            elif "rightCS" in csDict["ID"]:
                rightCSNum += 1
            elif re.match(r'\d', csDict["ID"]):
                ruleCSNum += 1
        return ruleCSNum,newCSNum,rightCSNum,formCSNum,formRuleCSNum

    # indexDict构造
    def creatIndexDict(self, pdfRowNum, H1Num, H2Num, ruleCSNum, ruleCSRowNum, formRowNum, formNum, formCSNum, newCSNum,
                       rightCSNum, formRuleCSNum):
        indexDict = {}
        indexDict["pdfRowNum"] = pdfRowNum
        indexDict["H1Num"] = H1Num
        indexDict["H2Num"] = H2Num
        indexDict["formNum"] = formNum
        indexDict["ruleCSRowNum"] = ruleCSRowNum
        indexDict["formRowNum"] = formRowNum
        indexDict["unCSRowNum"] = pdfRowNum - ruleCSRowNum - formRowNum - H2Num - H1Num
        indexDict["ruleCSNum"] = ruleCSNum
        indexDict["formCSNum"] = formCSNum
        indexDict["formRuleCSNum"] = formRuleCSNum
        indexDict["newCSNum"] = newCSNum
        indexDict["rightCSNum"] = rightCSNum
        return indexDict

    # 判断是否为表格行,匹配成功为True
    def judgeFormRow(self, ttrowID):
        for formrow in self.formRows:
            # 锁定表格的行
            if ttrowID == formrow[0]:
                return True

    # 通过该行data匹配，获取整个form的table
    def judgeFormData(self, formrowData):
        formTableList = []
        for formTable in self.formList:
            # 获取表头
            formTitles = formTable[0]
            # 内容匹配
            j = 0
            for ft in formTitles:
                if str(ft) in formrowData:
                    j += 1
            # j用于判断表头与该行表内容的匹配项，大于3项匹配成功
            if j > 3:
                formTableList = formTable
                break
        return formTableList

    # 输入表格行，表格table，标注表格参数，构造表格行，dataList
    def tagFormCS(self, formTableList):
        rowList = []
        # for csDict in self.csList:
        #     # 通过rowID识别表格参数
        #     if csDict["rowID"] == rowID:
        #         csValue = csDict["csValue"]
        #         csXY = csDict["titleID"]
        #         # 参数标注
        # 获取表格的剩下每一行,构造newRow
        for j in range(0, len(formTableList)):
            formRowList = list(filter(None, formTableList[j]))
            # 表头，可能存在None
            if j == 0:
                newRow = "【表格行-表头】" + " " * 32 + '    '.join(formRowList)
            else:
                for i in range(1, len(formRowList)):
                    if i >= 2:
                        formRowList[i] = "【*" + formRowList[i] + "*】"
                newRow = "【表格行-参数行】" + " " * 30 + '    '.join(formRowList)
            rowList.append(newRow)
        return rowList

    # 标注规则库对应的参数
    def tagRuleCS(self, csDict):
        csName = csDict["fcsName"]
        csValue = csDict["csValue"]
        lastText = csDict["lastText"]
        nextText = csDict["nextText"]
        rowData = "【参数行：" + csName + "】" + " " * (30 - len(csName) * 2) + lastText + "【*" + csValue + "*】" + nextText
        return rowData

    # 保存到txt中
    def saveTxt(self, dataList):
        fileName = "pdfMould_" + self.pdfName
        for dd in dataList:
            print(dd)
        saveTxt(fileName, dataList)
