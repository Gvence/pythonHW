n = int(input('day number :'))
num = []
for i in range(n+1):
    num.append(1)
def caculate (days):
    if days > 0:
        for i  in range(2,days + 1):
            num[i] = num[i-1]+ num[i-2]
            print('Day:', i, 'Cell num:', num)
        return num[days]
    else:
        return 0
caculate(n)
print('Day:',len(num)-1 , 'Cell num:', num[len(num) - 1])