# coding=utf-8
import data_process
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def pickData(readcsvname1,readcsvname2,readcsvname3,readcsvname4,function):
    print 'pickData'
    preslist=[]
    funclist=[]
    presdata = data_process.read_csv(readcsvname1)
    funcdata = data_process.read_csv(readcsvname2)

    webPresdata = data_process.read_csv(readcsvname3)
    webFuncdata = data_process.read_csv(readcsvname4)

    presdatalist=[]
    for item in presdata:
        presdatalist.append(item)

    webPresdatalist=[]
    for item in webPresdata:
        webPresdatalist.append(item)
    num=0
    for item in funcdata:
        # print '功效',item
        if num==0:
            item[0]=item[0].replace('﻿', '')
        for itemdata in item:
            if itemdata.decode('utf8').find(function)>-1:
                funclist.append(item)
                preslist.append(presdatalist[num])
        num+=1
    positiveCount=len(funclist)
    print '功效 %s 的个数为：%d'%(function,positiveCount)
    negativeCount=positiveCount*1.2
    num=0
    count=0
    for item in webFuncdata:
        # print '功效', item
        if num == 0:
            item[0] = item[0].replace('﻿', '')
        if count<negativeCount:
            for itemdata in item:
                # print 'itemdata.decode(utf8).find(function)',num,itemdata.decode('utf8').find(function)
                if itemdata.decode('utf8').find(function)==-1 :
                    funclist.append(item)
                    # print 'test',webPresdatalist[num]
                    preslist.append(webPresdatalist[num])
                    count+=1
                break
        num+=1

    print '功效 %s 的测试样本集大小为：%d' % (function, len(funclist))


    #换功效时 需要修改最后的保存文件！！！
    writecsvname = 'combinePrescription.csv'
    data_process.write_in_csv(writecsvname, preslist)
    writecsvname = 'combineFunction_QFCS.csv'
    data_process.write_in_csv(writecsvname, funclist)


if __name__ == '__main__':
    print 'combineData main...'
    #换其他功效时 修改这里即可
    function='祛风除湿'

    readcsvname1='prescription_6.csv'
    readcsvname2='function_1.csv'

    readcsvname3='webFormula_final_2.csv'
    readcsvname4='webFunction_3.csv'

    pickData(readcsvname1, readcsvname2, readcsvname3, readcsvname4,function)
