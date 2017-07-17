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
import data_process
import random




# calculate the sigmoid function
def sigmoid(inX):
    return 1.0 / (1 + exp(-inX))


# train a logistic regression model using some optional optimize algorithm
# input: train_x is a mat datatype, each row stands for one sample
#        train_y is mat datatype too, each row is the corresponding label
#        opts is optimize option include step and maximum number of iterations
def trainLogRegres(train_x, train_y, opts):
    # calculate training time
    startTime = time.time()
    numSamples, numFeatures = shape(train_x)
    print '样本数量：',numSamples
    print '每个实例有多少维特征：', numFeatures
    alpha = opts['alpha']
    print '梯度下降学习因子：',alpha
    maxIter = opts['maxIter']
    print '最大迭代次数：', maxIter
    weights = ones((numFeatures, 1))
    #把权重随机初始化在（-0.01,0.01之间）
    n=0
    for i in weights:
        weights[n]=weights[n]*random.uniform(-0.1,0.1)
        n+=1
    print '初始化权值：',weights
    labda= float(opts['lambda'])
    print '正则化系数：', labda
    # optimize through gradient descent algorilthm
    for k in range(maxIter):
        print '正在进行第%d次迭代...' % (k+1)
        if opts['optimizeType'] == 'gradDescent':  # gradient descent algorilthm
            output = sigmoid(train_x * weights)
            error = train_y - output
            weights = weights + alpha * train_x.transpose() * error

        #随机梯度下降
        elif opts['optimizeType'] == 'stocGradDescent':  # stochastic gradient descent
            for i in range(numSamples):
                # print 'train_x[i, :]',train_x[i, :]
                output = sigmoid(train_x[i, :] * weights)
                # print 'train_y[i, 0]',train_y[i, 0]
                error = train_y[i, 0] - output
                #德尔塔w=alpha * train_x[i, :].transpose() * error
                numlist=[]
                for num in weights:
                    # print 'num',num
                    if num >0:
                        numlist.append(1)
                    elif num<0:
                        numlist.append(-1)
                    else:
                        numlist.append(0)
                numlist=mat(numlist)
                # print 'numlist',numlist
                # print 'numlist.transpose()', numlist.transpose()
                # print 'train_x[i, :].transpose()', train_x[i, :].transpose()
                weights = weights + alpha * train_x[i, :].transpose() * error-alpha *labda* numlist.transpose()


        elif opts['optimizeType'] == 'smoothStocGradDescent':  # smooth stochastic gradient descent
            # randomly select samples to optimize for reducing cycle fluctuations
            dataIndex = range(numSamples)
            for i in range(numSamples):
                alpha = 4.0 / (1.0 + k + i) + 0.01
                randIndex = int(random.uniform(0, len(dataIndex)))
                output = sigmoid(train_x[randIndex, :] * weights)
                error = train_y[randIndex, 0] - output
                weights = weights + alpha * train_x[randIndex, :].transpose() * error
                del (dataIndex[randIndex])  # during one interation, delete the optimized sample
        else:
            raise NameError('Not support optimize method type!')

    print 'Congratulations, training complete! Took %fs!' % (time.time() - startTime)
    data_process.write_list_in_csv('weights_0.1.csv',weights)
    return weights


# test your trained Logistic Regression model given test set
def testLogRegres(weights, test_x, test_y):
    numSamples, numFeatures = shape(test_x)
    matchCount = 0
    for i in xrange(numSamples):
        predict = sigmoid(test_x[i, :] * weights)[0, 0] > 0.5
        if predict == bool(test_y[i, 0]):
            matchCount += 1
    accuracy = float(matchCount) / numSamples
    return accuracy


# show your trained logistic regression model only available with 2-D data
def showLogRegres(weights, train_x, train_y):
    # notice: train_x and train_y is mat datatype
    numSamples, numFeatures = shape(train_x)
    if numFeatures != 3:
        print "Sorry! I can not draw because the dimension of your data is not 2!"
        return 1

        # draw all samples
    for i in xrange(numSamples):
        if int(train_y[i, 0]) == 0:
            plt.plot(train_x[i, 1], train_x[i, 2], 'or')
        elif int(train_y[i, 0]) == 1:
            plt.plot(train_x[i, 1], train_x[i, 2], 'ob')

            # draw the classify line
    min_x = min(train_x[:, 1])[0, 0]
    max_x = max(train_x[:, 1])[0, 0]
    weights = weights.getA()  # convert mat to array
    y_min_x = float(-weights[0] - weights[1] * min_x) / weights[2]
    y_max_x = float(-weights[0] - weights[1] * max_x) / weights[2]
    plt.plot([min_x, max_x], [y_min_x, y_max_x], '-g')
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()