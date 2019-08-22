## 输入多行，先输入随机整数的个数，再输入相应个数的整数
## 去除重复的数后，从小到大排列
##n = int(input())
##list = []
##for i in range(n):
##    a = int(input())
##    if list.count(a) < 1:
##        list.append(a)
##
##for j in range(len(list)):
##    index = list.index(min(list))
##    print (list[index])
##    list[index] = 1001
## set() 函数创建一个无序不重复元素集，可进行关系测试，
## 删除重复数据，还可以计算交集、差集、并集等。
## set.add() set.remove() set.update() set.discard()
## sorted(iterable, cmp=None, key=None, reverse=False)
##sorted() 函数对所有可迭代的对象进行排序操作

while True:
    try:
 
        a,res=int(input()),set()
        for i in range(a):res.add(int(input()))
        for i in sorted(res):print(i)
 
    except:
        break
