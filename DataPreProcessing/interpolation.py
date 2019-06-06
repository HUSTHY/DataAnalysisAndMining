#!/usr/bin/env python

# -*- encoding: utf-8 -*-

'''
@Author  :    HY
@Software:   PyCharm
@File    :   interpolation.py
@Time    :   2019/6/6 14:39
@Desc    :    空值、异常值进行插值处理

'''
import pandas as pd
from scipy.interpolate import lagrange
def dataInterpolation(fileName):
    data=pd.read_excel(fileName)
    columns=data.columns
    data.loc[(data[columns[1]]<400) | (data[columns[1]]>5000),columns[1]]=None#过滤大于5000小于400的异常值
    print(data[columns[1]])
    def ployinterplate(vec,n,k=5):#拉格朗日插值，n插值点
        y = vec[list(range(n - k, n)) + list(range(n + 1, n + k + 1))]#取插值的需要的数据
        y=y[y.notnull()]#去空
        res= lagrange(y.index,list(y))(n)
        return res

    for i in range(len(data[columns[1]])):
        if pd.isnull(data.loc[i,columns[1]]):#判断是否为空值，然后就插值处理。
            data.loc[i,columns[1]]=ployinterplate(data.loc[:,columns[1]],i)
    print(data[columns[1]])

    # data[columns[1]][(data[columns[1]] < 400) | (data[columns[1]] > 5000)] = None  # 过滤大于5000小于400的异常值——会出现CopyWarning
    data.loc[(data[columns[1]] < 400) | (data[columns[1]] > 5000), columns[1]] = None  # 过滤大于5000小于400的异常值

    def ployMean(vec,n,k=5):#均值处理，n插值点
        y = vec[list(range(n - k, n)) + list(range(n + 1, n + k + 1))]#取插值的需要的数据
        y=y[y.notnull()]#去空
        res= y.sum()/10
        return res

    for i in range(len(data[columns[1]])):
        if pd.isnull(data[columns[1]][i]):#判断是否为空值，然后做均值处理。
            data.loc[i,columns[1]]=ployMean(data[columns[1]],i)
    print(data[columns[1]])
    outputFile='tmp/sale.xls'
    data.to_excel(outputFile)

if __name__ == '__main__':
    dataInterpolation('data/catering_sale.xls')