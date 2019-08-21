##输入一个int型整数，按照从右向左的阅读顺序，返回一个不含重复数字的新的整数。
##输入一个int型整数
##按照从右向左的阅读顺序，返回一个不含重复数字的新的整数
###!/usr/bin/python
### -*- coding: UTF-8 -*-
## 
##str = "-";
##seq = ("a", "b", "c"); # 字符串序列
##print str.join( seq );
##a-b-c
a = input()
b = []
for i in a[::-1]:
    if i not in b:
        b.append(i)
print(''.join(b))
