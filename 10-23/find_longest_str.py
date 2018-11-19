str_in1 = 'abcdefyux' #input("输入字符串1：")
str_in2 = 'abcrdeqyux' #input("输入字符串2：")
str_out = "1"
str_list = []
length = 0
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
        length = len(j)
for k in str_list:
    if length == len(k):
        longest_list.append(k)
print(" ".join(longest_list))