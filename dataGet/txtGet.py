import re
from configCBIM.fileConfig import fileConfig

class txtGet:

    def __init__(self):
        self.file = fileConfig().fileAddress["txtPDF"]
        self.txtData = self.openTxt()

    def openTxt(self):
        # python读取txt，读一次操作一次，否则为空
        with open(self.file, 'r', encoding='utf-8') as f:
            # data = f.read()
            txtData = f.readlines()
            print(len(txtData))
            txtData = self.strHandle(txtData)
        f.close()
        return txtData
    
    def strHandle(self, strs):
        Strs = []
        for s in strs:
            str = re.sub('\n', '', s)
            Strs.append(str)
        print(Strs)
        return Strs

txtGet()