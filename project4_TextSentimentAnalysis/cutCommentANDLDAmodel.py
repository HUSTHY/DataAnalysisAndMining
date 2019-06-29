#!/usr/bin/env python

# -*- encoding: utf-8 -*-

'''
@Author  :    HY
@Software:   PyCharm
@File    :   cutWordtoVec.py
@Time    :   2019/6/28 17:16
@Desc    :

'''
import pandas as pd
import jieba
import time
from gensim import corpora,models
def cutCommentToVector():
    posInputFile='tmp/posComment.csv'
    negInputFile='tmp/negComment.csv'
    posC=pd.read_csv(posInputFile)['评论']
    negC=pd.read_csv(negInputFile)['评论']
    posCtovec=posC.apply(myCut)
    negCtoVec=negC.apply(myCut)
    # posCtovec=pd.DataFrame(posCtovec)
    # negCtoVec=pd.DataFrame(negCtoVec)
    # posCtovec.to_csv('tmp/posCtovec.csv')
    # negCtoVec.to_csv('tmp/negCtoVec.csv')
    return posCtovec,negCtoVec


def stopWordList():
    stopwordslist=[line.strip() for line in open('stopwords_cn.txt',encoding='utf-8').readlines()]
    return stopwordslist

def myCut(data):
    slist=[]
    s = seg_jieba_sentence(data)
    l = s.strip().split(' ')
    for ele in l:
        slist.append(ele)
    return slist

def seg_jieba_sentence(sentence):
    sentence_seged=jieba.cut(sentence)
    stopWordlist=stopWordList()
    outputStr=''
    for ele in sentence_seged:
        if ele not in stopWordlist:
            outputStr+=ele
            outputStr+=' '
    return outputStr

def topicsLDA(posCtovec, negCtoVec):
    time1 = time.time()
    for num_topic in range(2,4,1):
        # num_topic=2
        pos_dic = corpora.Dictionary(posCtovec)  # 建立词典posCtovec可以视为2位list
        pos_corpus = [pos_dic.doc2bow(ele) for ele in posCtovec]  # 建立预料库
        pos_lda = models.LdaModel(corpus=pos_corpus, num_topics=num_topic, id2word=pos_dic)  # LDA
        # 模型训练
        print('好评主题如下：')
        print(pos_lda.bound(pos_corpus))#困惑度来评价
        for i in range(num_topic):
            print(pos_lda.print_topic(i))

        print('-------------------------------------分割线-------------------------------------')

        neg_dic = corpora.Dictionary(negCtoVec)
        neg_corpus = [neg_dic.doc2bow(ele) for ele in negCtoVec]
        neg_lda = models.LdaModel(corpus=neg_corpus, num_topics=num_topic, id2word=neg_dic)
        print('差评主题如下：')
        print(neg_lda.bound(neg_corpus))
        for i in range(num_topic):
            print(neg_lda.print_topic(i))
    time2 = time.time()
    print('主题分析耗时：%.4f 秒'%(time2-time1))


if __name__ == '__main__':
    time1=time.time()
    posCtovec, negCtoVec=cutCommentToVector()
    time2=time.time()
    print('分词完成：%.4f'%(time2-time1))
    topicsLDA(posCtovec, negCtoVec)