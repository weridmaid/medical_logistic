# coding=utf-8
import data_process
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

train_x = []
train_y = []
rem=[]
# presCsvname='presFeature_realValue.csv'
presCsvname = 'presFeature_onehot.csv'
funcCsvname = 'funcFeature.csv'
data = data_process.read_csv(presCsvname)
labeldata = data_process.read_csv(funcCsvname)
#csv内容存放在list才可再读
labellist=[]
num = 0
for j in labeldata:
    labellist.append(j)
    if num == 0:
        j[0] = j[0].replace('﻿', '')
    # print j
    if int(j[0])==1:
        rem.append(num)
        train_y.append(float(j[0]))
    num += 1
print 'len(rem)1',len(rem)
print 'len(train_y)1',len(train_y)

positiveNum=len(rem)+1
count=0
num=0
for k in labellist:
    if num == 0:
        k[0] = k[0].replace('﻿', '')
    # print k[0]
    if k[0]=='0' and count<positiveNum:
        # print float(k[0])
        rem.append(num)
        train_y.append(float(k[0]))
        count+=1
    num += 1
print 'len(rem)2', len(rem)
print 'train_y2',len(train_y)

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
print 'train_x',len(train_x)