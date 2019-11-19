# _*_coding:utf-8_*_
# file: NfaToDfa.py
# author: Yan_Daojiang
import json

def readNfa(inputFile):
    """从json文件中读取又穷自动机M, M表示为一个五元组M=(K, E, f, S, Z)"""
    M = json.load(open(inputFile,'r'))
    K = set(M["K"])
    E = M["E"]
    f = M["f"]  # 转换规则f的外层是一个字典，字典的键是状态，值又是一个字典，值字典的键是边
    S = set(M["S"])
    Z = set(M["Z"])
    return  K, E, f, S, Z


def set_cache(E):
    """设置一个字典cache进行记录，字典的键是字母表和epsilon弧"""
    cache = {}
    for i in E:
        cache[i] = {}
    cache['#'] = {}
    return cache


def epsilon_closure(f, cache, I):
    """
    状态集合I的epsilon闭包:
    定义为状态集I中的任何状态S经过任意条epsilon弧能到达的状态
    """
    return closure(f, cache["#"], I, '#')

def move(f, cache, I, arc):
    return closure(f, cache[arc], I, arc)

def closure(f, cache, I, arc):
    """闭包的实现，起始的状态为I,边为arc"""
    res = set()
    for i in I:
        if not i in cache:
            cache[i] = set()
            # 判断转换弧为epsilon时
            if arc == '#':
                cache[i] = set([i])   #将本身状态加入其中
            # 实现 move
            if i in f:
                if arc in f[i]:
                    # 如果为epsilon进行递归,确定经过任意条epsilon弧
                    if arc == '#':
                        cache[i] |= closure(f, cache, set(f[i][arc]), arc)
                    else:    # 对于其他非epsilon的边则向前移动一步
                        cache[i] = set(f[i][arc])
        # 得到闭包后的缓存
        res |= cache[i]
    return res

def setDfa(E):
    """设置DFA M的数据结构,M,N的输入字母表是相同的，即是E"""
    dfa = {}
    dfa["k"] = []
    dfa["e"] = list(E)
    dfa["f"] = {}
    dfa["s"] = []
    dfa["z"] = []
    return dfa

if __name__ == '__main__':
    nfa = 'nfa.json'
    K, E, f, S, Z = readNfa(nfa) # NFA M = (K, E, f, S, Z)
    cache = set_cache(E)
    print(f)
    print(epsilon_closure(f,cache,S))





