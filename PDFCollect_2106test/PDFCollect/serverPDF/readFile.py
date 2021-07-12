import os
from config.configPDF import configPDF

"""
    读取目录下的所有文件名
    传入：目录地址
    传出：文件地址list
"""
class readFile:

    def __init__(self):
        self.path = configPDF().pdfPath
        # 读取本文件中所有python文件
        # self.path = "F:\项目代码\Python代码\CBIM设计说明文档识别\PDFCollect"
        self.fileNames = []
        self.fileList = self.listdir(self.path, [])

    # 递归获取路径下所有文件名     # -*- coding: utf-8 -*-
    def listdir(self, path, list_name):  # 传入存储的list
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isdir(file_path):
                self.listdir(file_path, list_name)
            else:
                list_name.append(file_path)
                self.fileNames.append(file)
        # print(list_name)
        # print(fileNames)
        return list_name

    # def file_name(self, file_dir):
    #     L = []
    #     for root, dirs, files in os.walk(file_dir):
    #         for file in files:
    #             if os.path.splitext(file)[1] == '.jpeg':  # 想要保存的文件格式
    #                 L.append(os.path.join(root, file))
    #     return L

    # def getData(self):
    #     path = self.path  # 文件夹目录
    #     files = os.listdir(path)  # 得到文件夹下的所有文件名称
    #     print(files)
    #     s = []
    #     for file in files:  # 遍历文件夹
    #         if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
    #             print(file)
    #     #         f = open(path + "/" + file)  # 打开文件
    #     #         iter_f = iter(f)  # 创建迭代器
    #     #         str = ""
    #     #         for line in iter_f:  # 遍历文件，一行行遍历，读取文本
    #     #             str = str + line
    #     #         s.append(str)  # 每个文件的文本存到list中
    #     print(s)  # 打印结果


# fileNames = readFile().fileNames
# print(fileNames)
# for x in fileNames:
#     print(x)