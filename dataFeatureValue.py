# coding=utf-8
import xlrd
import csv
import codecs
import re
import sys
import excelprocess
reload(sys)
sys.setdefaultencoding('utf-8')

#找出字段里的数字
def findnum(itemdata):
    # print 'findnum'
    pattern_1 = re.compile(r'\d+.\d+')
    pattern_2 = re.compile(ur'\d+')

    value=0.0

    a1 = pattern_1.findall(itemdata)
    a2 = pattern_2.findall(itemdata)
    try:
        if (a1):
            value = a1[0]
        else:
            value = a2[0]
    except:pass

    return float(value)

#计算每种药物数值单位的最大值maxValue 和 最小值minValue （用于归一化）
def maxValueandminValue(listSet,listmadicalandvalue):
    print 'maxValueandminValue'
    medicalnum=[]
    for item in listSet:
        # print 'item',item
        minValue = 1000000.0
        maxValue=0.0
        value = 0.0
        list=[]
        list.append(item)
        for itemmediacal in listmadicalandvalue:
            # print 'itemmedical',itemmediacal
            try:
                if(itemmediacal[0]==item):
                    value=float(itemmediacal[1])
                    if (minValue>value):
                        minValue=value
                    if(maxValue<value):
                        maxValue=value
            except:
                continue

        valuemins=maxValue-minValue
        list.append(maxValue)
        list.append(minValue)
        list.append(valuemins)
        medicalnum.append(list)
    return medicalnum



# **************************** 输入：allData_normal1.csv ; 输出：allNormalMedicalCount.csv ***********************************
#统计所有处方中共有多少种药物出现过
def countallmedical():
    print 'countallmedical'
    # readcsvname = 'allmedical.csv'
    # readcsvname = 'allData_normal1.csv'
    # csvdata = excelprocess.read_csv(readcsvname)
    # readcsvname = 'allData_none1.csv'
    readcsvname = 'allData1.csv'
    csvdata = excelprocess.read_csv(readcsvname)
    medicaList=[]
    medical_value=[]
    pattern = re.compile(ur'[\u4e00-\u9fa5]')
    j=1
    for item in csvdata:
        # print 'item:',item
        mark = 0
        for itemdata in item:
            data_value = []
            if (mark == 0):
                mark += 1
                continue
            else:
                if(( mark % 2) == 0):
                    mark += 1
                    continue
                else:
                    itemdata = itemdata.strip()
                    itemdata = itemdata.replace('l', '')
                    itemdata = itemdata.decode('utf8')

                    if(pattern.search(itemdata)):
                        # print 'j',j,mark
                        #存取出的药物
                        medicaList.append(itemdata)
                        #存药物对应的数值
                        data_value.append(itemdata)
                        data_value.append(findnum(item[mark+1]))

                    mark += 1
                    medical_value.append(data_value)
            j+=1
    allcount=len(medicaList)
    print '所有处方中共有药物(medicaList)： ',allcount
    medicaListSet = list(set(medicaList))

    medicalcount=len(medicaListSet)
    print 'medicaList去重后得到处方中不同药物数量： ',medicalcount

    # print 'medicaListSet:',medicaListSet
    # print 'medical_value:',medical_value

    medicalminmax=maxValueandminValue(medicaListSet,  medical_value)
    print 'medicalminmax去重后得到处方中不同药物数量： ', len(medicalminmax)

   #统计每种药物出现的次数
    numarray = []
    n=[]
    for item in medicaListSet:
        n.append(item)
        n.append(medicaList.count(item))
        numarray.append(n)
        n = []

    #以次数排序
    numarray=sorted(numarray,key=lambda x:x[1],reverse=True)

    # writecsvname = 'allNormalMedicalCount.csv'
    # excelprocess.write_in_csv(writecsvname , numarray)

    # writecsvname = 'allNormalMedicalandValue.csv'
    # excelprocess.write_in_csv(writecsvname ,  medical_value)

    # writecsvname = 'allNormalMedicalMinMaxValue.csv'
    # excelprocess.write_in_csv(writecsvname , medicalminmax)

    writecsvname = 'allData1Count.csv'
    excelprocess.write_in_csv(writecsvname , numarray)

