from configCBIM.fileConfig import fileConfig
import xlwt

class saveXlsx:
    """
    功能：将处理结果保存为excel
    模块表：["序号","参数编号","参数名称","所属模块编号","参数值"]
    参数表：["序号","模块编号","模块名称","模块层级","段落序号","模块内容","模块子级内容"]
    """

    def __init__(self, moduleList, parameList):
        self.parameList = parameList
        self.moduleAll = moduleList
        self.fileAddress = fileConfig().fileAddress["saveExcel"]
        (self.book, self.sheet1, self.sheet2) = self.creatXlsx()
        self.saveParame()
        self.saveModule()
        self.book.save(self.fileAddress)
        print("结果已保存至%s" % self.fileAddress)

    def creatXlsx(self):
        book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        sheet1 = book.add_sheet('parame', cell_overwrite_ok=True)
        sheet2 = book.add_sheet('module', cell_overwrite_ok=True)
        paramecolNames = ["序号","参数编号","参数名称","所属模块编号","参数值"]
        for i in range(0,len(paramecolNames)):
            sheet1.write(0,i,paramecolNames[i])
        modulecolNames = ["序号","模块编号","模块名称","模块层级","段落序号","模块内容","模块子级内容"]
        for i in range(0,len(modulecolNames)):
            sheet2.write(0,i,modulecolNames[i])
        return book, sheet1, sheet2

    def saveParame(self):
        # dict(parameID=parameID, moduleID=module["moduleID"], parameName=parame[0], parameValue=parame[1])
        for i in range(0, len(self.parameList)):
            parame = self.parameList[i]
            self.sheet1.write(i+1, 0, i)
            self.sheet1.write(i+1, 1, parame["parameID"])
            self.sheet1.write(i+1, 2, parame["parameName"])
            self.sheet1.write(i+1, 3, parame["moduleID"])
            self.sheet1.write(i+1, 4, parame["parameValue"])

    def saveModule(self):
        # [{level：‘’，module：[{'wordindex': 65, 'moduleLv':'3','moduleID': '03052', 'name': '2.15装配式', 'cons': '2.15装配式\u2003本子项工程为装配式建筑', 'child': []}]}]
        j = 0
        for m in self.moduleAll:
            moduleList = m["module"]
            moduleLv = m["level"]

            for i in range(0, len(moduleList)):
                module = moduleList[i]
                j += 1
                self.sheet2.write(j, 0, i)
                self.sheet2.write(j, 1, module["moduleID"])
                self.sheet2.write(j, 2, module["name"])
                self.sheet2.write(j, 3, module["moduleLv"])
                self.sheet2.write(j, 4, module["wordIndex"])
                self.sheet2.write(j, 5, module["cons"])
                self.sheet2.write(j, 6, module["child"])
