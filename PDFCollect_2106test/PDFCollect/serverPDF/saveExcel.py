import xlwt
from config.configPDF import configPDF

"""
    将结果保存为excel格式
    输入：提取到的参数list
    输出：excel文件
"""

class saveExcel:

    def __init__(self, fileName, dataList, type):
        self.path = configPDF().excelPath + "\\%s.xls" % fileName
        self.headings = self.getHeading(type)
        self.dataList = dataList
        self.saveXls()

    def getHeading(self, type):
        headings = ""
        if type == 1:
            headings = configPDF().parameterHeadings
        elif type == 2:
            headings = configPDF().titleHeadings
        return headings

    # csGetList = [{ID,fcsID,fcsName,csName,csValue,csType,titleID,lastText,nextText,rowID,rowData}]
    def saveXls(self):
        work_book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        sheet = work_book.add_sheet('已提取参数', cell_overwrite_ok=True)
        headings = self.headings
        for i in range(0, len(headings)):
            sheet.write(0, i, headings[i])
        for j in range(0, len(self.dataList)):
            rowData = list(self.dataList[j].values())
            print("正在存入excle第%s行：%s" % (j+2, rowData))
            for k in range(0, len(rowData)):
                sheet.write(j+1, k, str(rowData[k]))
        work_book.save(self.path)

