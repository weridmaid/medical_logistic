# coding=utf-8
import re
import data_process

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#****************************输入：compostion_1.csv;输出：composition_1_1.csv***********************************
#把compostion_1.csv里的数据取出来，按空格分割提取每个成分；
#注意！这里处理后有的数据会出现多余的空格！***************手动处理那些多余的空格。。。**************************
#eg.地骨皮30g  防风30g  甘草15g(微炙) =============> 地骨皮30g,防风30g,甘草15g(微炙)
def composition_process(readcsvname,writecsvname):
    print ('composition_process')
    # readcsvname='composition_6.csv'
    csvdata=data_process.read_csv(readcsvname)
    datas=[]
    i=1
    for item in csvdata:
        # print 'row',i,item[0].split(' ')
        item=item[0].split(' ')
        num = 0
        for itemdata in item:
            if itemdata == '':
                item.pop(num)
            num += 1
        datas.append(item)
        i+=1

    # j=1
    # for item in datas:
    #     print 'j', j
    #     j+=1
    #     print item
    #     for itemdata in item:
    #         print 'zz',itemdata

    data_process.write_in_csv(writecsvname,datas)

#自动去除上述方法处理后还存在的空格
def process_blank(readcsvname,writecsvname):
    print ('process_blank')
    csvdata=data_process.read_csv(readcsvname)
    datas=[]
    i=1
    replace=[]
    for item in csvdata:
        num = 0
        lengh=len(item)
        for itemdata in item:
            # print 'itemdata',i,itemdata
            if itemdata == '':
                item.pop(num)
            itemdata = itemdata.split('\xe3\x80\x80')
            if len(itemdata)>1:
                # print 'split itemdata',i,itemdata
                for zz in itemdata:
                    replace.append(zz)
            else:
                replace.append(itemdata[0])
            num += 1
        datas.append(replace)
        replace=[]
        i+=1
    data_process.write_in_csv(writecsvname,datas)



#****************************输入：compostion_1_1.csv;输出：composition_1_2.csv***********************************
#清除描述中的 “各”字；清除药物括号里的内容
#eg.苍术(泔浸，去皮净)120g,防风6g,白术,白茯苓,白芍药各3g ======> 苍术120g,防风6g,白术,白茯苓,白芍药#3g
def splitnumandstr(readcsvname):
    print ('splitnumandstr')
    # readcsvname='csvtest.csv'
    # readcsvname='composition_1_1.csv'
    csvdata=data_process.read_csv(readcsvname)
    i=1
    data_after=[]
    datalist=[]
    for item in csvdata:
        print ('%%%%%%%%%%%%%num',i)

        for itemdata in item:
            itemdata=itemdata.replace('﻿','')
            #把 “各” 字 单独处理
            itemdata = itemdata.replace('各', '#')
            print ('itemdata', itemdata)

            #清洗数据：处理描述中的里括号里的内容***不要括号里的内容**********
            try:
                num1=itemdata.index('(')
                num2=itemdata.index(')')
                itemdata=itemdata+'*'
                print ('*****************num1,num2******************', num1, num2)
                itemdata=itemdata[0:num1]+itemdata[num2+1:-1]
                print ('*****************清除英文括号内容******************', itemdata)
                num11 = itemdata.index('（')
                num22 = itemdata.index('）')
                itemdata=itemdata+'*'
                print ('*****************num1,num2******************', num11, num22)
                itemdata=itemdata[0:num11]+itemdata[num22+1:-1]
                print ('*****************清除中文括号内容******************', itemdata)
            except:
                 pass
            data_after.append(itemdata)
        i+=1
        datalist.append(data_after)
        # print 'data_after^^^^^^^^^^^^^^^^^',data_after
        data_after=[]


    # writecsvname = 'composition_1_2.csv'

    # writecsvname='csvtest_1.csv'
    # data_process.write_in_csv(writecsvname,datalist)
    return datalist



