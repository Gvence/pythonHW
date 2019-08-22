##•连续输入字符串，请按长度为8拆分每个字符串后输出到新的字符串数组；
##•长度不是8整数倍的字符串请在后面补数字0，空字符串不处理。
##输入： abc
##       123456789
##输出：abc00000
##      12345678
##      90000000
##print(data + '0'*(8 - len(data)))  字符串的加法和乘法可以方便字符串操作
def print_8 (data):
    while len(data)> 8 :
        print(data[:8])
        data = data[8:]
    print(data + '0'*(8 - len(data)))
while True:
    print_8(input())
