list1 = [2,3,4,4,3,2,2]
max_num = list1[0]
max_num2 = list1[0]
for i in list1 :
    if i >= max_num:
        max_num = i
for i in list1 :
    if i < max_num:
        if i >= max_num2:
            max_num2 = i
if max_num == max_num2 :
    print('第二大的数字不存在')
else:
    print('max_nuim2:' , max_num2)