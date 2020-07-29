import re


# 先分割模块，再分割内容，返回[{'index': 65, 'moduleID': '03052', 'name': '2.15装配式', 'cons': '2.15装配式\u2003本子项工程为装配式建筑', 'child': []}]
class moduleJudge:
    """
    功能：模块识别与处理
    逻辑：通过正则识别各级模块，获取各级模块及模块内对应的子模块内容
    cutModule()遍历各级模块的re并执行getIndex()；
    getIndex()传入正则和内容，返回{wordIndex, moduleLv, moduleID, name, cons}；
    checkModuleList()避免最后一个模块取值超界；
    """

    def __init__(self, wordList):
        self.wordList = wordList
        self.moduleAll = self.cutModule()
        print("*"*10, "完成模块解析,共处理模块%s层" % len(self.moduleAll), "*"*10)
        print(self.moduleAll)

    # 按模块层级逐级遍历，若不为空则继续
    def cutModule(self):
        # 各种标题的正则表达式
        restrs = [r"\D、\w+", r"\d.\D\w+", r"\d.\d+\w+"]
        lv = 1
        moduleAll = []
        for i in range(0, len(restrs)):
            # 传入正则和父级内容，获取该父级的子级模块序号+名称
            moduleList = self.getIndex(restrs[i], self.wordList, lv)
            moduleList = self.checkModuleList(restrs[i-1], moduleList)
            if len(moduleList) > 0:
                lv += 1
            moduleCons = dict(level=i+1, module=moduleList)
            moduleAll.append(moduleCons)
        return moduleAll

    # 避免最后一个模块超界
    def checkModuleList(self, restr, moduleList):

        if len(moduleList[-1]["child"]) > 0:
            for m in moduleList[-1]["child"]:
                m1 = re.match(restr, m)
                if m1 is not None:
                    moduleList[-1]["child"] = []
                    break
        return moduleList

    # 通过正则获得模块序号，传入正则表达式和内容,返回序号+模块名称
    def getIndex(self, restr, fatherList, lv):
        # 提取模块结构
        moduleList = []
        a = []
        j = 1
        for i in range(0, len(fatherList)):
            line = self.wordList[i]
            m1 = re.match(restr, line)
            # 提取一级模块,段落序号+内容
            if m1 is not None:
                if len(moduleList) > 0:
                    moduleList[-1]["child"] = a
                moduleDict = dict(wordIndex=i, moduleLv=lv, moduleID=self.moduleID(lv, j, len(moduleList)), name=m1.group(), cons=line)
                moduleList.append(moduleDict)
                a = []
                j += 1
            else:
                a.append(line)
            if len(moduleList) > 0:
                if i == len(fatherList)-1:
                    moduleList[-1]["child"] = a
        # print("moduleList", moduleList)
        # for i in range(0,len(moduleList)):
        #     print("第%s层第%s个模块" % (lv, (i+1)), moduleList[i])
        return moduleList

    def moduleID(self, lv, j, moduleLen):
        moduleID = 0
        if lv ==1:
            moduleID = j
        elif lv ==2:
            moduleID = lv * 100 +j
        elif lv ==3:
            moduleID = lv * 10000 +j
        return moduleID




# moduleJudge()

