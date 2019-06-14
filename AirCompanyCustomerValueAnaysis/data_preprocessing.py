#!/usr/bin/env python

# -*- encoding: utf-8 -*-

'''
@Author  :    HY
@Software:   PyCharm
@File    :   data_preprocessing.py
@Time    :   2019/6/9 21:39
@Desc    :

'''
import pandas as pd
import numpy as np

def datapreProcessing():
    #数据清洗——直接删除空值和异常值（看空值和异常值具体的比例来做，否则就要进行均值和插值填充了）
    data=pd.read_csv('data/air_data.csv',sep=',')
    data=data[data['SUM_YR_1'].notnull() & data['SUM_YR_2'].notnull()]
    index1=data['SUM_YR_1']!=0
    index2=data['SUM_YR_2']!=0
    index3=(data['SEG_KM_SUM']==0) & (data['avg_discount']==0)
    data=data[index1 | index2 |index3]


    #属性规约——选择和挖掘目标相关的特征
    data['FFP_DATE']=pd.to_datetime(data['FFP_DATE'])
    data['LOAD_TIME']=pd.to_datetime(data['LOAD_TIME'])

    data['totalTime']=data['LOAD_TIME']-data['FFP_DATE']
    data['PricePerKilo']=( (data['SUM_YR_1']+data['SUM_YR_2'])/data['SEG_KM_SUM'] )
    data['时间间隔差值']=data['MAX_INTERVAL']-data['AVG_INTERVAL']
    data['totalTime']=data['totalTime'].astype(np.int64)/(60*60*24*10**9)
    filter_data=data[['totalTime','PricePerKilo','时间间隔差值','SEG_KM_SUM','avg_discount','FLIGHT_COUNT']]
    print(filter_data[0:10])
    #特征数值差异很大，所以采用标准化进行数据变换
    filter_data=(filter_data-filter_data.mean(axis=0))/(filter_data.std(axis=0))
    print(filter_data[0:10])

    #存储csv文件
    filter_data.to_csv('tmp/filter_data.csv',index=False)

if __name__ == '__main__':
    datapreProcessing()