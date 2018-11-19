a = input('请输入：')
num = 0
star = 0
end = 0
word_list = []
for i in a:
    if i == ' ' or i == ',' or i == ';' or i == ':' or i == '!':
        end = num
    if star == 0 and end != 0 :
        word_list.append(a[star:end])
        star = end
    if star!=0 and end != 0 and star != end :
        word_list.append(a[star+1:end])
        star = end
    num += 1
print(len(word_list),word_list)