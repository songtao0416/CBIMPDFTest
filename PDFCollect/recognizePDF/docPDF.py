# --*-- coding:utf-8 --*--

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import *
from pdfminer.converter import PDFPageAggregator
import PyPDF2
import camelot
import pdfplumber
import pandas as pd

"""
    读取文档格式的PDF
    输入：传入pdf文件地址
    输出：返回读取内容=[rowData]
"""
class docPDF:

    def __init__(self, f):
        self.pdfPath = f
        self.pdfText = self.getpdfminer()

    def getpdfminer(self):
        # 以二进制读模式打开
        # fp = open(self.pdfPath, 'rb')
        # 接受上传的pdf文档
        fp = self.pdfPath
        print(type(fp))
        # 从文件句柄创建一个pdf解析对象
        parser = PDFParser(fp)
        # 创建pdf文档对象，存储文档结构
        document = PDFDocument(parser)
        # 创建一个pdf资源管理对象，存储共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个device对象
        laparams = LAParams()
        # device = PDFDevice(rsrcmgr)
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个解释对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # 用来计数页面，图片，曲线，figure，水平文本框等对象的数量
        num_page, num_image, num_curve, num_figure, num_TextBoxHorizontal = 0, 0, 0, 0, 0
        # 处理包含在文档中的每一页
        results = []
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            # print("page", page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            """
            LTTextBox:代表一组被包含在矩形区域中的文本
            LTTextLine:表现为单行文本
            LTChar / LTAnno:作为一个unicode字符串
            LTFigure:图表
            LTImage:代表一个图形对象
            LTLine:代表一根直线。用来分割文本或图表(figures)。
            LTRect:代表一个矩形。用来框住别的图片或者图表。
            LTCurve:代表一个贝塞尔曲线。
            """
            results = []
            for x in layout:
                # print(x.get_text())
                if isinstance(x, LTImage):  # 图片对象
                    num_image += 1
                if isinstance(x, LTCurve):  # 曲线对象
                    num_curve += 1
                if isinstance(x, LTFigure):  # figure对象
                    num_figure += 1
                if isinstance(x, LTTextBoxHorizontal):  # 获取文本内容
                    num_TextBoxHorizontal += 1  # 水平文本框对象增一
                    # 保存文本内容
                    print("pdfText:", x.get_text())
                    results.append(x.get_text())
        print(num_page,num_image,num_curve,num_figure,num_TextBoxHorizontal)
        return results


    def getPlumber(self):
        formList = []
        with pdfplumber.open(self.pdfPath) as pdf:
            first_page = pdf.pages[0]
            # # 获取文本，直接得到字符串，包括了换行符【与PDF上的换行位置一致，而不是实际的“段落”】
            # print(first_page.extract_text())
            # 获取本页全部表格，也可以使用extract_table()获得单个表格
            for table in first_page.extract_tables():
                # print(len(first_page.extract_tables()))
                # df = pd.DataFrame(table)
                # 第一列当成表头：
                df = pd.DataFrame(table[1:], columns=table[0])
                # print(df)
                formList.append(df)
            return formList


    # 使用py2pdf解析pdf，无法识别图片pdf
    # 处理英文效果好，处理中文效果差
    # def getPDF2(self):
    #     # 读取文件
    #     reader = PyPDF2.PdfFileReader(open(self.pdfPath, 'rb'))
    #     # 获取pdf总页数
    #     pdfNum = reader.getNumPages()
    #     print("总页数：", pdfNum)
    #     # 判断是否有加密
    #     print("是否加密：", reader.isEncrypted)
    #     # 获取每一页文字
    #     # for i in range(0, reader.getNumPages()):
    #     i = 0
    #     page = reader.getPage(i)
    #     print("第%s页内容为\n" % i, page.extractText())
    #     # 获取PDF元信息，即创建时间，作者，标题等
    #     print("PDF元信息：", reader.getDocumentInfo())

    # pdfminer识别
    # 因为pdfminer只是获取PDF中的文本。如果这个PDF本身就不能提取文本

    # camelot读取pdf的表格
    # 效果较差
    # def getCamelot(self):
    #     tables = camelot.read_pdf(self.pdfPath, flavor='stream')  # 类似于Pandas打开CSV文件的形式
    #     # tables[0].df  # get a pandas DataFrame!
    #     # tables.export('foo.csv', f='csv', compress=True)  # json, excel, html, sqlite，可指定输出格式
    #     # tables[0].to_csv('foo.csv')  # to_json, to_excel, to_html, to_sqlite， 导出数据为文件
    #     # tables[0].parsing_report
    #     print(tables[0])
    #     print(tables[0].df)
    #     print(tables[0].parsing_report)
    #     tables.export('foo.csv', f='csv', compress=True)
    #     tables[0].to_csv('foo.csv')

    # pdfPlimber识别表格
    # 按行读取，当出现多列时即不实用

# # 测试
# pdfPath = "F:\\项目代码\\Python代码\\CBIM设计说明文档识别\\PDFCollect\\resources\\pdf文本\\崇礼度假区\\崇礼度假区（建筑单专业） h建施-001 - 设计说明及图纸目录.pdf"
# pdfText = docPDF(pdfPath).pdfText
# print(pdfText)