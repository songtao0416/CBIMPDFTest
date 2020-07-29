from dataGet import wordGet
import re


# 先分割模块，再分割内容
class moduleJudge:
    """
    功能：模块识别与处理
    逻辑：在word段落中提取模块，再按层级逐步提取模块下对应的内容，再分别提取一级模块中的参数，再二级模块中的参数，再三级模块中的参数
    问题：各级模块内容提取对象是整个word文档，导致二级模块中最后一个模块的内容超载，包含了其后的word中的全部内容
    解决：未解决
    """

    def __init__(self):
        self.wordList = wordGet.wordData().wordList
        self.cutModule()

    # 按模块层级逐级遍历，若不为空则继续
    def cutModule(self):
        restrs = [r"\D、\w+", r"\d.\D\w+", r"\d.\d+\w+"]
        fatherCons = [{"cons": self.wordList}]
        for restr in restrs:
            # 传入上级内容，获取父级内容
            fatherList = self.wordList
            # 传入正则和父级内容，获取该父级的子级模块序号+名称
            moduleList = self.getIndex(restr, fatherList)
            # # 若不为空则获取子级模块内容
            if len(moduleList) > 0:
                fatherCons = self.getCons(moduleList, fatherList)

    # 内容截止到本模块序号前
    def getFather(self, fatherCons):
        fatherList = fatherCons[-1]["cons"]
        print("fatherList", fatherList)
        # for i in range(0, index):
        #     fatherList.append(self.wordList[i])
        return fatherList

    # 通过正则获得模块序号，传入正则表达式和内容,返回序号+模块名称
    def getIndex(self, restr, fatherList):
        # 提取模块结构
        moduleList = []
        a= []
        for i in range(0, len(fatherList)):
            line = self.wordList[i]
            m1 = re.match(restr, line)
            # 提取一级模块,段落序号+内容
            if m1 is not None:
                moduleDict = dict(index=i, name=m1.group(), cons=line)
                moduleList.append(moduleDict)
        return moduleList

    # 传入模块序号、父级内容，分割后得到模块后内容
    # 先获取模块的序号段，遍历父级内容，得到模块内容
    def getCons(self, moduleList, fatherList):
        moduleCons = []
        # 获取模块序号段
        for j in range(0, len(moduleList)):
            moduleCon = []
            startIndex = moduleList[j]["index"]
            for i in range(0, len(fatherList)):
                line = fatherList[i]
                if j == len(moduleList) - 1:
                    if i > startIndex - 1:
                        moduleCon.append(line)
                elif i < moduleList[j+1]["index"]:
                    if i > startIndex - 1:
                        moduleCon.append(line)
            # 此处的index对应的是wordList中的段落号，i对应的是模块中的段落号，应修改i为i+k
            moduleDict = dict(index=moduleList[j]["index"], name=moduleList[j]["name"], cons=moduleCon)
            moduleCons.append(moduleDict)
        print("moduleList", moduleList)
        print("moduleCons", moduleCons)
        print(len(moduleCons))
        for line in moduleCons:
            print(line)

moduleJudge()

