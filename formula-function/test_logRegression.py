# coding=utf-8
#################################################
# 代码原作者logRegression: Logistic Regression
# Author : zouxy
# Date   : 2014-03-02
# HomePage : http://blog.csdn.net/zouxy09
# Email  : zouxy09@qq.com
#################################################
#################################################
# 修改logRegression: Logistic Regression
# Author : zsy
# Date   : 2017-7-14
#################################################

from numpy import *
import matplotlib.pyplot as plt
import time
import logRegression
import data_process


def loadData():
    train_x = []
    train_y = []
    presCsvname='presFeature_realValue.csv'
    # presCsvname = 'presFeature_onehot.csv'
    funcCsvname = 'funcFeature.csv'
    data = data_process.read_csv(presCsvname)
    labeldata=data_process.read_csv(funcCsvname)
    num=0
    for i in data:
        if num==0:
            i[0]=i[0].replace('﻿', '')
        i=[float(item) for item in i]
        i.insert(0,1.0)
        train_x.append(i)
        num+=1
    num = 0
    for j in labeldata:
        if num==0:
            j[0]=j[0].replace('﻿', '')
        train_y.append(float(j[0]))
        num += 1

    #别人的例子
    # fileIn = open('../Ch05/testSet.txt')
    # for line in fileIn.readlines():
    #     lineArr = line.strip().split()
    #     train_x.append([1.0, float(lineArr[0]), float(lineArr[1])])
    #     train_y.append(float(lineArr[2]))
    return mat(train_x), mat(train_y).transpose()


## step 1: load data
print "step 1: load data..."
train_x, train_y = loadData()
test_x = train_x
test_y = train_y

## step 2: training...
print "step 2: training..."
opts = {'alpha': 0.01, 'maxIter': 10, 'optimizeType': 'stocGradDescent','lambda':0.3}
# opts = {'alpha': 0.01, 'maxIter': 100, 'optimizeType': 'smoothStocGradDescent'}
optimalWeights = logRegression.trainLogRegres(train_x, train_y, opts)

## step 3: testing
print "step 3: testing..."
accuracy = logRegression.testLogRegres(optimalWeights, test_x, test_y)

## step 4: show the result
print "step 4: show the result..."
print 'The classify accuracy is: %.3f%%' % (accuracy * 100)
logRegression.showLogRegres(optimalWeights, train_x, train_y)