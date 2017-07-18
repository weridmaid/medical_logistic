# coding=utf-8
import re
import sys
import web_dataFeatureValue
import web_data_process
reload(sys)
sys.setdefaultencoding('utf-8')

#获取表示方剂的数值化特征 -one hat方法
def presFeature(csvname1,csvname2):
    print 'presFeature'

    prescriptiondata = web_data_process.read_csv(csvname1)
    medicaldata = web_data_process.read_csv(csvname2)

    medicaList=[]
    for item in medicaldata:
        medicaList.append(item[0].replace('﻿', ''))
    # print 'mediacl', medicaList
    # for item in medicaList:
    #     print (item)

    pFeatrue= []
    presLabelFeatrue=[]
    j=1
    wrongnum=1
    #allData_normal1.csv一共有药物1487种
    for item in prescriptiondata:
        # print 'item:',item
        mark = 0
        featrue = [0] * 1486
        for itemdata in item:
                if(( mark % 2) == 0):
                    try:
                        location=medicaList.index(itemdata)
                        # print 'location',location
                        # itemvalue=dataFeatureValue.findnum(item[mark+1])
                        # finalValue=(itemvalue-float(mediaclvalueList[location][2])+1)/(float(mediaclvalueList[location][3])+1)
                        #特征既有配伍成分，有考虑了单位数量
                        # featrue[location]=finalValue
                        #只关心配伍成分，不关心单位数量
                        featrue[location]=1
                    except:
                        # print 'wrong',wrongnum,item[0],mark,itemdata
                        wrongnum += 1
                    mark += 1
                else:
                     mark+=1
        j+=1
        pFeatrue.append(featrue)

    print len(pFeatrue),j,wrongnum
    return pFeatrue


#获取表示方剂的数值化特征 -每维值用单位数量表示
def presFeature_1(csvname1,csvname2):
    print 'presFeature_1'

    prescriptiondata = web_data_process.read_csv(csvname1)
    medicaldata = web_data_process.read_csv(csvname2)

    medicaList=[]
    for item in medicaldata:
        medicaList.append(item[0].replace('﻿', ''))

    pFeatrue= []
    presLabelFeatrue=[]
    j=1
    wrongnum=1
    for item in prescriptiondata:
        # print 'item:',item
        mark = 0
        featrue = [0] * 1486
        for itemdata in item:
                if(( mark % 2) == 0):
                    try:
                        location=medicaList.index(itemdata)
                        # print 'location',location
                        if item[mark+1]!='None':
                            itemvalue=web_dataFeatureValue.findnum(item[mark + 1])
                            # finalValue=(itemvalue-float(mediaclvalueList[location][2])+1)/(float(mediaclvalueList[location][3])+1)
                            #特征既有配伍成分，又考虑了单位数量
                            featrue[location]=float(itemvalue)
                        else:
                            featrue[location] = float(28)
                    except:
                        # print 'wrong',wrongnum,item[0],mark,itemdata
                        wrongnum += 1
                    mark += 1
                else:
                     mark+=1
        j+=1
        pFeatrue.append(featrue)

    print len(pFeatrue),j,wrongnum
    return pFeatrue

#获取表示方剂的数值化特征 -每维值用归一化的单位数量表示
def presFeature_2(csvname1,csvname2):
    print 'presFeature_1'
    prescriptiondata = web_data_process.read_csv(csvname1)
    medicaldata = web_data_process.read_csv(csvname2)

    medicaList=[]
    for item in medicaldata:
        medicaList.append(item[0].replace('﻿', ''))

    pFeatrue= []
    presLabelFeatrue=[]
    j=1
    wrongnum=1
    for item in prescriptiondata:
        # print 'item:',item
        mark = 0
        featrue = [0] * 1487
        lenth=len(item)
        thisall=0
        for i in range(0,lenth):
            if ((i % 2)!=0):
                if item[i] != 'None':
                    thisall = thisall + web_dataFeatureValue.findnum(item[i])
                else:
                    thisall=thisall+28
        for itemdata in item:
                if(( mark % 2) == 0):
                    try:
                        location=medicaList.index(itemdata)
                        # print 'location',location
                        if item[mark+1]!='None':
                            itemvalue=web_dataFeatureValue.findnum(item[mark + 1])
                            # finalValue=(itemvalue-float(mediaclvalueList[location][2])+1)/(float(mediaclvalueList[location][3])+1)
                            #特征既有配伍成分，又考虑了单位数量和归一化
                            featrue[location]=itemvalue/thisall
                        else:
                            featrue[location] = 28/thisall
                    except:
                        # print 'wrong',wrongnum,item[0],mark,itemdata
                        wrongnum += 1
                    mark += 1
                else:
                     mark+=1
        j+=1
        pFeatrue.append(featrue)

    print len(pFeatrue),j,wrongnum
    return pFeatrue

#计算方剂中剂量的平均值
def computeAverage(csvname):
    print  'computeAverage'
    prescriptiondata = web_data_process.read_csv(csvname)
    num=0
    itemvalue=0
    for item in prescriptiondata:
        mark = 0
        for itemdata in item:
            if ((mark % 2) == 0):
                mark += 1
            else:
                if itemdata != 'None':
                    value=web_dataFeatureValue.findnum(itemdata)
                    if value<1000:
                        itemvalue = itemvalue+value
                        num += 1
                else:
                    continue
                mark += 1
    ave=itemvalue/num
    print 'itemvalue,num,ave=itemvalue/num:',itemvalue,num,ave



if __name__ == '__main__':
    print '计算配方的特征向量...'

    #step 1 统计所有处方中共有多少种药物出现过
    # readcsvname='prescription_6.csv'
    # numarray=dataFeatureValue.countallmedical(readcsvname)
    # writecsvname = 'allMedicalCount.csv'
    # data_process.write_in_csv(writecsvname , numarray)

    #step 2 计算方剂向量特征
    #(1)使用one-hot表示，每个方剂的维数等于所有方剂中药物的去重个数，若出现则为1 *********presFeature_onehot.csv
    # csvname1='prescription_6.csv'
    # csvname2 = 'allMedicalCount.csv'
    # pFeatrue= presFeature(csvname1,csvname2)
    # writecsvname = 'presFeature_onehot.csv'
    # data_process.write_in_csv(writecsvname , pFeatrue)

    # (2)使用配伍单位数值表示，每个方剂的维数等于所有方剂中药物的去重个数*********presFeature_realValue.csv
    csvname1 = 'prescription_6.csv'
    csvname2 = 'allMedicalCount.csv'
    pFeatrue = presFeature_1(csvname1, csvname2)
    writecsvname = 'presFeature_realValue.txt'
    web_data_process.write_in_csv(writecsvname, pFeatrue)

    # (3)使用配伍单位数值表示，每个方剂的维数等于所有方剂中药物的去重个数,在方剂中做归一化处理*********presFeature_standardValue.csv
    # csvname1 = 'prescription_6.csv'
    # csvname2 = 'allMedicalCount.csv'
    # pFeatrue = presFeature_2(csvname1, csvname2)
    # writecsvname = 'presFeature_standardValue.csv'
    # data_process.write_in_csv(writecsvname, pFeatrue)



     #strep other 计算方剂剂量的均值
    # csvname = 'prescription_6.csv'
    # computeAverage(csvname)

