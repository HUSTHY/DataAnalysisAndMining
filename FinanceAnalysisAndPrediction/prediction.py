#!/usr/bin/env python

# -*- encoding: utf-8 -*-

'''
@Author  :    HY
@Software:   PyCharm
@File    :   prediction.py
@Time    :   2019/6/21 17:15
@Desc    :

'''
from FinanceAnalysisAndPrediction.GM11 import GM11
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPRegressor

def prediction():
    """
        Description:做预测：第一个适用灰色预测得到一系列的自变量的预测值；二是适用神经网络模型——进行因变量的回归预测
        Params:

        Return:

        Author:
                HY
        Modify:
                2019/6/21 23:06
    """
    inputFile='tmp/newData.csv'
    data=pd.read_csv(inputFile)
    data.drop(['year'],axis=1,inplace=True)
    data.index=list(range(1994,2014,1))
    columns=data.columns
    data.loc[2014]=None;data.loc[2015]=None
    for i in columns[0:-1]:
        # fuc=GM11(data[i][0:20].as_matrix())[0]#得到灰色预测模型函数
        # C=GM11(data[i][0:20].as_matrix())[4]
        fuc = GM11(data[i][0:20].values)[0]  # 得到灰色预测模型函数——适用于小数据量、指数增长
        C = GM11(data[i][0:20].values)[4]
        data[i][2014]=fuc(len(data)-1)
        data[i][2015]=fuc(len(data))
        data[i]=np.round(data[i],2)

    MLPModel = MLPRegressor(hidden_layer_sizes=(12, 12, 12), activation='relu', solver='lbfgs', max_iter=10000,
                            tol=0.0000001, alpha=0.00001, random_state=1)#使用人工神经网络回归预测——hidden_layer_sizes表示3个隐含层12/12/12个神经元

    #数据标准化——特征数据
    data_mean=data[columns[0:]][0:22].mean()
    data_std=data[columns[0:]][0:22].std()
    data_train_x=(data[columns[0:-1]][0:20]-data_mean[0:-1])/data_std[0:-1]
    data_test_x = (data[columns[0:-1]][0:22] - data_mean[0:-1]) / data_std[0:-1]
    data_train_y=(data[columns[-1]][0:20]-data_mean[-1])/data_std[-1]

    MLPModel.fit(data_train_x,data_train_y)
    data['yPredic']=MLPModel.predict(data_test_x)*data_std[-1]+data_mean[-1]
    rmse=RMSE(data['y'][0:20],data['yPredic'][0:20])#均方根误差
    print(rmse)
    rr=MLPModel.score(data_train_x,data_train_y)#决定系数越接近1越好
    print(rr)

    #画出图像
    import matplotlib.pyplot as plt
    plt.plot(range(1994,2014),data['y'][0:20],c='b',label='True',linestyle='--')
    plt.scatter(range(1994,2014),data['y'][0:20],s=50,alpha=0.8,color='black')
    plt.legend()
    plt.show()
    plt.plot(range(1994, 2016), data['yPredic'], c='r', label='Predict',linestyle='--')
    plt.scatter(range(1994, 2016), data['yPredic'],s=50,alpha=0.8 ,color='purple')
    plt.legend()
    plt.show()


def RMSE(y_pre,y):
    return np.sqrt(np.mean((y_pre-y)**2))
if __name__ == '__main__':
    prediction()