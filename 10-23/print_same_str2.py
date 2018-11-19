str_in1 = 'abcdefyux' #input("输入字符串1：")
str_in2 = 'abcrdequx' #input("输入字符串2：")
str_out = "1"
str_list = []
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
print(" ".join(str_list))