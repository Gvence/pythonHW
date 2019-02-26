Str = list(input('输入字符串：'))
num = 0

for i in Str:
    if ord(i) - ord('0') <= 9:
        num += 1
        print(i)
print("数量是：" ,num)