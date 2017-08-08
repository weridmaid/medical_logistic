# coding=utf-8
import re
import sys
import data_process
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
def countallmedical(readcsvname):
    print 'countallmedical'
    csvdata = data_process.read_csv(readcsvname)
    medicaList=[]
    medical_value=[]
    pattern = re.compile(ur'[\u4e00-\u9fa5]')
    j=1
    for item in csvdata:
        print 'item:',item[0]
        mark = 0
        for itemdata in item:
                if mark==0:
                    mark+=1
                    continue
                data_value = []
                if(( mark % 2) == 1):
                    itemdata = itemdata.strip()
                    itemdata = itemdata.replace('l', '')
                    itemdata = itemdata.decode('utf8')
                    # print 'itemdata zzz', itemdata
                    if (pattern.search(itemdata)):
                        # print 'j', j, mark
                        # 存取出的药物
                        medicaList.append(itemdata)
                        # 存药物对应的数值
                        # data_value.append(itemdata)
                        # data_value.append(findnum(item[mark + 1]))
                    mark += 1
                    medical_value.append(data_value)
                else:
                    mark += 1
                    continue
        j+=1
    allcount=len(medicaList)
    print '所有处方中共有药物(medicaList)： ',allcount
    medicaListSet = list(set(medicaList))

    medicalcount=len(medicaListSet)
    print 'medicaList去重后得到处方中不同药物数量： ',medicalcount

    # medicalminmax=maxValueandminValue(medicaListSet,  medical_value)
    # print 'medicalminmax去重后得到处方中不同药物数量： ', len(medicalminmax)

   #统计每种药物出现的次数
    numarray = []
    n=[]
    for item in medicaListSet:
        n.append(item)
        n.append(medicaList.count(item))
        numarray.append(n)
        n = []

    print 'numarray1'
    #以次数排序
    numarray=sorted(numarray,key=lambda x:x[1],reverse=True)
    print 'numarray2'
    return numarray


if __name__ == '__main__':
    print 'main'

    # countallmedical()
    # prescriptionFeature()

    # prescription2Feature()


    # print (findnum('56ml'))
    # print (findnum('2个'))

    # maxValueandminValue()