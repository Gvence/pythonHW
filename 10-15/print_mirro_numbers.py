num = 1000
def confirm(i):
    a = i % 10
    b = i
    while (b >= 10):
        b //= 10
    if a == b:
        return True
    else:
        return False
for i in range(num+1):
    if confirm(i) == True:
        print(i)