## 实验一：

### 实验内容

对一个简单语言的子集编制一个一遍扫描的词法分析程序

### 实验要求
（1）待分析的简单语言的词法

1) 关键字

begin if then while do end

2) 运算符和界符

:= + - * / < <= > >= <> = ; ( ) #

3) 其他单词是标识符(ID)和整形常数(NUM)，通过以下正规式定义：

ID=letter(letter|digit)*

NUM=digitdigit*

4) 空格由空白、制表符和换行符组成。空格一般用来分隔ID、NUM、运算符、界符和关键字，词法分析阶段通常被忽略。

 

（2）各种单词符号对应的种别编码

| 单词符号               | 种别码 | 单词符号 | 种别码 |
| ---------------------- | ------ | -------- | ------ |
| begin                  | 1      | :        | 17     |
| if                     | 2      | :=       | 18     |
| then                   | 3      | <        | 20     |
| while                  | 4      | <>       | 21     |
| do                     | 5      | <=       | 22     |
| end                    | 6      | >        | 23     |
| letter(letter\|digit)* | 10     | >=       | 24     |
| digitdigit*            | 11     | =        | 25     |
| +                      | 13     | ;        | 26     |
| -                      | 14     | (        | 27     |
| *                      | 15     | )        | 28     |
| /                      | 16     | #        | 0      |

 

（3）词法分析程序的功能

输入：所给文法的源程序字符串

输出：二元组（syn,token或sum）构成的序列。

syn为单词种别码；

token为存放的单词自身字符串；

sum为整形常数。

例如：对源程序begin x:=9;if x>0 then x:=2*x+1/3;end# 经词法分析后输出如下序列：（1，begin）(10,’x’) (18,:=) (11,9) (26,;) (2,if)……




## 实验二：
### 实验内容
把 NFA 确定化为 DFA 的算法实现 
### 设计内容及要求
构造一程序，实现：将给定的 NFA M(其状态转换矩阵及初态、终
态信息保存在指定文件中)，确定化为 DFA M’。（要先实现ε-CLOSURE 函数和 Ia 函数）。输
出 DFA M’(其状态转换矩阵及初态、终态信息保存在指定文件中)。 

### 程序检验

《编译原理》王生原，第三版，清华大学出版社

P50 图3.6 NFA N的状态图

* 转换前的NFA N如下图所示：

![](D:\2019\Complier\Images\NFA.JPG)

* 转换后的DFA M如下图所示

![](D:\2019\Complier\Images\DFA.JPG)