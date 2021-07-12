import re

"""
    获取参数的上下文信息，为固定字段
    输入：参数值，参数所在行，全部参数
    输出：参数上下文, str
"""


class getgroudText:

    def __init__(self, rowCSList, rowData):
        self.csList = rowCSList
        self.rowData = rowData
        self.getText()




    # 提取参数的上下文,行数据去掉参数值，即得到参数上下文
    # 优化：需读取完所有参数后，针对每一行定位参数，以参数为界限提取上下文
    # todo 目前上下文提取模糊，未解决同一行多个参数时，参数的上下文包含其他参数
    def getText(self):
        lenRow = len(self.rowData)
        # 判断参数数量，多个参数时，只取上文，最后一个参数取上下文；
        if len(self.csList) > 1:
            # 遍历所有参数并获取其上文、下文
            for i in range(0, len(self.csList)):
                newCSDict = self.csList[i]
                csValue = newCSDict["csValue"]
                lenCS = len(csValue)
                csIndex = self.rowData.find(str(csValue))
                # 非最后一个参数时
                if i < len(self.csList)-1:
                    # nextcsValue = self.csList[i+1]["csValue"]
                    # nextcsIndex = self.rowData.find(str(nextcsValue))
                    nextText = ""
                    # 判断是否第一个参数，首参数则从0开始取上文
                    if i == 0:
                        lastIndex = 0
                    else:
                        lastcsValue = self.csList[i-1]["csValue"]
                        lastIndex = self.rowData.find(str(lastcsValue))+len(lastcsValue)
                # 截取最后一个参数时,需截取下文
                else:
                    nextcsIndex = lenRow
                    lastcsValue = self.csList[i-1]["csValue"]
                    lastIndex = self.rowData.find(str(lastcsValue))+len(lastcsValue)
                    nextText = self.rowData[csIndex + lenCS: nextcsIndex]
                lastText = self.rowData[lastIndex: csIndex]
                newCSDict["lastText"] = lastText
                newCSDict["nextText"] = nextText
                self.csList[i] = newCSDict
                # 检验上下文问题出处
                # if self.csList[i]["ID"] == 115:
                #     print(csValue, "\n", self.rowData)
                #     print(csIndex + lenCS, nextcsIndex, lenRow, i, len(self.csList))
                #     print("lastText", lastText)
                #     print("nextText", nextText)
                #     print(self.csList[i])
        # 只有一个参数时
        else:
            newCSDict = self.csList[0]
            csValue = newCSDict["csValue"]
            lenCS = len(csValue)
            csIndex = self.rowData.find(str(csValue))
            lastText = self.rowData[0:csIndex]
            nextText = self.rowData[csIndex+lenCS:lenRow]
            newCSDict["lastText"] = lastText
            newCSDict["nextText"] = nextText
            self.csList[0] = newCSDict







# 测试
# rowData = "1)本工程防火设计执行《建筑设计防火规范》（GB 50016—2006）、《建筑内部装修设计防火规范》（GB 50222—95）、《汽车库、修车库、停车场设计防火规范》（GB 50067-97）" \
#           "等现行国家规范的要求。"
# csValue = [{"csValue":"《建筑设计防火规范》（GB 50016—2006）","lastText":"","nextText":""},
#            {"csValue":"《建筑内部装修设计防火规范》（GB 50222—95）","lastText":"","nextText":""},
#            {"csValue":"《汽车库、修车库、停车场设计防火规范》（GB 50067-97）","lastText":"","nextText":""}]
# csList = getgroudText(csValue, rowData).csList
# for cs in csList:
#     csValue = cs["csValue"]
#     lastText = cs["lastText"]
#     nextText = cs["nextText"]
#     print("上下文复现", lastText + "【" + csValue + "】" + nextText)