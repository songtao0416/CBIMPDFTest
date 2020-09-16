from wand.image import Image
from PIL import Image as PI
import pytesseract

"""
    尚未成功
    读取图片格式的PDF
    传入pdf文件地址
    返回读取内容
"""
#  todo 图片识别
class pdfOCR:

    def __init__(self, path):
        self.pdfPath = path
        self.reqImage = self.pdftoImage()
        self.imageOCR()

    def readPDF(self):
        pass

    def pdftoImage(self):
        reqImage = []
        # 采用wand将一个PDF文件转成jpeg文件
        imagePdf = Image(filename=self.pdfPath, resolution=300)
        imageJpeg = imagePdf.convert('jpeg')
        for img in imageJpeg.sequence:
            imgPage = Image(image=img)
            reqImage.append(imgPage.make_blob('jpeg'))
        return reqImage

    def imageOCR(self):
        finalText = []
        for img in self.reqImage:
            txt = pytesseract.image_to_string(img, lang='eng')
            finalText.append(txt)
            print(txt)
        return finalText

pdfOCR(path="..\\pdf文本\\崇礼度假区（建筑单专业） K建施-001 - 设计说明及图纸目录.pdf")
