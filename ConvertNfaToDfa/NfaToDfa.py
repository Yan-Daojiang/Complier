# _*_coding:utf-8_*_
# file: NfaToDfa.py
# author: Yan_Daojiang
import json


def readNfa(inputFile):
    """从json文件中读取自动机M, M表示为一个五元组M=(K, E, f, S, Z)"""
    M = json.load(open(inputFile, 'r'))
    # print(M)
    K = set(M["K"])
    E = M["E"]
    f = M["f"]  # 转换规则f的外层是一个字典，字典的键是状态，值又是一个字典，值字典的键是边
    S = set(M["S"])
    Z = set(M["Z"])
    return K, E, f, S, Z


def epsilon_closure(f, I):
    """求状态集合I:ε-closure(I)"""
    I = set(I)
    # 设置每个状态的标志
    closure_flag = dict()
    for i in I:
        closure_flag[i] = False  # 初始状态设置为False
    # 调用闭包操作函数进行递归求解
    return opt_closure(f, closure_flag)


def opt_closure(f, closure_flag):
    """被ε-closure(I)函数进行调用，进行递归求解，直到集合不再增大就返回调用函数"""
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
    T = {}  # 保存构造出的所有子集,键为子集的下标，值为对应的状态集合
    flags = {}  # 每个子集设置一个标志，表明是否被标记
    relations = {}  # 子集间的转换关系
    index = 0

    # 开始，令ε-closure(K_0)，并且将其设置为未标记状态
    # 即求T_0并标记
    T[index] = epsilon_closure(f, K_0)
    flags[index] = False

    while True:
        # 将子集合状态族C初始化，其中T_0为子集状态族唯一成员，之后循环更新
        # C=（T_1,T_2,...）这里用列表存储下标，下标作为字典的键可进行定位
        C = list(T.keys())
        beforeSize = len(C)  # 通过子集状态族前后变化设置循环退出条件
        for i in C:
            if flags[i] == False:
                flags[i] = True  # 标记T
                # 构造两个状态之间的转换关系
                relations[i] = {}
                for arc in E:
                    U = epsilon_closure(f, move(f, T[i], arc))

                    # 产生的U不在子集状态族中
                    if U not in T.values():
                        index += 1
                        T[index] = U
                        # 并将新状态的标记为设置为False
                        flags[index] = False
                        relations[i][arc] = index
                    # 已经存在就添加转换关系
                    else:
                        # 字典中根据value获得key （因为是一一对应的关系）
                        relations[i][arc] = list(T.keys())[list(T.values()).index(U)]
        # 添加新的子集并更新C
        C = list(T.keys())
        afterSize = len(C)
        # 判断子集合构造是否结束
        if beforeSize == afterSize:  # 已经没有新的状态需要加入
            break

    return T, relations


def convert(K, E, f, S, Z):
    """转换函数，实现构造DFA M=(S,E,D,S0, St)"""
    subsets, D = subSet(f, E, S)  # 调用子集合构造函数，获取子集合和转换关系
    # 对状态子集合的返回进行解析，根据转换关系构造DFA M
    # print(subsets)
    # print(D)
    dfa = {}
    # 重命名的状态
    print("转换得到DFA M=(S,E,D,S0, St)")
    print("有穷集S:")
    dfa["S"] = list(subsets.keys())   # 返回状态集合的排序作为新的命名
    print(dfa["S"])
    # 字母表没有变化
    print("有穷字母表E:")
    dfa["E"] = E
    print(dfa["E"])
    # 转换规则
    print("转换规则D:")
    dfa["D"] = D
    print(dfa["D"])

    # 初始状态：再调用一次闭包进行求解
    for s in list(subsets.keys()):
        if subsets[s] == epsilon_closure(f, S):
            dfa["S0"] = "{}".format(s)
    print("唯一初始状态S0:")
    print(dfa["S0"])

    # 终态   对应课本算法的第五步
    print("终态集St:")
    dfa["St"] = set()
    for i in list(subsets.keys()):
        if (Z & subsets[i]) != set():
            dfa["St"].add(i)
    print(dfa["St"])

    return dfa


def outputToJsonFile(dfa, f):
    """将dfa输出到json文件"""
    # 在进行文件写入的时候出现了问题，提示：Object of type set is not JSON serializable
    # 可能是字典中的某些键后者值不符合json文件的格式
    # 考虑到后面的操作是将DFA最小化还是用json文件读入比较方便
    # 按照它的提示是集合出现的问题，因此将集合类型变为list类型
    dfa["St"] = list(dfa["St"])
    # 写入json文件
    f = open(f, "w")
    dfa_json = json.dumps(dfa, indent=4, sort_keys=False, ensure_ascii=False)
    f.write(dfa_json)
    f.close()


if __name__ == '__main__':
    nfa = 'nfa.json'
    K, E, f, S, Z = readNfa(nfa)  # NFA M = (K, E, f, S, Z),f['i']['arc']表示状态i经过arc弧到达的状态
    dfa = convert(K, E, f, S, Z)
    output = "dfa.json"
    outputToJsonFile(dfa, output)
