# coding=utf-8
import web_data_process
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def process_symbol(csv_data):
    print 'process_symbol 处理中文符号 '
    num=0
    datalist=[]
    for item in csv_data:
        # print 'item :',num,item
        fcontent=item[0].replace('。','')
        fcontent= fcontent.replace(' ', '')
        data=fcontent.split('，')
        # print 'split item',data
        datalist.append(data)
        num+=1
    print len(datalist)
    return datalist

def function_count(csvname):
    print 'function_count 计算有多少种功效，每种功效出现的次数和比例*'
    csv_data = web_data_process.read_csv(csvname)
    flist=[]
    for item in csv_data:
        for itemdata in item:
            itemdata=itemdata.replace('疏风','祛风')
            itemdata = itemdata.replace('散风', '祛风')
            itemdata = itemdata.replace('驱风', '祛风')
            flist.append(itemdata)
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
def func2feature(csvname1,csvname2):
    print 'func2feature'
    funcdata = web_data_process.read_csv(csvname1)
    countdata = web_data_process.read_csv(csvname2)

    countlist=[]
    for item in countdata:
        countlist.append(item[0])

    featurelist=[]
    #这里可以修改需要判别的功效，放一个时会检索不到（‘.-’）
    locmark= countlist.index('祛风清热'.decode('utf-8'))
    print 'locmark',locmark
    for item in funcdata:
        check=0
        for itemdata in item :
            itemdata=itemdata.replace('疏风','祛风')
            itemdata = itemdata.replace('散风', '祛风')
            itemdata = itemdata.replace('驱风', '祛风')
            try:
                loc = countlist.index(itemdata.decode('utf-8'))
                if loc==locmark:
                    check=1
            except:
                pass
        if check==1:
            featurelist.append(1)
        else:
            featurelist.append(0)
    print 'len(featurelist):',len(featurelist)
    print '有多少方剂属于该功效（祛风清热）：',featurelist.count(1)
    return featurelist

if __name__ == '__main__':
    print ('功效数据清洗进行中....')

    #step 1 处理文本中的符号
    # readcsvname='function.csv'
    # writecsvname='function_1.csv'
    # csv_data=data_process.read_csv(readcsvname)
    # datalist=process_symbol(csv_data)
    # data_process.write_in_csv(writecsvname,datalist)

    #step 2 计算有多少种功效，每种功效出现的次数和比例
    # csvname='function_1.csv'
    # numarray=function_count(csvname)
    # writecsvname = 'function_count.csv'
    # writecsvname='function_count_replace.csv'
    # data_process.write_in_csv(writecsvname,numarray)

    #step 3 计算功效的类标特征向量
    csvname1='function_1.csv'
    csvname2='function_count_replace.csv'
    featurelist=func2feature(csvname1,csvname2)
    writecsvname='funcFeature.txt'
    web_data_process.write_list_in_csv(writecsvname, featurelist)
