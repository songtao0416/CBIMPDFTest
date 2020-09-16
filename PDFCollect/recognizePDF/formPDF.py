import re
import pdfplumber
import pandas as pd

"""
    读取PDF中的表格信息
    输入：pdfPath
    输出：formList =[[table],[]]
         rightList = [[table],[]]
         table = []
"""

class formPDF:

    def __init__(self, f):
        self.pdfPath = f
        # self.formList, self.rightformList
        (self.formList, self.rightformList) = self.getPlumber()
        self.forms = (self.formList, self.rightformList)

    # plumer读取文本类型PDF中的表格，返回formList, rightformList
    def getPlumber(self):
        formList = []
        rightformList = []
        pdfPages = pdfplumber.open(self.pdfPath)
        for page in pdfPages.pages:
            # print(page.extract_text())
            # 第一个表为右侧图框表
            rightTable = page.extract_tables()[0]
            rightformList.append(rightTable)
            # for line in rightTable:
            #     print(line)
            # print("*" * 20)
            for i in range(1, len(page.extract_tables())):
                pdf_table = page.extract_tables()[i]
                # for line in pdf_table:
                #     print(line)
                # print("*" * 20)
                # 表格处理，逻辑或需调整
                table = []
                cells = []
                for row in pdf_table:
                    # any() 函数用于判断给定的可迭代参数 iterable 是否全部为 False，则返回 False，如果有一个为 True，则返回 True。
                    if not any(row):
                        # 如果一行全为空，则视为一条记录结束
                        if any(cells):
                            table.append(cells)
                            cells = []
                    elif all(row):
                        # 如果一行全不为空，则本条为新行，上一条结束
                        if any(cells):
                            table.append(cells)
                            cells = []
                        table.append(row)
                    else:
                        if len(cells) == 0:
                            cells = row
                        else:
                            for i in range(len(row)):
                                if row[i] is not None:
                                    cells[i] = row[i] if cells[i] is None else cells[i] + row[i]
                for row in table:
                    print([re.sub('\s+', '', cell) if cell is not None else None for cell in row])
                print('---------- 分割线 ----------')
                if table != []:
                    formList.append(table)
        pdfPages.close()
        # print(formList)
        return formList, rightformList


    # 方法2，效果暂不理想，作为备用方案
    # def getPlumber2(self):
    #     formList = []
    #     with pdfplumber.open(self.pdfPath) as pdf:
    #         first_page = pdf.pages[0]
    #         # # 获取文本，直接得到字符串，包括了换行符【与PDF上的换行位置一致，而不是实际的“段落”】
    #         # print(first_page.extract_text())
    #         # 获取本页全部表格，也可以使用extract_table()获得单个表格
    #         for table in first_page.extract_tables():
    #             # print(len(first_page.extract_tables()))
    #             # df = pd.DataFrame(table)
    #             # 第一列当成表头：
    #             df = pd.DataFrame(table[1:], columns=table[0])
    #             # print(df)
    #             formList.append(df)
    #             for line in table:
    #                 print(line)
    #         return formList

# 测试
# f = "F:\\项目代码\\Python代码\\CBIM设计说明文档识别\\PDFCollect\\resources\\pdf文本\\崇礼度假区\\崇礼度假区（建筑单专业） H建施-001 - 设计说明及图纸目录.pdf"
# formPDF(f)