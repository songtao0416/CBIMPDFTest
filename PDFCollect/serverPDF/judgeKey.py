import re

"""
    判断关键词与文本是否匹配
    输入：关键词，匹配文本
    输出：是否匹配
"""
class judgeKey:

    def __init__(self, keyWord, data):
        self.key = keyWord
        self.data = data
        self.judge = self.keyJudge()

    # todo 关键词四级关系，重构
    def keyJudge(self):
        # 优先级:! & || *
        if "!" in self.key:
            keyWords = re.split(r'!', self.key)
            kw = keyWords[0]
            if keyWords[1] not in self.data:
                if "&" in kw:
                    if self.andKeyJudge(kw):
                        return True
                elif "||" in kw:
                    if self.orKeyJudge(kw):
                        return True
                elif kw in self.data:
                    return True
        elif "&" in self.key:
            if self.andKeyJudge(self.key):
                return True
        elif "||" in self.key:
            if self.orKeyJudge(self.key):
                return True
        else:
            if self.key in self.data:
                return True

    # 判断与，需要都满足
    def andKeyJudge(self, keyWord):
        keyWords = re.split(r'&', keyWord)
        j = 0
        for i in range(0, len(keyWords)):
            kw = keyWords[i]
            if "||" in kw:
                if self.orKeyJudge(kw):
                    j += 1
            elif "*" in kw:
                if self.muchKeyJudge(kw):
                    j += 1
            elif kw in self.data:
                    j += 1
        if j == len(keyWords):
            return True

    # 判断或，满足之一即返回true
    def orKeyJudge(self, keyWord):
        keyWords = re.split(r'\|+', keyWord)
        for kw in keyWords:
            if "*" in kw:
                if self.muchKeyJudge(kw):
                    return True
            elif kw in self.data:
                return True

    # 判断多，限制其出现次数
    def muchKeyJudge(self, keyWord):
        pdfData = self.data
        keyWords = re.split(r'\*', keyWord)
        kw = keyWords[0]
        kwNum = keyWords[1]
        pdkwNum = pdfData.count(kw)
        if str(pdkwNum) >= kwNum:
            return True




# 测试
# key = ["我&好&你||他!吃","我!吃","我&你||他*3!的","哈*2&我"]
# for kw in key:
#     if judgeKey(kw, "我好他他他哈哈哈哈").judge:
#         print(1)
#     else:
#         print(2)


