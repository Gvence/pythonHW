for i in range(1001):
    a = i % 10
    b = int(i/10) % 10
    c= int(i/100) % 10
    if a**3 + b**3 + c**3 == i:
        print(i)
        print(c,b,a)