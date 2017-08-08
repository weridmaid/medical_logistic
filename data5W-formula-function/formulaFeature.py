# coding=utf-8
import sys
import dataFeatureValue
import data_process
reload(sys)
sys.setdefaultencoding('utf-8')

#获取表示方剂的数值化特征 -one hat方法
def presFeature(csvname1,csvname2):
    print 'presFeature'

    prescriptiondata = data_process.read_csv(csvname1)
    medicaldata = data_process.read_csv(csvname2)

    medicaList=[]
    for item in medicaldata:
        medicaList.append(item[0].replace('﻿', ''))
    # print 'mediacl', medicaList
    # for item in medicaList:
    #     print (item)

    pFeatrue= []
    presLabelFeatrue=[]
    wrongnum=1
    #allData_normal1.csv一共有药物1487种
    for item in prescriptiondata:
        # print 'item:',item
        item[0] = item[0].replace('﻿', '')
        mark = 0
        #多少种药就是多少维 668种药，668维
        # featrue = [0] * 1563
        featrue = [0] * 584
        for itemdata in item:
                if mark==0:
                    mark+=1
                    continue
                if(( mark % 2) == 1):
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
        pFeatrue.append(featrue)

    print len(pFeatrue),wrongnum
    return pFeatrue


#获取表示方剂的数值化特征 -每维值用单位数量表示
def presFeature_1(csvname1,csvname2):
    print 'presFeature_1'

    prescriptiondata = data_process.read_csv(csvname1)
    medicaldata = data_process.read_csv(csvname2)

    medicaList=[]
    for item in medicaldata:
        medicaList.append(item[0].replace('﻿', ''))

    pFeatrue= []
    presLabelFeatrue=[]
    j=1
    wrongnum=1
    for item in prescriptiondata:
        # print 'item:',item
        item[0] = item[0].replace('﻿', '')
        mark = 0
        # featrue = [0] * 1563
        featrue = [0] * 223
        for itemdata in item:
                if(( mark % 2) == 0):
                    try:
                        location=medicaList.index(itemdata)
                        # print 'location',location
                        if item[mark+1]!='None':
                            itemvalue=dataFeatureValue.findnum(item[mark+1])
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
    prescriptiondata = data_process.read_csv(csvname1)
    medicaldata = data_process.read_csv(csvname2)

    medicaList=[]
    for item in medicaldata:
        medicaList.append(item[0].replace('﻿', ''))

    pFeatrue= []
    presLabelFeatrue=[]
    j=1
    wrongnum=1
    for item in prescriptiondata:
        # print 'item:',item
        item[0] = item[0].replace('﻿', '')
        mark = 0
        # featrue = [0] * 1563
        featrue = [0] * 223
        lenth=len(item)
        thisall=0
        for i in range(0,lenth):
            if ((i % 2)!=0):
                if item[i] != 'None':
                    thisall = thisall+dataFeatureValue.findnum(item[i])
                else:
                    thisall=thisall+28
        for itemdata in item:
                if(( mark % 2) == 0):
                    try:
                        location=medicaList.index(itemdata)
                        # print 'location',location
                        if item[mark+1]!='None':
                            itemvalue=dataFeatureValue.findnum(item[mark+1])
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
    prescriptiondata = data_process.read_csv(csvname)
    num=0
    itemvalue=0
    for item in prescriptiondata:
        mark = 0
        for itemdata in item:
            if ((mark % 2) == 0):
                mark += 1
            else:
                if itemdata != 'None':
                    value=dataFeatureValue.findnum(itemdata)
                    if value<1000:
                        itemvalue = itemvalue+value
                        num += 1
                else:
                    continue
                mark += 1
    ave=itemvalue/num
    print 'itemvalue,num,ave=itemvalue/num:',itemvalue,num,ave

def tongji(readcsvname):
    print 'tongji'
    data = data_process.read_csv(readcsvname)
    medicallist=[]
    for item in data:
        medicallist.append(item)

    num=0
    count = 0
    countp=0
    all=len(medicallist)
    print all
    for item in medicallist:
        if num ==0:
            aa=item[1]
            count += 1
        else:
            # print 'zz', item[1]
            if item[1]==aa:
                count+=1
            else:
                # print count
                p=float(count)/all
                countp=countp+p
                print '频次：%s , 占比：%f'%(aa,p)
                count=0
                count += 1
            aa = item[1]
        num+=1

    p = float(count) / all
    countp = countp + p
    print '频次：%s , 占比：%f' % (aa, p)
    print 'countp',countp


if __name__ == '__main__':
    print '计算配方的特征向量...'

    #step 1 统计所有处方中共有多少种药物出现过
    # readcsvname='../formulaData_1/QRJD_pres.csv'
    # numarray=dataFeatureValue.countallmedical(readcsvname)
    # # 手动去除allMedicalCount_1.csv里频次为1的药物；和调和药“甘草”
    # writecsvname = '../formulaData_1/QRJD_medical_count.csv'
    # data_process.write_in_csv(writecsvname , numarray)

    #统计处方中不同频次的药物占比
    # readcsvname = 'allMedicalCount_combine_QFCS.csv'
    # tongji(readcsvname)

    #step 2 计算方剂向量特征
    #(1)使用one-hot表示，每个方剂的维数等于所有方剂中药物的去重个数，若出现则为1 *********presFeature_onehot.csv
    #数据1：全取自防风数据集
    csvname1='../formulaData_1/QRJD_pres.csv'
    csvname2 = '../formulaData_1/QRJD_medical_count.csv'
    pFeatrue= presFeature(csvname1,csvname2)
    writecsvname = '../formulaData_1/presFeature_onehot_QRJD_584t.csv'
    data_process.write_in_csv(writecsvname , pFeatrue)
    #
    # # (2)使用配伍单位数值表示，每个方剂的维数等于所有方剂中药物的去重个数*********presFeature_realValue.csv
    # csvname1 = 'prescription_6.csv'
    # csvname2 = 'allMedicalCount_1.csv'
    # pFeatrue = presFeature_1(csvname1, csvname2)
    # writecsvname = 'presFeature_realValue_combine_QFCS_223t.csv'
    # data_process.write_in_csv(writecsvname, pFeatrue)
    #
    # # (3)使用配伍单位数值表示，每个方剂的维数等于所有方剂中药物的去重个数,在方剂中做归一化处理*********presFeature_standardValue.csv
    # csvname1 = 'prescription_6.csv'
    # csvname2 = 'allMedicalCount_1.csv'
    # 数据2：与web爬取数据结合的正负例
    # csvname1='combinePrescription.csv'
    # csvname2 = 'allMedicalCount_combine_QFCS.csv'

    # pFeatrue = presFeature_2(csvname1, csvname2)
    # writecsvname = 'presFeature_vstandardValue_combine_QFCS_227t.cs'
    # data_process.write_in_csv(writecsvname, pFeatrue)



     #strep other 计算方剂剂量的均值
    # csvname = 'prescription_6.csv'
    # computeAverage(csvname)

