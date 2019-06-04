#!/usr/bin/env python

# -*- encoding: utf-8 -*-

'''
@Author  :    HY
@Software:   PyCharm
@File    :   pandas.py
@Time    :   2019/6/3 12:01
@Desc    :

'''
import pandas as pd
import numpy as np
if __name__ == '__main__':
    # 创建DataFrame
    df1= pd.DataFrame(np.random.rand(5,5),columns=['A','B','C','D','E',],index=[1,2,3,4,5])
    print(df1)
    df2=pd.DataFrame(
        {'name':['Hy','Hb','CL','LWR','HUST'],
         'age':[22,15,26,29,28],
         'address': ['hubei','wuhan','guagnz','shagnha','shenz']
         },

        index=[1, 2, 3, 4, 5]
    )
    print(df2)

    #基本操作
    print(df2.index)#访问index
    print(df2.columns)#访问columns
    print(df2.loc[2])#访问2这一行数据
    print(df2.loc[2]['name'])#访问2一行中name列数据

    # 计算
    print(df1.sum())#默认的是列求和
    print(df1.sum(1))#1表示axis=1 行求和

    #行列扩充
    df1['row_sum']=df1.apply(lambda x:x.sum(),axis=1)#列扩充——行相加然后作为一列
    print(df1)
    df1.loc['column_sum']=df1.apply(lambda  y:y.sum())#行扩充
    print(df1)
    df1=df1.append(pd.DataFrame({'A':'CNN','B':'CNN','C':'CNN','D':'CNN','E':'CNN','row_sum':'CNN',},index=[7]))#行扩充
    print(df1)

