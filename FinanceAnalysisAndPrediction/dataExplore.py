#!/usr/bin/env python

# -*- encoding: utf-8 -*-

'''
@Author  :    HY
@Software:   PyCharm
@File    :   dataExplore.py
@Time    :   2019/6/21 10:51
@Desc    :

'''
import pandas as pd
import numpy as np

def dataExpolre():
    """
        Description:得到数据的整体性描述，相关分析；大致得出要选取哪些数据
        Params:

        Return:

        Author:
                HY
        Modify:
                2019/6/21 15:12
    """
    inputFile='data/data1.csv'
    data=pd.read_csv(inputFile)
    data_describe=data.describe()#得到整个数据一个描叙性的结果
    np.round(data_describe,4)
    print(data_describe.T)
    r=[data.min(),data.max(),data.mean(),data.std()]#得到方差、均值、最大值、最小值等
    r=pd.DataFrame(r,index=['Min','Max','Mean','STD']).T
    np.round(r,4)#保留4位小数
    print(r)
    corr=data.corr(method='pearson')#变量之间的相系数
    np.round(corr,4)
    print(corr)

if __name__ == '__main__':
    dataExpolre()