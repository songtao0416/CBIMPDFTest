from dataHandle.saveExcel import saveXlsx
from dataGet.wordGet import wordData
from dataGet.txtGet import txtGet
from dataHandle.moduleCut import moduleJudge
from dataHandle.parameterJudge import parameterJudge

def readWord():
    wordList = wordData().wordList
    return wordList

def readTxt():
    txtList = txtGet().txtData
    return txtList



if __name__ == '__main__':
    # 读取
    # dataList = readWord()
    dataList = readTxt()
    # 模块处理
    moduleList = moduleJudge(dataList).moduleAll
    # 参数处理
    parameList = parameterJudge(moduleList).parameList
    # 保存结果
    # saveXlsx(moduleList, parameList)
