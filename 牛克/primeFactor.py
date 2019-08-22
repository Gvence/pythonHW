## 输入一个正整数，按照从小到大的顺序输出它的所有质数的因子
def Isprime(factor):
    R = True
    for i in range(2,factor):
        if factor % i == 0:
            R =  False
    return R

while True:
    try:
        a = int(input())
        out = '0'
        if a >= 2:
            factor = 2
            while a  != 1:
                if a % factor == 0:
                    a /= factor
                    if Isprime(factor):
                        out +=  "%d "%(factor)
                else:
                    factor += 1
            print (out[1:])
        else:
            break
    except:
        break
                
