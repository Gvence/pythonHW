Str = input('输入字符串:')
index = input('输入想要查找的字符：')
times = 0
while( Str.find(index) >= 0 ):
    Str = Str.replace(index,'xxx',1)
    times += 1
print(times)