# **************************** 输入：allData_normal1.csv  & allNormalMedicalMinMaxValue.csv & allLabelDataValue.csv;
#****************************  输出：prescriptionFeature.csv &labelFeature.csv  ***********************************
#获取表示方剂的数值化特征
def prescriptionFeature():
    print 'prescriptionFeature'
    readcsvname = 'allNormalMedicalMinMaxValue.csv'
    medicaldata = excelprocess.read_csv(readcsvname)

    # readcsvname = 'allData_normal1.csv'
    readcsvname = 'allData1.csv'
    prescriptiondata = excelprocess.read_csv(readcsvname)

    readcsvname = 'allLabelDataValue.csv'
    labeldata = excelprocess.read_csv(readcsvname)

    medicaList=[]
    mediaclvalueList=[]
    for item in medicaldata:
        medicaList.append(item[0].replace('﻿', ''))
        mediaclvalueList.append(item)

    labelmark=[]
    labelvalue=[]
    for item in labeldata:
        mark=0
        nn=[]
        for itemdata in item:
            itemdata=itemdata.replace('﻿', '')
            if(mark==0):
                labelmark.append(itemdata)
            else:
                nn.append(itemdata)
            mark+=1
        labelvalue.append(nn)

    # print (labelvalue)

    # print 'mediacl', medicaList
    # for item in medicaList:
    #     print (item)
    presFeatrue= []
    presLabelFeatrue=[]
    j=1
    wrongnum=1
    #allData_normal1.csv一共有药物1298种
    # print (featrue)
    for item in prescriptiondata:
        # print 'item:',item
        mark = 0
        #allData_normal1.csv
        # featrue = [0] * 1298
        #allData1.csv
        featrue = [0] * 1379
        for itemdata in item:
            if (mark == 0):
                # print 'itemdata',itemdata
                itemdata = itemdata.replace('﻿', '')
                # print 'itemdata', itemdata
                loc = labelmark.index(itemdata)
                # print 'loc',loc
                # print (labelvalue[loc])
                presLabelFeatrue.append(labelvalue[loc])
            else:
                if(( mark % 2) != 0):
                    try:
                        location=medicaList.index(itemdata)
                        # print 'location',location
                        itemvalue=findnum(item[mark+1])
                        finalValue=(itemvalue-float(mediaclvalueList[location][2])+1)/(float(mediaclvalueList[location][3])+1)
                        #特征既有配伍成分，有考虑了单位数量
                        # featrue[location]=finalValue
                        #只关心配伍成分，不关心单位数量
                        featrue[location]=1
                    except:
                        # print 'wrong',wrongnum,item[0],mark,itemdata
                        wrongnum += 1
                else:
                    mark+=1
                    continue
            mark+=1

        j+=1
        # print (featrue)
        presFeatrue.append(featrue)

    print len(presFeatrue),j,len(presLabelFeatrue)
    # for item in presFeatrue:
    #     print (item)

    # writecsvname = 'prescriptionFeature2.csv'
    # excelprocess.write_in_csv(writecsvname , presFeatrue)
    #
    # writecsvname = 'labelFeature2.csv'
    # excelprocess.write_in_csv(writecsvname , presLabelFeatrue)


def prescription2Feature():
    print 'prescription2Feature'
    #allData_normal1.csv里的不同药味数统计
    readcsvname = 'allNormalMedicalMinMaxValue.csv'
    # allData1.csv里的不同药味数统计
    # readcsvname = 'allData1Count.csv'
    medicaldata = excelprocess.read_csv(readcsvname)

    readcsvname = 'allData_normal1.csv'
    # readcsvname = 'allData1.csv'
    prescriptiondata = excelprocess.read_csv(readcsvname)

    readcsvname = 'allLabelDataValue.csv'
    labeldata = excelprocess.read_csv(readcsvname)

    medicaList=[]
    mediaclvalueList=[]
    for item in medicaldata:
        medicaList.append(item[0].replace('﻿', ''))
        # mediaclvalueList.append(item)

    labelmark = []
    labelvalue = []
    for item in labeldata:
        mark = 0
        nn = []
        for itemdata in item:
            itemdata = itemdata.replace('﻿', '')
            if (mark == 0):
                labelmark.append(itemdata)
            else:
                nn.append(itemdata)
            mark += 1
        labelvalue.append(nn)

    presFeatrue = []
    presLabelFeatrue = []
    j = 1
    wrongnum = 1
    # allData_normal1.csv一共有药物1298种
    for item in prescriptiondata:
        # print 'item:',item
        mark_v=0
        prevalue = 0
        for itemdata in item:
            #计算每个处方里药物剂量总值
            if (mark_v == 0):
                mark_v=+1
                continue
            else:
                if ((mark_v % 2) != 0):
                    mark_v += 1
                else:
                    value = findnum(itemdata)
                    prevalue = prevalue + value
                    mark_v += 1
        mark = 0
        # allData1.csv
        # dim=1379
        # allData_normal1.csv
        dim=1298
        featrue = [0] * dim
        for itemdata in item:
            if (mark == 0):
                #处理对应的标签
                itemdata = itemdata.replace('﻿', '')
                # print 'itemdata', itemdata
                loc = labelmark.index(itemdata)
                # print 'loc',loc
                # print (labelvalue[loc])
                presLabelFeatrue.append(labelvalue[loc])
            else:
                if ((mark % 2) != 0):
                    try:
                        location = medicaList.index(itemdata)
                        itemvalue = findnum(item[mark + 1])/prevalue

                        # featrue[location] = 1
                        # featrue[location+dim-1] = itemvalue
                        featrue[location] = itemvalue
                    except:
                        print 'wrong',wrongnum,item[0],mark,itemdata
                        wrongnum += 1
                else:
                    mark += 1
                    continue
            mark += 1

        j += 1
        # print (featrue)
        presFeatrue.append(featrue)

    print len(presFeatrue), j, len(presLabelFeatrue)

    writecsvname = 'prescriptionFeature4.csv'
    excelprocess.write_in_csv(writecsvname , presFeatrue)

    writecsvname = 'labelFeature4.csv'
    excelprocess.write_in_csv(writecsvname , presLabelFeatrue)

if __name__ == '__main__':
    print 'main'

    # countallmedical()
    # prescriptionFeature()

    prescription2Feature()


    # print (findnum('56ml'))

    # maxValueandminValue()