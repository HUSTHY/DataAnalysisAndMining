#!/usr/bin/env python

# -*- encoding: utf-8 -*-

'''
@Author  :    HY
@Software:   PyCharm
@File    :   dataProcess.py
@Time    :   2019/6/21 15:14
@Desc    :

'''
import pandas as pd
import numpy as np
from sklearn.linear_model import LassoLars
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
def dataPreprocess():
    """
        Description:使用最小角回归Lasso算法进行特征压缩
        Params:

        Return:

        Author:
                HY
        Modify:
                2019/6/21 16:37
    """
    inputFile = 'data/data1.csv'
    outputFile = 'tmp/newData.csv'
    data = pd.read_csv(inputFile)
    model=LassoLars(alpha=4,max_iter=1000)
    model.fit(data.iloc[:,0:13],data['y'])
    coefs=model.coef_
    print(coefs)
    # model = Lasso(alpha=1.0,max_iter=1000000,tol=0.00000001)
    # model.fit(data.iloc[:, 0:13], data['y'])
    # coefs=model.coef_
    # print(coefs)
    newColumns=[]
    for index,column in enumerate(data.columns[0:13]):
        if coefs[index]!=0:
            newColumns.append(column)
    newColumns.append(data.columns[13])
    newData=pd.DataFrame(data[newColumns])#用Copy()是为了避免出现链式问题
    newData['year']=list(range(1994,2014,1))
    newData.to_csv(outputFile,index=False)

    # 用岭回归还是选择不了特征变量，没有一个系数会恰好为0
    # model2=Ridge(alpha=100,random_state=1.0,tol=0.0000001,max_iter=100000)
    # model2.fit(data.iloc[:, 0:13], data['y'])
    # coefs2=model2.coef_
    # print('coefs_:',coefs2)


if __name__ == '__main__':
    dataPreprocess()
