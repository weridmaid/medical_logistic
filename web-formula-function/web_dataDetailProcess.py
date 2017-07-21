# coding=utf-8
import re
import web_data_process

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#****************************输入：compostion_1.csv;输出：composition_1_1.csv***********************************
#把compostion_1.csv里的数据取出来，按空格分割提取每个成分；
#注意！这里处理后有的数据会出现多余的空格！***************手动处理那些多余的空格。。。**************************
#eg.地骨皮30g  防风30g  甘草15g(微炙) =============> 地骨皮30g,防风30g,甘草15g(微炙)
def composition_process(readcsvname):
    print ('composition_process')
    # readcsvname='composition_6.csv'
    csvdata=web_data_process.read_csv(readcsvname)
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

    return datas

