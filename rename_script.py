import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
PATH = os.getcwd()

if __name__ == '__main__':
    src_path = PATH + '\\source\\'
    tar_path = PATH + '\\target\\'
    file_list = os.listdir(src_path)
    print(file_list)
    for i in file_list:
        print('sourceName : %s',i)
        old_file = os.path.join(src_path,i)
        new_file = os.path.join(tar_path,i[:-3]+'aaa')
        os.rename(old_file, new_file)
    # for i in range(100):
    #     file = open(path+'\\source\\'+str(i)+'.txt', 'w')
    #     file.write(str(i)+'\n')
    #     file.close()