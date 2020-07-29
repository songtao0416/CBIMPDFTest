import re
import jieba

class parameterJudge:
    """
    功能：参数识别与处理
    逻辑：判定模块集中，child(子模块内容)为空的模块包含参数，从其cons(模块名称+内容)中获取参数
    cutModule()，按倒序的层级来遍历模块，提取无子集的模块
    getParame()，获取cons中的参数信息，返回{parameID, moduleID, parameName, parameValue=}
    cutString()，对参数进行正则处理，分割参数名和参数值；

    """

    def __init__(self, moduleList):
        # moduleall=[{level, module}]
        self.moduleAll = moduleList
        self.getmoduleList = self.cutModule()
        self.parameList = self.getParame()
        print("*"*10, "完成参数解析，共处理参数%s个" % len(self.parameList), "*"*10)
        print(self.parameList)

    # 参数={参数编号，模块编号，参数名称，参数值}
    def parameterID(self):
        pass

    # 遍历模块，取最下级模块，即取无子集的模块提取参数
    def cutModule(self):
        getmoduleList = []
        for i in range(len(self.moduleAll)-1, -1, -1):
            moduleList = self.moduleAll[i]
            print("第%s层级模块:" % moduleList["level"], moduleList["module"])
            for mm in moduleList["module"]:
                if len(mm["child"]) < 1:
                    getmoduleList.append(mm)
        # print("getmoduleList", getmoduleList)
        return getmoduleList

    # 组建参数
    def getParame(self):
        parameList = []
        for i in range(0, len(self.getmoduleList)):
            module = self.getmoduleList[i]
            parame = self.cutString(module["cons"])
            parameID = i+1
            parameDict = dict(parameID=parameID, moduleID=module["moduleID"], parameName=parame[0], parameValue=parame[-1])
            parameList.append(parameDict)
            # print('parameDict',parameDict)
        return parameList

    # 字符串处理特殊符号
    def cutString(self, string):
        # 先去掉空格，再特殊字符分割：参数名，参数值
        restr = r'\s'
        reString = re.split(restr, string.replace(' ', ''))
        for i in range(0, len(reString)):
            nameString = reString[0]
            nameString = re.sub(r'\w[、]', '', nameString)
            nameString = re.sub(re.compile(r'[^\u4e00-\u9fa5]'), '', nameString)
            # nameString = re.sub(r'\r"\D、+"', '', nameString)
            # nameString = re.sub(r'\W?', '', nameString)
            if len(reString) == 1:
                reString.append(nameString)
            # 参数名检查，限制字符长度
            if len(nameString)>10:
                nameString = nameString[0:6]
            reString[0] = nameString
        # print("reString", reString)
        return reString

# parameterJudge()