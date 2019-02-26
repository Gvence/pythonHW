list_x = [1,2,3,2,1,-1,4,5,2]
num_1 = list_x[0]
out_put = []
up = False
dow = False
for i in list_x :
    if i > num_1 :
        out_put.append(str(num_1))
        if dow :
            out_put.append(("||"))
            out_put.append(str(num_1))
            dow = False
        up = True
    elif i == num_1 :
        continue
    elif i < num_1 :
        out_put.append(str(num_1))
        if up :
            out_put.append(("||"))
            out_put.append(str(num_1))
            up = False
        dow = True
    num_1 = i
space = " "
newvar = space.join(out_put)
print(newvar,list_x[len(list_x)-1])
