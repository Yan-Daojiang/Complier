# _*_coding:utf-8_*_
# file: LexAnalysis_f.py
def getSourceCode(path):
    """按行从文件中读取代码（忽略每行末尾的换行符）,返回源代码串"""
    line = ''
    for s in open(path):
        line = line + s.strip('\n')
    return line


def removeSpace(sourceCode):
    """去除源代码中的空格和制表符
    返回一个字符流形式的代码列表"""
    sourceCode = [' '.join([i.strip() for i in code.strip().split('\t')]) for code in sourceCode]  # 处理
    while '' in sourceCode:
        sourceCode.remove('')
    return sourceCode


def take(sourceCode):
    """从字符流列表开始进行逐一分析"""
    num = 0
    while num != len(sourceCode):
        str = sourceCode[num]
        k = identifyChar(str)
        if k == 1:
            str1, num = idetifier(sourceCode, str, num)
            if isKeyWord(str1):
                printf(str1, isKeyWord(str1))
            else:
                printf(str1, 10)
            continue
        if k == 2:
            str1, num = number(sourceCode, str, num)
            printf(str1, 11)
            continue
        if k == 3:
            str1, num = symbolStr(sourceCode, str, num)
            printf(str1, isSymbol(str1))
            continue


def idetifier(souceCode, s, num):
    """标识符和保留字处理"""
    if num == len(sourceCode) - 1:
        return s, num + 1
    curNum = num + 1
    flag = True
    while flag:
        if isNum(sourceCode[curNum]) or isLetter(sourceCode[curNum]):
            s = s + sourceCode[curNum]
            if isKeyWord(s):
                curNum = curNum + 1
                num = curNum
                return s, num
            curNum = curNum + 1
        else:
            flag = False
        num = curNum
    return s, num


def symbolStr(sourceCode, s, num):
    """符号处理"""
    if num == len(sourceCode) - 1:
        return s, num + 1
    if num == len(sourceCode) - 1:
        return s, num
    curNum = num + 1
    str = sourceCode[curNum]
    if str in [">", "<", "=", ":"]:
        s = s + sourceCode[curNum]
        curNum = curNum + 1
    num = curNum
    return s, num


def number(sourceCode, s, num):
    """对数字进行处理"""
    if num == len(sourceCode) - 1:
        return s, num + 1
    curNum = num + 1
    flag = True
    while flag:
        if isNum(sourceCode[curNum]):
            s = s + sourceCode[curNum]
            curNum = curNum + 1
        else:
            flag = False
    num = curNum
    return s, num


def isSymbol(s):
    """对运算符和界符进行判断，如果是C子集中的运算符和界符界返回相应的种别码"""
    symbol = ["+", "-", "*", "/", ":", ":=", "<", ">", "<>", "<=", ">", ">=", "=", ";", "(", ")", "#"]
    symbolNum = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 0]
    if s in symbol:
        return symbolNum[symbol.index(s)]
    else:
        return 0


def isNum(s):
    """判断是否是数字"""
    if s in '0123456789':
        return True
    else:
        return False


def isLetter(s):
    """判断是否是字母"""
    letters = 'qwertyuiopasdfghjklzxcvbnm'
    if s in letters:
        return True
    else:
        return False


def isKeyWord(s):
    """判断是否是关键字，如果是就返回种别码"""
    key = ["begin", "if", "then", "while", "do", "end"]
    keyNum = [1, 2, 3, 4, 5, 6]
    if s in key:
        return keyNum[key.index(s)]
    else:
        return 0


def identifyChar(c):
    """对单个字符进行识别"""
    if c in 'qwertyuiopasdfghjklzxcvbnm':
        return 1
    if c in '0123456789':
        return 2
    if c in ["+", "-", "*", "/", ":", ":=", "<", ">", "<>", "<=", ">", ">=", "=", ";", "(", ")", "#"]:
        return 3


def printf(s, num):
    print("(" + s + ' , ' + str(num) + ')')


if __name__ == '__main__':
    # path = input("请输入文件的绝对路径:")
    path = 'test.f'
    # 预备工作：从文件中读取源代码，去除中间空白等
    # 后续的分析中以一个字符列表sourceCode为基础
    sourceCode = getSourceCode(path)
    sourceCode = removeSpace(sourceCode)
    # 对字符列表接收进行分析
    take(sourceCode)
