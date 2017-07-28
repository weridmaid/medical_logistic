# coding=utf-8
import data_process
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.cross_validation import train_test_split, cross_val_score
from sklearn.externals import joblib
import random

# 版本二 加了抽样，样本正反例数据平衡 start
train_x = []
train_y = []
rem = []
# presCsvname='presFeature_realValue.csv'
presCsvname = 'presFeature_onehot_668.csv'
funcCsvname = 'funcFeature.csv'
data = data_process.read_csv(presCsvname)
labeldata = data_process.read_csv(funcCsvname)
# csv内容存放在list才可再读
labellist = []
num = 0
for j in labeldata:
    labellist.append(j)
    if num == 0:
        j[0] = j[0].replace('﻿', '')
    # print j
    if int(j[0]) == 1:
        rem.append(num)
        train_y.append(float(j[0]))
    num += 1
print 'len(rem)1', len(rem)
print 'len(train_y)1', len(train_y)

positiveNum = len(rem) * 1.3
count = 0
num = 0
for k in labellist:
    if num == 0:
        k[0] = k[0].replace('﻿', '')
    # print k[0]
    if k[0] == '0' and count < positiveNum:
        # print float(k[0])
        rem.append(num)
        train_y.append(float(k[0]))
        count += 1
    num += 1
print 'len(rem)2', len(rem)
print 'train_y2', len(train_y)

num = 0
for i in data:
    # print num
    if num == 0:
        i[0] = i[0].replace('﻿', '')
    try:
        rem.index(num)
        i = [float(item) for item in i]
        i.insert(0, 1.0)
        train_x.append(i)
    except:
        pass
    num += 1
print 'train_x', len(train_x)

# 随机打乱数据集
index = [i for i in range(len(train_x))]
random.shuffle(index)
num = 0
my_x = [1] * len(train_x)
my_y = [1] * len(train_y)
for item in index:
    my_x[num] = train_x[item]
    my_y[num] = train_y[item]
    num += 1
    # train_x = train_x[index]
    # train_y = train_y[index]

    # 版本二 加了抽样，样本正反例数据平衡 end


# df = pd.read_csv('mlslpic/sms.csv')
# X_train_raw, X_test_raw, y_train, y_test = train_test_split(df['message'], df['label'])

vectorizer = TfidfVectorizer()
X_train =  my_x
X_test = my_x
classifier = LogisticRegression(penalty='l1',C=100,max_iter=50)
rf=classifier.fit(X_train, my_y)

print 'rf',rf
#保存模型
joblib.dump(rf,'rf.model')

#加载模型
RF=joblib.load('rf.model')

#应用模型进行预测
# result=RF.predict(thsDoc)

scores = cross_val_score(classifier, X_train, my_y, cv=5)
print '准确率：',np.mean(scores), scores
precisions = cross_val_score(classifier, X_train, my_y, cv=5, scoring='precision')
print '精确率：',np.mean(precisions), precisions
recalls = cross_val_score(classifier, X_train,my_y, cv=5, scoring='recall')
print '召回率：', np.mean(recalls), recalls

