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
    # presCsvname='presFeature_realValue.csv'
    presCsvname = 'presFeature_onehot.csv'
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

for i in range(2,11):
   print '迭代次数设置：',i*10
   maxiter=i*10
   for j in range(1,11):
        print '正则化因子lamda设置：',round((float(j)/10),2)
        lamda=round((float(j)/10),2)
        ## step 2: training...
        print "step 2: training..."

        opts = {'alpha': 0.01, 'maxIter': maxiter, 'optimizeType': 'stocGradDescent','lambda':lamda}
        # opts = {'alpha': 0.01, 'maxIter': 100, 'optimizeType': 'smoothStocGradDescent'}
        word='weight'+str(maxiter)+'_'+str(lamda)+'csv'
        writecsvname='.csv'
        optimalWeights = logRegression.trainLogRegres(train_x, train_y, opts,writecsvname)

        ## step 3: testing
        print "step 3: testing..."
        accuracy = logRegression.testLogRegres(optimalWeights, test_x, test_y)

        ## step 4: show and write the result
        print "step 4: write the result in ExResult.csv..."
        condiction='学习因子（尼尔塔）：0.01 最大迭代次数：%d 正则化因子（拉姆达）：%f 初始权重：1'%(maxiter,lamda)
        recordlist=[]
        recordlist.append(condiction)
        recordlist.append(accuracy* 100)
        data_process.write_list_in_csv_a('ExResult.csv',recordlist)
        print 'The classify accuracy is: %.3f%%' % (accuracy * 100)
        # logRegression.showLogRegres(optimalWeights, train_x, train_y)