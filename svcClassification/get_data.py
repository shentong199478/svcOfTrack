import pandas as pd
import numpy as np
import random

import numpy as np
import os,sys
last_path = os.path.dirname(os.getcwd())
sys.path.append(os.path.join(last_path,'data'))


def get_labeldata():
    x = pd. read_excel(os.path.join(last_path,r"data\邮箱标签数据12-23.xls"))
    yangben = x[['fea1','fea2','fea3','fea4','fea5','fea6',"fea7",'fea8','predict']].values
    # print(yangben[0:2,4])
    flag = yangben[:,8]
    lis = list()
    for i in range(1000):
        if int(flag[i]) == -1:
            lis.append(i)
    random.sample(lis,400)
    res = list()
    for i in range(len(flag)):
        if i not in lis:
            res.append(yangben[i,:])
    res = np.array(res)
    permutation = np.random.permutation(res.shape[0])
    shuffled_dataset = res[permutation]
    data = shuffled_dataset[:,:8]
    label =shuffled_dataset[:,-1]
    return data,label

if __name__ == '__main__':
    data,label = get_labeldata()