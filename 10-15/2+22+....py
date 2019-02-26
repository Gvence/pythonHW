m = int(input("请输入m:"))
n = int(input("请输入n:"))
i = 1
sum = 0
temp = m
while ( i <= n):
    sum += m
    m = 10*m + temp
    i += 1
print(sum)