#****************************输入：compostion_1_1.csv;输出：composition_1_3.csv***********************************
#提取描述中的药物单位量以及它所对应的药
#eg1.苍术120g,防风6g,白术,白茯苓,白芍药#3g =================》苍术,120g,防风,6g,白术,3g ,白茯苓,3g ,白芍药,3g
#eg2.黄芩,防风#等分=================》黄芩,None,防风,None
def extractnumwithstr(readcsvname):
    print ('extractnumwithstr')
    # readcsvname='csvtest_1.csv'
    # readcsvname='composition_5_2.csv'
    csvdata=data_process.read_csv(readcsvname)

    # i:指示第i个处方
    i=1
    #正则匹配要用' ur'' '才能正确匹配中文
    #(?:..):(...)的不分组版本，用于使用| 或 后接数量词
    pattern1 = re.compile(ur'\d+.\d+(?:g|kg|ml|l|个|钱|片|根|条|份|张|枚|具|朵|只|粒|茎|两|斤|挺|对|头|L|ML|分|节|cm|握)')
    pattern2=re.compile(ur'\d+(?:g|kg|ml|l|个|钱|片|根|条|份|张|枚|具|朵|只|粒|茎|两|斤|挺|对|头|L|ML|分|节|cm|握)')
    pattern3=re.compile(ur'kg')
    finalmedicallist=[]
    for item in csvdata:
        print '****************************************************************** 处方： ',i
        medicallist = []
        point = []
        medicaldict=[]
        for itemdata in item:
            weight = ''
            yaowulist=[]
            itemdata = itemdata.replace('﻿', '')
            itemdata = itemdata.replace('．', '.')
            itemdata = itemdata.replace('o', '0')
            itemdata = itemdata.decode('utf8')
            # print 'itemdata', itemdata

            #在处方内容中通过正则匹配找出数量单位 start
            weight1=pattern1.findall(itemdata)
            weight2=pattern2.findall(itemdata)
            #把正确的值放在变量weight中
            if(weight1):
                weight=weight1[0]
                yaowulist=pattern1.split(itemdata)
            elif(weight2):
                weight = weight2[0]
                yaowulist=pattern2.split(itemdata)
            # print '$$$$$$$$$$$$findal',weight1,weight2,weight
            # 在处方内容中通过正则匹配找出数量单位 end
            # print 'yaowulist',yaowulist
            # for ii in yaowulist:
            #     print ii

            # 把处方的每味药提出来重新放在medicallist列表元素[0]里，同时已经去除了药的数量单位
            if(yaowulist):
                try:
                    yaowulist.remove('')
                    for zz in yaowulist:
                        medicallist.append(zz)
                except:
                    pass
            else:
                medicallist.append(itemdata)

            # 把处方的每味药所对应的数量单位存入medicallist 列表元素[1]的位置列表里
            if(weight):
                medicallist.append(weight)
            else:
                medicallist.append('None')

            #medicallist eg.[u'\u9632\u98ce', u'3l']
            medicaldict.append(medicallist)
            medicallist = []

        # print "medicallist", medicallist

        print ('medicaldict',medicaldict)
        #j统计每个处方里的第j味药
        j=0
        for k,v in medicaldict:
            #用point记录#在哪味药上
            # print k,v
            if(k.find('#')>0):
                point.append(j)
                medicaldict[j][0]=medicaldict[j][0].replace('#','')
                # print (medicaldict[j][0])
                print '检测到“各”字，该味药在处方中所处位置：',j,k
            j+=1
        print '该方剂一共配药数量为：',j
        print '该方剂中出现“各”字的位置有：', point

        f=0
        print ('##################### 开始处理所有药的数量单位 ##################')
        # print ('medicaldict', medicaldict)


        for m,n in medicaldict:
            if(point!=[]):
                for pointnum in point:
                    # print 'test', pointnum
                    if(f>pointnum):
                        continue
                    elif (n=='None'):
                            # print 'test4',medicaldict[f][1],pointnum
                            medicaldict[f][1]=medicaldict[pointnum][1]
                            break
            f+=1
        # print '@@@@@@~~最后处理结果(列表):', medicaldict

        #重新整理medicaldict数据格式，并存入csv里
        onepiece=[]
        for x,y in medicaldict:
            print (x,y)
            onepiece.append(x)
            onepiece.append(y)
            # print 'onepiece',onepiece

        # data_process.createListCSV('csvtest_2.csv',medicaldict)
        finalmedicallist.append(onepiece)
        #处方数增一
        i += 1


    return finalmedicallist
    # print (finalmedicallist)
    # writecsvname = 'composition_2_3.csv'
    # data_process.createListCSV(writecsvname, finalmedicallist)


# ****************************输入：compostion_1_3.csv ~ compostion_6_3.csv; 输出：allData.csv***********************************
#把六个类的数据全部放在一个csv里:allData.csv
#eg.*1*4,地骨皮,30g,防风,30g,炙甘草,7.5g
def createAllList():
    print ('createAllList')
    addlist = []
    for inum in range(1,7):
        print ('inum',inum)
        readcsvname='composition_'+str(inum)+'_3.csv'
        # readcsvname = 'csvtest_2.csv'
        csvdata = data_process.read_csv(readcsvname)
        pnum='*'+str(inum)
        # print 'csvdata',csvdata
        i=1
        for item in csvdata:
            pnum=pnum+'*'+str(i)
            item.insert(0,pnum)
            # print 'zzzz:',item
            addlist.append(item)
            pnum='*'+str(inum)
            i+=1
    # writecsvname = 'allData.csv'
    #测试
    # writecsvname = 'csvtest_3.csv'
    # data_process.write_in_csv(writecsvname, addlist)


