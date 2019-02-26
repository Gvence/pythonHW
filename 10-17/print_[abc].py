Str = input('输入字符串:')
L_c = Str.find('[')
R_c = Str.find(']')
if L_c <= R_c & L_c >= 0 & R_c >= 0:
    print(Str[L_c+1 : R_c])
else:
    print('不存在\" [] \"')
