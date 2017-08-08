# coding=utf-8
import data_process
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

def pickFunction(readcsvname1,readcsvname2,writecsvname1,writecsvname2,function):
    print 'pickFunction'
    funcdata = data_process.read_csv(readcsvname1)
    presdata = data_process.read_csv(readcsvname2)
    funclist=[]
    preslist=[]
    for item in presdata:
        preslist.append(item)
    for item in funcdata:
        funclist.append(item)

    finalpreslist=[]
    finalfunclist = []
    print "要选择的方剂功效为 %s:"%function
    print "正在进行中....."
    num=0
    for item in funclist:
        for itemdata in item:
            itemdata=itemdata.decode('utf8')
            if itemdata.find(function)>-1 and len(preslist[num])>=3:
                finalfunclist.append(item)
                finalpreslist.append(preslist[num])
                break
        num+=1
    print "功效%s 在5W数据集的方剂中找到含有该功效方剂 %d 条。"%(function,len(finalfunclist))
    print "收集负例中.....（设置负例为正例个数的1.3倍）"
    num=0
    count=0
    neglength=len(finalfunclist)*1.3
    for item in funclist:
        if(num%50==0):
            check=True
            for itemdata in item:
                itemdata=itemdata.decode('utf8')
                if itemdata.find(function)>-1:
                    check=False
                    break
                #近义词也要考虑过滤
                if itemdata.find('清热')>-1:
                    check=False
                    break
                if itemdata.find('解毒')>-1:
                    check=False
                    break
            if check and count<neglength:
                if len(preslist[num])>3:
                    finalfunclist.append(item)
                    finalpreslist.append(preslist[num])
                    count+=1
            if count>neglength:
                break
        num+=1


    print "功效%s 在5W数据集的方剂中正负样例共有 功效：%d 配伍：%d 条。" % (function, len(finalfunclist),len(finalpreslist))
    data_process.write_in_csv(writecsvname1,  finalfunclist)
    data_process.write_in_csv(writecsvname2, finalpreslist)

if __name__ == '__main__':
    print ('功效数据清洗进行中....')
    #step 1 选取指定功效，并搭配负例组成样本集

    function = "清热解毒"
    readcsvname1='../formulaData_1/func_5W_1.csv'
    readcsvname2 = '../formulaData_1/pres_5W_4.csv'
    writecsvname1 = '../formulaData_1/QRJD_func.csv'
    writecsvname2 = '../formulaData_1/QRJD_pres.csv'

    pickFunction(readcsvname1, readcsvname2, writecsvname1, writecsvname2,function)