# **************************** 输入：allData.csv; 输出：allData_normal.csv    ,   allData_none.csv ***********************************
#把带None的数据和完整数据分开
def seperateNone():
    print ('seperateNone')
    readcsvname = 'csvtest_3.csv'
    # readcsvname ='allData_none.csv'
    csvdata = data_process.read_csv(readcsvname)
    normalList=[]
    noneLise=[]
    nn=1
    #统计每类数据里带NONE的方剂有多少条
    count=1
    for item in csvdata:
        # print 'item',item
        check=1
        for itemdata in item:
            # print 'itemdata',itemdata
            if(itemdata=='None'):
                check=0
                noneLise.append(item)
                break
        if(check==1):
            normalList.append(item)
        zz=item[0].split('*')
        # print 'zz',zz
        if(zz[1]==nn):
           count+=1
        else:
            print ('count :',count)
            count=1
        #nn用于判断类别有没有改变
        nn = zz[1]

        #看最后一类数据时打开
        # print 'count??? :', count

    # writenormalcsvname = 'csvtest_normal.csv'
    # writenonecsvname = 'csvtest_none.csv'

    #把数据中带none和完善的数据分别保存在不同的csv里
    # writenormalcsvname = 'allData_normal.csv'
    # writenonecsvname = 'allData_none.csv'
    # data_process.write_in_csv(writenormalcsvname , normalList)
    # data_process.write_in_csv(writenonecsvname, noneLise)


# **************************** 输入：allData_normal.csv (只有normal里面的才带完整的数量单位); 输出：csvtest_normal1.csv ***********************************
#单位转换为g的函数 加在这里！！
#把单位kg,钱，两 统一为 g（克）
def unitTransformation(readcsvname):
    print ('unitTransformation()')
    # readcsvname = 'csvtest_normal.csv'
    # readcsvname = 'allData_normal.csv'
    # readcsvname ='allData_none.csv'
    csvdata = data_process.read_csv(readcsvname)
    normalList=[]
    for item in csvdata:
        # print 'item',item
        midList = []
        for itemdata in item:
            # print 'itemdata', itemdata
            itemdata=itemdata.decode('utf8')
            if (itemdata.find('两') > 0):
                try:
                    zz = itemdata.split('两')
                    # print 'split itemdata', itemdata
                    unit = float(zz[0]) * 50
                    # print 'unit', unit
                    changeunit = str(unit) + 'g'
                    # print 'changeunit', changeunit
                    midList.append(changeunit)
                except:midList.append(itemdata)
            elif(itemdata.find('钱')>0):
                try:
                    zz = itemdata.split('钱')
                    unit=float(zz[0])*3.125
                    # print 'unit',unit
                    changeunit=str(unit)+'g'
                    midList.append(changeunit)
                except:
                    midList.append(itemdata)
            elif(itemdata.find('kg')>0):
                try:
                    zz = itemdata.split('kg')
                    unit=float(zz[0])*1000
                    changeunit=str(unit)+'g'
                    midList.append(changeunit)
                except:
                    midList.append(itemdata)
            elif (itemdata.find('斤') > 0):
                try:
                    zz = itemdata.split('斤')
                    unit = float(zz[0]) * 500
                    changeunit = str(unit) + 'g'
                    midList.append(changeunit)
                except:
                    midList.append(itemdata)
            elif (itemdata.find('分') > 0):
                try:
                    zz = itemdata.split('斤')
                    unit = float(zz[0]) * 0.3
                    changeunit = str(unit) + 'g'
                    midList.append(changeunit)
                except:
                    midList.append(itemdata)
            else:
                midList.append(itemdata)
        normalList.append(midList)


    # writecsvname = 'csvtest_normal1.csv'
    # writecsvname = 'allData_normal1.csv'
    # data_process.write_in_csv(writecsvname , normalList)
    return normalList

# **************************** 输入：allData_none.csv (只有normal里面的才带完整的数量单位); 输出：csvtest_none1.csv ***********************************
#单位转换为g的函数 加在这里！！
#把单位kg,钱，两 统一为 g（克）
def noneStandard(readcsvname):
    print ('noneStandard')
    # readcsvname ='allData_none.csv'
    csvdata =data_process.read_csv(readcsvname)

    noneList = []
    for item in csvdata:
        midList = []
        for itemdata in item:
            itemdata = itemdata.replace('﻿', '')
            itemdata = itemdata.replace('等分', '')
            itemdata = itemdata.replace('少许', '')
            itemdata = itemdata.replace('3倍于上药', '')
            itemdata = itemdata.replace('减半', '')
            itemdata = itemdata.replace('倍加', '')
            midList.append(itemdata)
        noneList.append(midList)

    # writecsvname = 'allData_none1.csv'
    # data_process.write_in_csv(writecsvname , noneList)
    return noneList

if __name__ == '__main__':
    print ('main')
    # composition_pracess()
    # splitnumandstr()
    # readcsvname = 'composition_2_2.csv'
    # writecsvname = 'composition_2_3.csv'
    # extractnumwithstr(readcsvname, writecsvname)
    # createAllList()
    # seperateNone()
    # unitTransformation()
    # noneStandard()

