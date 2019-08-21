##数据表记录包含表索引和数值，
##请对表索引相同的记录进行合并，
##即将相同索引的数值进行求和运算，
##输出按照key值升序进行输出。
##先输入键值对的个数
##然后输入成对的index和value值，以空格隔开
##输出合并后的键值对（多行）
listlength = int(input())
lis = []
for i in range(listlength):
    lis.append(0)
for i in range(listlength):
    index, value = map(int, input().split())
    lis[index] += value
index = 0
for i in lis:
    if i:
        print(index, i)
    index += 1
