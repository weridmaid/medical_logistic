# coding=utf-8
import data_process
def pickData(readcsvname1,readcsvname2,function):
    print 'pickData'
    preslist=[]
    funclist=[]
    presdata = data_process.read_csv(readcsvname1)
    funcdata = data_process.read_csv(readcsvname2)
    presdatalist=[]
    for item in presdata:
        presdatalist.append(item)
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

    print '功效 %s 的样本集大小为：%d' % (function, len(funclist))


    #换功效时 需要修改最后的保存文件！！！
    writecsvname = 'Apriori_QFCS_Prescription.csv'
    data_process.write_in_csv(writecsvname, preslist)
    writecsvname = 'Apriori_QFCS_Function.csv'
    data_process.write_in_csv(writecsvname, funclist)

def onlyWord(readcsvname):
    print 'onlyWord'




if __name__ == '__main__':
    print ('准备Apriori算法数据....')
    #换其他功效时 修改这里即可
    function='祛风除湿'
    # readcsvname1='prescription_6.csv'
    # readcsvname2='function_1.csv'
    #
    # pickData(readcsvname1, readcsvname2,function)

    readcsvname = 'Apriori_QFCS_Prescription.csv'
    onlyWord(readcsvname)