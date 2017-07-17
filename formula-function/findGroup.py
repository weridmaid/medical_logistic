# coding=utf-8
import re
import sys
import dataFeatureValue
import data_process
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    print '从训练好的logistic模型参数中找出占主导作用的药物...'
    readcsvname='weights_0.1.csv'
    weightdata=data_process.read_csv(readcsvname)
    csvname='allMedicalCount.csv'
    medicaldata=data_process.read_csv(csvname)
    medicallist=[]
    importantMedical=[]
    weightlist=[]
    for item in medicaldata:
        medicallist.append(item[0])
    num = 0
    # data=[]
    # for item in weightdata:
    #     print 'zz', item
    #     item[0]=item[0].replace('[[','')
    #     item[0] = item[0].replace(']]', '')
    #     item[0] = item[0].replace('﻿', '')
    #     print 'zzz',item[0]
    for item in weightdata:
        zz=[]
        item[0]=item[0].replace('[[','')
        item[0] = item[0].replace(']]', '')
        item[0] = item[0].replace('﻿', '')
        # print 'zz',item[0]
        if num==0:
            pass
        else:
            if float(item[0])>0.001 or float(item[0])<-0.004:
                zz.append(medicallist[num-1])
                zz.append(item[0])
                importantMedical.append(zz)
        num+=1

    print '当功效为‘祛风清热’时，占主导作用的药物组合是：\n'
    count=0
    print importantMedical
    for item in importantMedical:
        print item
        print '药物%d:'%(count+1),item[0],item[1]
        count+=1
    print '一共有 %d 中药物'%len(importantMedical)

    writecsvname='result_0.1.csv'
    data_process.write_in_csv(writecsvname, importantMedical)

