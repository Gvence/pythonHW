str =list( input("请输入字符串："))
n = int(input("请输入移动幅度："))
temp = str[:]#把一个列表的值给另一列表不能用temp = str,要用temp = str[:]
length = len(str)
print(length)
i = 0
while(i < length):
    if i + n >= length :
        temp[i + n - length ] = str[i]
    else :
        temp[i + n] = str[i]
    i += 1
print(temp)