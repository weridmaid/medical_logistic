# coding=utf-8
import data_process
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

def process_symbol(csv_data):
    print 'process_symbol 处理中文符号 '
    datalist=[]
    pattern=re.compile(ur'(?:主|治|适用于|用于|适用|等)')
    for item in csv_data:
        # print 'item :',num,item
        item[0]=item[0].decode('utf8')
        fcontent=item[0].replace('。','，')
        fcontent= fcontent.replace('、', '，')
        fcontent = fcontent.replace('；', '，')
        fcontent = fcontent.replace(' ', '，')
        fcontent = fcontent.replace(';', '，')
        fcontent = re.sub(pattern,'',fcontent)
        data=fcontent.split('，')
        # print 'split item',data
        try:
            data.remove('')
        except:
            pass
        try:
            data.remove('')
        except:
            pass
        datalist.append(data)
    print len(datalist)
    return datalist

def function_count(csvname):
    print 'function_count 计算有多少种功效，每种功效出现的次数和比例*'
    csv_data = data_process.read_csv(csvname)
    flist=[]

    for item in csv_data:
        checknum = 0
        for itemdata in item:
            if checknum!=0:
                itemdata=itemdata.replace('疏风','祛风')
                itemdata = itemdata.replace('散风', '祛风')
                itemdata = itemdata.replace('驱风', '祛风')
                flist.append(itemdata)
            checknum+=1
    print '所有方剂中的功效有（没有去重）：',len(flist)
    #去重 计算有多少不同的功效
    flistset=list(set(flist))

    # 统计每种药物出现的次数
    numarray = []
    n = []
    for item in flistset:
        n.append(item)
        n.append(flist.count(item))
        numarray.append(n)
        n = []
    # 以次数排序
    numarray = sorted(numarray, key=lambda x: x[1], reverse=True)
    print '所有方剂中的功效有（去重）：', len(numarray)

    return  numarray

def func2feature(csvname1,function):
    print 'func2feature'
    funcdata = data_process.read_csv(csvname1)

    featurelist=[]

    for item in funcdata:
        check=False
        for itemdata in item :
            itemdata=itemdata.decode('utf-8')
            itemdata=itemdata.replace('疏风','祛风')
            itemdata = itemdata.replace('散风', '祛风')
            itemdata = itemdata.replace('驱风', '祛风')
            if itemdata.find(function)>-1:
                check=True
        if check:
            featurelist.append(1)
        else:
            featurelist.append(0)
    print 'len(featurelist):',len(featurelist)
    print '有多少方剂属于该功效（祛风除湿）：',featurelist.count(1)
    return featurelist

if __name__ == '__main__':
    print ('功效数据清洗进行中....')

    #step 1 处理文本中的符号
    # readcsvname='../formulaData_1/func_5W.csv'
    # writecsvname='../formulaData_1/func_5W_1.csv'
    # csv_data=data_process.read_csv(readcsvname)
    # datalist=process_symbol(csv_data)
    # data_process.write_in_csv(writecsvname,datalist)

    #step 2 计算有多少种功效，每种功效出现的次数和比例
    # csvname='../formulaData_1/func_5W_1.csv'
    # numarray=function_count(csvname)
    # writecsvname='../formulaData_1/func_5W_count.csv'
    # data_process.write_in_csv(writecsvname,numarray)

    #step 3 计算功效的类标特征向量
    # csvname1='function_1.csv'
    # csvname2='function_count_replace.csv'

    csvname1='../formulaData_1/QRJD_func.csv'
    function='清热解毒'
    featurelist=func2feature(csvname1,function)
    writecsvname='../formulaData_1/FuncFeature_QRJD.csv'
    data_process.write_list_in_csv(writecsvname,featurelist)
