#!/usr/bin/env python

# -*- encoding: utf-8 -*-

'''
@Author  :    HY
@Software:   PyCharm
@File    :   dataPreProcess.py
@Time    :   2019/6/18 17:45
@Desc    :

'''
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

def dataPreprocess(sql):
    data=dataClean(sql)
    return dataChange(data)




def dataClean(sql):
    """
        Description:数据清洗
        Params:

        Return:

        Author:
                HY
        Modify:
                2019/6/18 18:40
    """
    data=[i for i in sql]
    data=pd.concat(data)
    #删除中间类型的网址
    data1=data[~data['fullURL'].str.contains('midques_')]
    count1=data[data['fullURL'].str.contains('midques_')]['fullURL'].count()


    #删除律师访问的网址
    data2=data1[~(data1['pageTitle']=='法律快车-律师助手')]
    count2=data1[data1['pageTitle']=='法律快车-律师助手']['pageTitle'].count()


    #删除咨询发布成功的网址
    data3=data2[~(data2['pageTitle']=='咨询发布成功')]
    count3=data2[(data2['pageTitle']=='咨询发布成功')]['pageTitle'].count()

    #删除不包含关键字的网址
    data4=data3[((data3['fullURL'].str.contains('ask')) | (data3['fullURL'].str.contains('info')) |(data3['fullURL'].str.contains('fagui')) |(data3['fullURL'].str.contains('lawyer')))]
    count4=data3[~((data3['fullURL'].str.contains('ask')) | (data3['fullURL'].str.contains('info')) |(data3['fullURL'].str.contains('fagui')) |(data3['fullURL'].str.contains('lawyer')))]['fullURL'].count()

    # 删除快搜与免费发布咨询的记录
    count5 = data4[((data4['pageTitle'].str.contains('法律快搜')) | (data4['pageTitle'].str.contains('免费发布法律咨询')))][
        'pageTitle'].count()  # 删除数据记录的条数=38
    data5 = data4[
        ~((data4['pageTitle'].str.contains('法律快搜')) | (data4['pageTitle'].str.contains('免费发布法律咨询')))]  # 2629条记录


    #删除其他类别中带有？的网址 也就是199类型网址带？的
    data6 = data5[~((data5['fullURL'].str.contains('\?')) & (data5['fullURLId'].str.contains('199')))]  # 2627条记录
    count6 = data5[(data5['fullURL'].str.contains('\?')) & (data5['fullURLId'].str.contains('199'))]['fullURL'].count()

    #只包含html的网址
    data7=data6[data6['fullURL'].str.contains('\.html')]
    count7=data6[~data6['fullURL'].str.contains('\.html')]['fullURL'].count()


    #删除重复记录
    data7[data7.duplicated(['realIP','timestamp','fullURL'])][['realIP','timestamp','fullURL']].sort_values(['realIP','timestamp'])
    data8=data7.drop_duplicates()  #删除重复记录


    return data8

def dataChange(data):
    #数据变换
    #网址的特殊性，不同的网址可能属于同一类型网址，要做处理
    datac=data.copy()
    datac['fullURL']=datac['fullURL'].str.replace('_\d\.html','.html')
    datac=datac.drop_duplicates()  #删除重复记录
    finalaData=datac[['realIP','fullURL','fullURLId']]
    resData=finalaData.copy()
    engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/test?charset=utf8')  # 数据库的连接
    resData.to_sql('finalaData',engine,index=False,if_exists='append')

    #属性规约只选择3个属性 IP和网址
    website=datac['fullURL'].unique()#数组类型
    b=sorted(website.tolist())
    print(len(datac['realIP'].unique()))

    #数据量太大了，不能取这么高的维度
    # matrix=pd.DataFrame(np.arange(len(b)*len(datac['realIP'])).reshape(len(datac['realIP']),len(b)), index=datac['realIP'],columns=b)
    realIP=datac['realIP'].unique()
    matrix = pd.DataFrame(np.arange(len(b[:300]) * len(realIP[:10000])).reshape(len(realIP[:10000]), len(b[:300])),
                          index=realIP[:10000], columns=b[:300])

    return matrix ,finalaData



def createIntersetingMat( matrix ,finalaData):
    finalaData=finalaData[0:20000]#控制数量级、原数据集太大了
    for i in range(matrix.index.size):
        temps = []
        for k in range(len(finalaData)):
            if finalaData.iloc[k][0] == matrix.index[i]:
                temps.append(finalaData.iloc[k][1])
        for j in range(matrix.columns.size):
            matrix.iloc[i][j] = 0
            for temp in temps:
                if temp==matrix.columns[j]:
                    matrix.iloc[i][j]=1
                    break
    print(matrix[0:20][0:5])
    return matrix

#构建协同过滤算法
import numpy as np
def Jaccard(a, b):  # 自定义杰卡德相似系数函数，仅对0-1矩阵有效
    return 1.0 * (a * b).sum() / (a + b - a * b).sum()
class Recommender():
    sim = None  # 相似度矩阵
    def similarity(self, x, distance):
        y = np.ones((len(x), len(x)))
        for i in range(len(x)):
            for j in range(len(x)):
                y[i, j] = distance(x[i], x[j])
        return y
    def fit(self, x, distance=Jaccard):  # 训练函数，计算相似度矩阵，其中x为所有用户对所有物品的喜好程度（0-1矩阵）
        self.sim = self.similarity(x, distance)
    def recommend(self, a):  # 推荐函数
        return np.dot(self.sim, a) * (1 - a)


r=Recommender()
result2=r.recommend('''''')#传入数据即可

#向每个IP推荐k个网址
from pandas import DataFrame
def tuijian_result(K, recomMatrix):
    recomMatrix.fillna(0, inplace=True)
    xietong = ['xietong' + str(K) for K in range(1, K + 1)]
    tuijian = DataFrame([], index=recomMatrix.columns, columns=xietong)
    for i in range(len(recomMatrix.columns)):
        temp = recomMatrix.sort_values(by=recomMatrix.columns[i], ascending=False)
        k = 0
        while k < K:
            tuijian.iloc[i, k] = temp.index[k]
            if temp.iloc[k, i] == 0:
                tuijian.iloc[i, k:K] = np.nan
                break
            k = k + 1
        return tuijian

#result2是通过recommend函数算出来的
final_result = tuijian_result(3, result2)


if __name__ == '__main__':
    engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/test?charset=utf8')  # 数据库的连接
    sql = pd.read_sql('all_gzdata', engine, chunksize=10000)  # chunksize每次读取表中的10000条记录，总计83W数据
    matrix ,finalaData=dataPreprocess(sql)
    createIntersetingMat(matrix ,finalaData)
