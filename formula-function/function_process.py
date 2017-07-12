# coding=utf-8
import data_process
import dataDetailProcess


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

def function_count():
    print 'function_count 计算有多少种功效，每种功效出现的次数和比例*'

if __name__ == '__main__':
    print ('功效数据清洗进行中....')

    #step 1 处理文本中的符号
    # readcsvname='function.csv'
    # writecsvname='function_1.csv'
    # csv_data=data_process.read_csv(readcsvname)
    # datalist=process_symbol(csv_data)
    # data_process.write_in_csv(writecsvname,datalist)

    #step 2 计算有多少种功效，每种功效出现的次数和比例