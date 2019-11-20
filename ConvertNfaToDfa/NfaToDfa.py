# _*_coding:utf-8_*_
# file: NfaToDfa.py
# author: Yan_Daojiang
import json


def readNfa(inputFile):
    """从json文件中读取又穷自动机M, M表示为一个五元组M=(K, E, f, S, Z)"""
    M = json.load(open(inputFile, 'r'))
    K = set(M["K"])
    E = M["E"]
    f = M["f"]  # 转换规则f的外层是一个字典，字典的键是状态，值又是一个字典，值字典的键是边
    S = set(M["S"])
    Z = set(M["Z"])
    return K, E, f, S, Z


def epsilon_closure(f, I):
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
            opt_closure(f, closure_flag)
    # 没有新的状态加入就返回
    return set(closure_flag.keys())


def move(f, I, arc):
    """move函数的实现，从集合I中的某个状态出发，经过一条arc弧到达的状态"""
    new_states = set()  # 将转移状态集合初始化为空集
    for i in I:
        if arc in f[i].keys():
            for new_state in f[i][arc]:
                new_states.add(new_state)
    return new_states


def subSet(f, E, K_0):
    """子集构造算法,传入参数为NFA状态装换规则，字母表和NFA初始状态"""
    subsets = {}  # 保存构造出的所有子集
    flags = {}  # 每个子集设置一个标志，表明是否被标记
    relations = {}  # 子集间的转换关系
    index = 0
    # 开始，令ε-closure(K_0)为C中的唯一成员，并且将其设置为未标记状态
    subsets[index] = epsilon_closure(f, K_0)
    flags[index] = False

    while True:
        C = list(subsets.keys())
        subsets_num_before_move = len(C)
        # 如果还存在没用move函数转换的子集
        for i in C:
            if flags[i] == False:
                # 把选中用来move的状态集标志位置为True
                flags[i] = True
                # 构造两个状态之间的转换关系
                relations[i] = {}
                for ch in E:
                    U = epsilon_closure(f, move(f, subsets[i], ch))

                    # 如果转换后的新状态集已经在subsets里面不存在,才添加,并添加转换关系
                    if U not in subsets.values():
                        index += 1
                        subsets[index] = U
                        # 并将新状态的标记为设置为False
                        flags[index] = False
                        relations[i][ch] = index
                    # 如果转换后的状态集已经在subsets中存在，不添加集合,但添加转换关系
                    else:
                        # 字典中根据value获得key （因为是一一对应的关系）
                        relations[i][ch] = list(subsets.keys())[list(subsets.values()).index(U)]

        # 把C更新（因为添加了新的子集）
        C = list(subsets.keys())
        subsets_num_after_move = len(C)
        if subsets_num_before_move == subsets_num_after_move:
            break
    return subsets, relations


def convert(K, E, f, S, Z):
    """转换函数"""
    subsets, relations = subSet(f, E, S)    # 调用子集合构造函数，获取子集合和转换关系
    # 对状态子集合的返回进行解析，根据转换关系构造DFA M
    print(subsets)
    print(relations)


if __name__ == '__main__':
    nfa = 'nfa.json'
    K, E, f, S, Z = readNfa(nfa)  # NFA M = (K, E, f, S, Z),f['i']['arc']表示状态i经过arc弧到达的状态
    convert(K, E, f, S, Z)
