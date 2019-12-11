# _*_coding:utf-8_*_
# file: ReversePolishNotation.py
def reversePolishNotation(expression):
    stack = []   # 初始化空栈
    result = []
    for ch in expression:
        if ch.isnumeric():
            result.append(ch)
        else:
            if len(stack) == 0: # 空栈就将符号直接推入
                stack.append(ch)
            elif ch in '(*/':
                stack.append(ch)
            elif ch is ')':  # 出栈直到遇到(
                c = stack.pop()
                while c is not '(':
                    result.append(c)
                    c = stack.pop()
            elif ch in '+-' and stack[-1] in '*/':
                # 如果栈中没有左括号就将所有出栈，加入结果
                if stack.count('(') == 0:
                    while stack:
                        result.append(stack.pop())
                else:
                    t = stack.pop()
                    while t != '(':
                        result.append(t)
                        t = stack.pop()
                    stack.append('(')
                stack.append(ch)   # 出栈完成后将当前的入栈
            else:
                stack.append(ch)
    # 表达式遍历完成后将栈清空
    while stack:
        result.append(stack.pop())
    return "".join(result)

if __name__ == "__main__":
    expression = "1+(2*3-4)+5*6"
    result = reversePolishNotation(expression)
    print(result)