from dataGet.keywordGet import keyWordGet
from dataGet.wordGet import wordData
import re

class keywordMate:

    def __init__(self):
        self.cutRuleList = keyWordGet().cutRuleList
        self.wordList = wordData().wordList
        self.keywordMate()

    def keywordMate(self):
        # [{'parameID': 1.0, 'parameName': '市规划国土函', 'parameType': '文本', 'parameUnitType': 3.0, 'parameKeyword': '市规划局||国土函', 'parameRE': '《(.*?)》'}]
        j = 0
        mateParame = []
        for cons in self.wordList:
            # print("待匹配单元", cons)
            j += 1
            for i in range(0,len(self.cutRuleList)):
                keywords = self.cutRuleList[i]["parameKeyword"]
                if len(keywords) > 1:
                    keywords = self.keywordCut(keywords)
                    # for keyword in keywords:
                    keyword = keywords
                    if keyword in cons:
                        print("关键词匹配成功：【%s】" % keyword)
                        parameUnit = self.wordList[j - 1]
                        parameList = self.parameCut(parameUnit)
                        mateKeyword = dict(parameID=j, parameKeyword=keyword, parameName=self.cutRuleList[i]["parameName"],
                                           parameValue=parameList[-1], parameUnit=parameUnit)
                        mateParame.append(mateKeyword)
                        print(mateKeyword)
                    # else:
                    #     print("关键词匹配不成功：【%s】" % keyword)
        print(mateParame)
        print("匹配成功%s个" % len(mateParame))

    def keywordCut(self, keywords):
        # keywords中为字符串，需要分割
        # keywords = re.sub("&", "||", keywords)
        # k1 = keywords.split("||")
        keywords = re.sub("&", "", keywords)
        keywords = re.sub("\||", "", keywords)
        return keywords

    def parameCut(self, string):
        # 先去掉空格，再特殊字符分割：参数名，参数值
        restr = r'\s'
        reString = re.split(restr, string.replace(' ', ''))
        for i in range(0, len(reString)):
            nameString = reString[0]
            nameString = re.sub(r'\w[、]', '', nameString)
            nameString = re.sub(re.compile(r'[^\u4e00-\u9fa5]'), '', nameString)
            # nameString = re.sub(r'\r"\D、+"', '', nameString)
            # nameString = re.sub(r'\W?', '', nameString)
            if len(reString) == 1:
                reString.append(nameString)
            # 参数名检查，限制字符长度
            if len(nameString) > 10:
                nameString = nameString[0:6]
            reString[0] = nameString
        # print("reString", reString)
        return reString







keywordMate()