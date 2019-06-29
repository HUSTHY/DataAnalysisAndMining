#!/usr/bin/env python

# -*- encoding: utf-8 -*-

'''
@Author  :    HY
@Software:   PyCharm
@File    :   commentSentimentAnalysis.py
@Time    :   2019/6/26 22:04
@Desc    :

'''
import pandas as pd
from snownlp import SnowNLP
import time
def SnowNLPForSentimentAnalysis():
    inputFile='tmp/commentData.csv'
    data=pd.read_csv(inputFile)
    index=[]
    values=[]
    for i in range(len(data)):
        s=SnowNLP(str(data.iloc[i][1]))#每一条评论分词
        for j in s.sentences:
            index.append(i)
            values.append(SnowNLP(j).sentiments)#每个词的情感得分
    scores=pd.DataFrame({'ID':index,'score':values})
    average=scores.groupby('ID')['score'].mean()#均值代表每条评论的得分
    data['sentimentsScore']=average
    print(data)
    data.to_csv('tmp/sentimentsScore.csv')
    posData = data[['评论', 'sentimentsScore']][(data['sentimentsScore'] >= 0.7)]
    negData = data[['评论', 'sentimentsScore']][(data['sentimentsScore'] <= 0.3)]
    posData.to_csv('tmp/posComment.csv')
    negData.to_csv('tmp/negComment.csv')
    return data


if __name__ == '__main__':
    time1=time.time()
    SnowNLPForSentimentAnalysis()
    time2=time.time()
    print('情感分析Finished in %.4f'%(time2-time1))