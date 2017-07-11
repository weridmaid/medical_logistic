# coding=utf-8
import re
import data_process
import dataDetailProcess


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#
def checkitem(readcsvname1,readcsvname2,readcsvname3):
    print '检查配伍-功效-主治对应与否中....'
    data1=data_process.read_csv(readcsvname1)
    data2 = data_process.read_csv(readcsvname2)
    data3 = data_process.read_csv(readcsvname3)

    i=0
    for item in data1:
        if i==1620:
            print '第1620行 配伍 ',item
            for itemdata in item:
                print itemdata
        i+=1
    j=0
    for item in data2:
        if j==1620:
            print '第1620行 功效 ',item[0]
        j+=1
    k=0
    for item in data3:
        if k==1620:
            print '第1620行 主治 ',item[0]
        k+=1

    # print '第1632行 配伍-功效-主治：', data1[1631], data2[1631], data3[1631]


if __name__ == '__main__':
    print ('数据细节处理进行中....')
    #step 1 处理文本中的空格
    # readcsvname='prescription.csv'
    # writecsvname='prescription_1.csv'
    # dataprocess.composition_process(readcsvname,writecsvname)

    #step 2 处理用空格切割后还存在的多余的空格？
    # readcsvname='prescription_1.csv'
    # writecsvname='prescription_2.csv'
    # dataprocess.process_blank(readcsvname,writecsvname)

    # step 3 去括号等一些附加说明
    # readcsvname='prescription_2.csv'
    # writecsvname='prescription_3.csv'
    # dataDetailProcess.process_blank(readcsvname, writecsvname)


    # step other  检查一下功效和配伍是否一一对应
    # readcsvname1 = 'prescription_2.csv'
    # readcsvname2 = 'function.csv'
    # readcsvname3='indications.csv'
    # data1=checkitem(readcsvname1,readcsvname2,readcsvname3)

    # step 4
    readcsvname1 = 'prescription_2.csv'
    # readcsvname2 = 'function.csv'
    # readcsvname3='indications.csv'
    # data1=checkitem(readcsvname1,readcsvname2,readcsvname3)