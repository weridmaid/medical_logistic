# coding=utf-8
import re
import sys
import dataFeatureValue
import data_process
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    print '从训练好的logistic模型参数中找出占主导作用的药物...'
    allresults=[]
    qq = 1
    for i in range(1, 2):
        print '迭代次数设置：', i * 10
        maxiter = i * 10
        for j in range(0, 4):
            # NOL1_weight_onehot_QRJD_s0.1_50.csv
            # readcsvname = '../formulaData_Experiment/NOL1_weight_onehot_QRJD_s0.1_'+str(maxiter)+'.csv'
            if(qq==1):
                lamda=0.7
            if (qq == 2):
                lamda = 1.3
            if(qq==3):
                lamda=2.7
            if(qq==4):
                lamda=4.3
            print 'lamda',lamda
            readcsvname = '../formulaData_Experiment/weight_onehot_QRJD_s0.1_500_'+str(lamda)+'.csv'
            weightdata=data_process.read_csv(readcsvname)
            qq+=1

            csvname = '../formulaData_1/QRJD_medical_count.csv'
            medicaldata=data_process.read_csv(csvname)
            medicallist=[]
            importantMedical=[]
            weightlist=[]
            for item in medicaldata:
                medicallist.append(item[0])

            weightlist=[]
            num = 0
            for item in weightdata:
                if num!=0:
                    zz=[]
                    item[0]=item[0].replace('[[','')
                    item[0] = item[0].replace(']]', '')
                    item[0] = item[0].replace('﻿', '')
                    # print 'zz',item[0]
                    zz.append(num)
                    zz.append(float(item[0]))
                    weightlist.append(zz)
                num += 1

            weightlist = sorted(weightlist, key=lambda x: x[1], reverse=True)

            for i in range(0,10):
                zz=[]
                zz.append(medicallist[weightlist[i][0]-1])
                allresults.append(medicallist[weightlist[i][0]-1])
                zz.append(weightlist[i][1])
                importantMedical.append(zz)

            print '当功效为‘清热解毒’时，占主导作用的药物组合是：\n'
            count=0
            # print importantMedical
            for item in importantMedical:
                # print item
                print '药物%d:'%(count+1),item[0],item[1]
                count+=1
            print '一共有 %d 中药物'%len(importantMedical)

            # writecsvname='../resultsdata/result_'+readcsvname.split('/')[-1]
            # data_process.write_in_csv(writecsvname, importantMedical)

    medicaListSet = list(set(allresults))
    # 统计每种药物出现的次数
    numarray = []
    n = []
    for item in medicaListSet:
        n.append(item)
        n.append(allresults.count(item))
        numarray.append(n)
        n = []
    # 以次数排序
    numarray = sorted(numarray, key=lambda x: x[1], reverse=True)
    writecsvname='../resultsdata/result.csv'
    data_process.write_in_csv(writecsvname, numarray)