##第一行输入一个有字母和数字以及空格组成的字符串，第二行输入一个字符。
##输出输入字符串中含有该字符的个数。
##输入：ABCDEF
##      A
##输出：1
a = input()
b = input()
num = 0
for i in a:
    if i == b:
        num +=1
print(num)
#区分大小写
all = input()
one = input()
print (all.count(one))

#不区分大小写
all = input()
one = input()
print (all.lower().count(one.lower()))
