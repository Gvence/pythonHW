str_in1 = 'abcdefyux' #input("输入字符串1：")
str_in2 = 'abcdeqyux' #input("输入字符串2：")
str_out = "1"
str_list = []
length = 4
longest_list = []
last_statioin = -1
for i in str_in1:
    if str_in2.find(i) >= 0 :
        if str_in2.find(i) != last_statioin + 1 :
            str_list.append(str_out[1:])
            str_out = "1"
        last_statioin = str_in2.find(i)
        str_out += i
        if i == str_in1[len(str_in1)-1] and str_out != "1":
            str_list.append(str_out[1:])
            str_out = "1"
for j in str_list:
    if len(j) >= length:
        longest_list.append(j)
if len(longest_list)>0:
    print(" ".join(longest_list))
else:
    print("不存在")