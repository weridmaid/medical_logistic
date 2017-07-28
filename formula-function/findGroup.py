# coding=utf-8
import re
import sys
import dataFeatureValue
import data_process
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    print '从训练好的logistic模型参数中找出占主导作用的药物...'
    # readcsvname='weight_668_oneHot_alpha0.01_100_1.0.csv'
    # readcsvname = 'weight_onehot_668_500_0.1.csv'
    readcsvname = 'weight_onehot_QFCS_start0.1_223t_maxIter50_lambda0.1.csv'
    weightdata=data_process.read_csv(readcsvname)
    # csvname='allMedicalCount_1.csv'
    csvname = 'allMedicalCount_combine_QFCS.csv'
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

    for i in range(0,11):
        zz=[]
        zz.append(medicallist[weightlist[i][0]-1])
        zz.append(weightlist[i][1])
        importantMedical.append(zz)

    print '当功效为‘祛风除湿’时，占主导作用的药物组合是：\n'
    count=0
    # print importantMedical
    for item in importantMedical:
        # print item
        print '药物%d:'%(count+1),item[0],item[1]
        count+=1
    print '一共有 %d 中药物'%len(importantMedical)

    writecsvname='result_'+readcsvname
    data_process.write_in_csv(writecsvname, importantMedical)

