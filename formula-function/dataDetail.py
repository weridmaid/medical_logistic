# coding=utf-8
import data_process
import dataDetailProcess


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#检查配伍-功效-主治是否一一对应
def checkitem(readcsvname1,readcsvname2,readcsvname3):
    print '检查配伍-功效-主治对应与否中....'
    data1=data_process.read_csv(readcsvname1)
    data2 = data_process.read_csv(readcsvname2)
    data3 = data_process.read_csv(readcsvname3)

    i=0
    for item in data1:
        if i==1620:
            print 'excel 第1622行 配伍(蓝实,决明子。。。) ',item
            for itemdata in item:
                print itemdata
        i+=1
    j=0
    for item in data2:
        if j==1620:
            print '第1622行 功效(疏风散热，清肝明目。) ',item[0]
        j+=1
    k=0
    for item in data3:
        if k==1620:
            print '第1622行 主治(肝胆风热上攻，两目？？(目旁加流字右边)，视物不明。) ',item[0]
        k+=1

    # print '第1632行 配伍-功效-主治：', data1[1631], data2[1631], data3[1631]


if __name__ == '__main__':
    print ('配伍数据细节处理进行中....')
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

    # step 4
    # (1)去掉‘各’字或括号内容（还有小部分扣号需人工去除
    # readcsvname = 'prescription_2.csv'
    # datalist=dataDetailProcess.splitnumandstr(readcsvname)
    # writecsvname='prescription_3.csv'
    # data_process.write_in_csv(writecsvname, datalist)

    # (2)药名-数量单位 一一提取匹配 (有问题会停下，手动处理
    # writecsvname='prescription_3.csv'
    # finalmedicallist=dataDetailProcess.extractnumwithstr(writecsvname)
    # print 'prescription_3.csv 总行数 ：',len(finalmedicallist)
    # writecsvname1='prescription_4.csv'
    # data_process.createListCSV(writecsvname1, finalmedicallist)

    #step 5
    csvname='prescription_4.csv'





    # step other  检查一下功效和配伍是否一一对应
    # readcsvname1 = 'prescription_4.csv'
    # readcsvname2 = 'function.csv'
    # readcsvname3='indications.csv'
    # data1=checkitem(readcsvname1,readcsvname2,readcsvname3)
