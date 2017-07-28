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
def trainLogRegres(train_x, train_y, opts,writecsvname):
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
        weights[n]=weights[n]*random.uniform(-0.01,0.01)
        n+=1
    # print '初始化权值：',weights
    labda= float(opts['lambda'])

    print '正则化系数：', labda
    # optimize through gradient descent algorilthm
    for k in range(maxIter):
    # while(abs(checkerror)>0.01):

        print '正在进行第%d次迭代...'%(k+1)

        if opts['optimizeType'] == 'gradDescent':  # gradient descent algorilthm
            output = sigmoid(train_x * weights)
            error = train_y - output
            weights = weights + alpha * train_x.transpose() * error

        #随机梯度下降
        elif opts['optimizeType'] == 'stocGradDescent':  # stochastic gradient descent
            for i in range(numSamples):
                output = sigmoid(train_x[i, :] * weights)
                error = train_y[i, 0] - output
                #德尔塔w=alpha * train_x[i, :].transpose() * error

                #添加L1范数约束 start
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
                # 添加L1范数约束 end

                # 添加L1范数约束
                weights = weights + alpha * train_x[i,:].transpose() * error-alpha *labda* numlist.transpose()
                # 取消L1范数约束
                # weights = weights + alpha * train_x[i,:].transpose() * error
        else:
            raise NameError('Not support optimize method type!')

    print 'Congratulations, training complete! Took %fs!' % (time.time() - startTime)
    data_process.write_list_in_csv(writecsvname,weights)
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