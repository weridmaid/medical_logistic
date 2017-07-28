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
import random


def loadData():
    #版本一 没有抽样，全部数据 start
    # train_x = []
    # train_y = []
    # # presCsvname='presFeature_realValue.csv'
    # presCsvname = 'presFeature_onehot.csv'
    # funcCsvname = 'funcFeature.csv'
    # data = data_process.read_csv(presCsvname)
    # labeldata=data_process.read_csv(funcCsvname)
    # num=0
    # for i in data:
    #     if num==0:
    #         i[0]=i[0].replace('﻿', '')
    #     i=[float(item) for item in i]
    #     i.insert(0,1.0)
    #     train_x.append(i)
    #     num+=1
    # num = 0
    # for j in labeldata:
    #     if num==0:
    #         j[0]=j[0].replace('﻿', '')
    #     train_y.append(float(j[0]))
    #     num += 1
    # 版本一 没有抽样，全部数据 end

    #版本二 加了抽样，样本正反例数据平衡 start
    # train_x = []
    # train_y = []
    # rem = []
    # presCsvname='presFeature_realValue.csv'
    # presCsvname = 'presFeature_onehot.csv'
    # presCsvname = 'presFeature_onehot_668.csv'
    # funcCsvname = 'funcFeature.csv'
    # data = data_process.read_csv(presCsvname)
    # labeldata = data_process.read_csv(funcCsvname)
    # # csv内容存放在list才可再读
    # labellist = []
    # num = 0
    # for j in labeldata:
    #     labellist.append(j)
    #     if num == 0:
    #         j[0] = j[0].replace('﻿', '')
    #     # print j
    #     if int(j[0]) == 1:
    #         rem.append(num)
    #         train_y.append(float(j[0]))
    #     num += 1
    # print 'len(rem)', len(rem)
    # print 'len(train_y)', len(train_y)
    #
    # positiveNum = len(rem)*1.3
    # count = 0
    # num = 0
    # for k in labellist:
    #     if num == 0:
    #         k[0] = k[0].replace('﻿', '')
    #     # print k[0]
    #     if k[0] == '0' and count < positiveNum:
    #         # print float(k[0])
    #         rem.append(num)
    #         train_y.append(float(k[0]))
    #         count += 1
    #     num += 1
    # print 'len(rem)2', len(rem)
    # print 'train_y2', len(train_y)
    #
    # num = 0
    # for i in data:
    #     # print num
    #     if num == 0:
    #         i[0] = i[0].replace('﻿', '')
    #     try:
    #         rem.index(num)
    #         i = [float(item) for item in i]
    #         i.insert(0, 1.0)
    #         train_x.append(i)
    #     except:
    #         pass
    #     num += 1
    # print 'train_x', len(train_x)
    # 版本二 加了抽样，样本正反例数据平衡 end


   #版本三 结合了web爬取的数据；处理好的数据集已经正负例平衡
    train_x = []
    train_y = []

    presCsvname = 'presFeature_onehot_combine_QFCS_227t.csv'
    funcCsvname = 'combineFuncFeature_QFCS.csv'
    data = data_process.read_csv(presCsvname)
    labeldata = data_process.read_csv(funcCsvname)

    check=0
    for i in data:
        if check==0:
            i[0] = i[0].replace('﻿', '')
        train_x.append(i[0])
        check+=1
    check = 0
    for j in labeldata:
        if check==0:
            i[0] = i[0].replace('﻿', '')
        train_y.append(j[0])
        check += 1
    # 版本三 结合了web爬取的数据；处理好的数据集已经正负例平衡

    #随机打乱数据集
    index = [i for i in range(len(train_x))]
    random.shuffle(index)
    num=0
    my_x = [1]*len(train_x)
    my_y = [1]*len(train_y)
    for item in index:
        my_x[num]=train_x[item]
        my_y[num] = train_y[item]
        num+=1

    #别人的例子
    # fileIn = open('../Ch05/testSet.txt')
    # for line in fileIn.readlines():
    #     lineArr = line.strip().split()
    #     train_x.append([1.0, float(lineArr[0]), float(lineArr[1])])
    #     train_y.append(float(lineArr[2]))


    # return mat(train_x), mat(train_y).transpose()

    return mat(my_x), mat(my_y).transpose()

## step 1: load data
print "step 1: load data..."
data_x, data_y = loadData()

train_x=data_x
train_y=data_y

test_x = train_x
test_y = train_y

num=1
for i in range(5,6):
   print '迭代次数设置：',i*10
   maxiter=i*10
   for j in range(1,2):
        print '正则化因子lamda设置：',round((float(j)/10),2)
        lamda=round((float(j)/10),2)
        ## step 2: training...
        print "step 2: training..."

        opts = {'alpha': 0.01, 'maxIter': maxiter, 'optimizeType': 'stocGradDescent','lambda':lamda}
        # opts = {'alpha': 0.01, 'maxIter': 100, 'optimizeType': 'smoothStocGradDescent'}
        writecsvname='weight_onehot_QFCS_227_'+str(maxiter)+'_'+str(lamda)+'.csv'
        optimalWeights = logRegression.trainLogRegres(train_x, train_y, opts,writecsvname)

        ## step 3: testing
        print "step 3: testing..."
        accuracy = logRegression.testLogRegres(optimalWeights, test_x, test_y)

        ## step 4: show and write the result
        print "step 4: write the result in test.csv..."
        condiction='%d# 学习因子（尼尔塔）：0.01 最大迭代次数：%d 正则化因子（拉姆达）：%f 初始权重：(-0.01,0.01) acc:%f'%(num,maxiter,lamda,accuracy* 100)
        recordlist=[]
        recordlist.append(condiction)
        # data_process.write_list_in_csv_a('ExResult_1564_realValue.csv',recordlist)
        data_process.write_list_in_csv_a('ExResult_onehot_QFCS.csv', recordlist)
        print 'The classify accuracy is: %.3f%%' % (accuracy * 100)
        num +=1
        # logRegression.showLogRegres(optimalWeights, train_x, train_y)