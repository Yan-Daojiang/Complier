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

def epsilon_closure(f,I):
    """求状态集合I:ε-clouure(I)"""
    I = set(I)
    # 设置每个状态的标志
    closure_flag = dict()
    for i in I:
        closure_flag[i] = False  # 初始状态设置为False
    # 调用闭包操作函数进行递归求解
    return opt_closure(f, closure_flag)

def opt_closure(f, closure_flag):
    """被ε-closure(I)函数进行调用，进行递归求解，知道集合不再增大就返回调用函数"""
    for i in list(closure_flag.keys()):
        if "#" in f[i].keys() and closure_flag[i] == False:
            for new_state in f[i]["#"]:
                closure_flag[new_state] = False  # 添加新的状态，并将操作标志置为False
            # 更改当前的标志位
            closure_flag[i] = True
            # 对新加入的状态进行递归求解
            opt_closure(f,closure_flag)
            # 没有新的状态加入就返回
    return set(closure_flag.keys())

def move(f,I,arc):
    """move函数的实现，从集合I中的某个状态出发，经过一条arc弧到达的状态"""
    new_states = set()    # 将转移状态集合初始化为空集
    for i in I:
        if arc in f[i].keys():
            for new_state in f[i][arc]:
                new_states.add(new_state)
    return new_states




if __name__ == '__main__':
    nfa = 'nfa.json'
    K, E, f, S, Z = readNfa(nfa) # NFA M = (K, E, f, S, Z),f['i']['arc']表示状态i经过arc弧到达的状态
    





