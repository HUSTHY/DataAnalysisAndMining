#!/usr/bin/env python

# -*- encoding: utf-8 -*-

'''
@Author  :    HY
@Software:   PyCharm
@File    :   getTextData.py
@Time    :   2019/6/25 17:26
@Desc    :

'''
import pandas as pd
import time
def getTextDataFromCSV():
    inputFile='data/huizong.csv'
    data=pd.read_csv(inputFile,encoding='utf-8')
    newData=data[['评论']][data['品牌']=='美的']
    return newData

def DataUnique(data):
    l1=len(data)
    data=pd.DataFrame(data['评论'].unique(),columns=['评论'])
    l2=len(data)
    # print('删除重复评论条数：%d'%(l1-l2))
    data = filterlessThan4Words(data)
    return data.reset_index(drop=True)
def cutWordFrontAndBack(data):
    for j in range(len(data)):#正向压缩去词
        string = str(data.iloc[j][0])
        temp = string.strip().strip('\n')
        charlist = list(temp)
        str1=cutAlgorithm(charlist)
        data.loc[j]=str1
    for j in range(len(data)):#反向压缩去词
        string = str(data.iloc[j][0])
        temp = string.strip().strip('\n')
        charlist = list(temp)[:: -1]#反转
        str1 = cutAlgorithm(charlist)
        data.loc[j] = str1[::-1]#反转
    data=filterlessThan4Words(data)
    data.to_csv('tmp/commentData.csv')
    return data
def cutAlgorithm(charlist):
    """
        Description:压缩去词算法、仅仅包含开头和结尾的重复。中间重复不包含。
        有7条准则
        Params:

        Return:

        Author:
                HY
        Modify:
                2019/6/28 15:54
    """
    list1 = ['']
    list2 = ['']
    del1 = []
    flag = ['']
    i = 0
    while i < len(charlist):
        if charlist[i] == list1[0]:
            if list2 == ['']:
                list2[0] = charlist[i]
            else:
                if list2 == list1:
                    t = len(list1)
                    m = 0
                    while m < t:
                        del1.append(i - m - 1)
                        m += 1
                    list2 = ['']
                    list2[0] = charlist[i]
                else:
                    list1 = ['']
                    list2 = ['']
                    flag = ['']
                    list1[0] = charlist[i]
                    flag[0] = i
        else:
            if (list1 == list2) and (list1 != ['']) and (list2 != ['']):
                if len(list1) > 2:
                    t = len(list1)
                    m = 0
                    while m < t:
                        del1.append(i - m - 1)
                        m += 1
                    list1 = ['']
                    list2 = ['']
                    list1[0] = charlist[i]
                    flag[0] = i
            else:
                if list2 == ['']:
                    if list1 == ['']:
                        list1[0] = charlist[i]
                        flag[0] = i
                    else:
                        list1.append(charlist[i])
                        flag.append(i)
                else:
                    list2.append(charlist[i])
        i += 1
        if (i == len(charlist)):
            if list2 == list1:
                t = len(list1)
                m = 0
                while m < t:
                    del1.append(i - m - 1)
                    m += 1
                if len(del1) + len(flag) != len(charlist):  # 保证完全重复的字符保留一个重复单元
                    m = 0
                    while m < t:
                        del1.append(flag[m])
                        m += 1
    a = sorted(del1)
    t = len(a) - 1
    while (t >= 0):
        del charlist[a[t]]
        t = t - 1
    str1 = "".join(charlist)
    str2 = str1.strip()
    return str2


def filterlessThan4Words(data):
    delIndexs = []
    for i in range(len(data)):
        if len(str(data.iloc[i][0])) < 4:  # 过滤长度4以下的评论
            delIndexs.append(i)
    data.drop(index=delIndexs, inplace=True)
    # print(data)
    return data.reset_index(drop=True)

if __name__ == '__main__':
    data=getTextDataFromCSV()
    data=DataUnique(data)
    # data=pd.DataFrame({'评论':['非常好非常好非常好非常好非常好非常好非常好非常好非常好非常好!','可以，可以可以可以可以可以','很好很好很好','非常棒的体验我是黄洋你好呀贵贵贵贵贵贵贵',
    #                          'aaaaaaaaaaaaaa,我是美的的忠实客户','5555555555555']},index=[0,1,2,3,4,5])
    # data = pd.DataFrame(
    #     {'评论': ['非常棒的体验我是黄洋你好呀贵贵贵贵贵贵贵']}, index=[0])
    # print(data)
    time1=time.time()
    newdata=cutWordFrontAndBack(data)
    time2 = time.time()
    print('压缩去词耗时：%.4f seconds'%(time2-time1))
