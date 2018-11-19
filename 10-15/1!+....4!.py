i = 1
sum = 0

def factorial(i):
    s = 1
    for n in range(i):
        s *= i
    return s

while (i <= 4):
    sum += factorial(i)
    i += 1
print(sum)
