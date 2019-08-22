## 输出最后一个单词的长度
## 输入： hello world

a=input()
print(a)
print(a.split())
print(len(a[-1]) if len(a)>1 else len(a[0]))
