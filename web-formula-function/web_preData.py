# coding=utf-8
import web_data_process
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')


#把爬取到的【组成】，配伍信息提取出来
def webOne(readcsvname):
    print 'webOne'
    csvdata = web_data_process.read_csv(readcsvname)
    formulalist=[]
    functionlist=[]
    zhuzhilist=[]
    num=0
    for item in csvdata:
        # print item
        for itemdata  in item:
            print num,itemdata.strip()
        try:
            formulalist.append(str(num)+'#'+item[1].strip())
            functionlist.append(str(num)+'#'+item[2].strip())
            zhuzhilist.append(str(num) + '#'+item[3].strip())
        except:
            pass
        num+=1

    print '........得到配伍数据共%d条 \n'%len(formulalist)

    # writecsvname='webFormula.csv'
    # web_data_process.write_list_in_csv_a(writecsvname,formulalist)
    # writecsvname='webFunction.csv'
    # web_data_process.write_list_in_csv_a(writecsvname,functionlist)
    # writecsvname='webZhuzhi.csv'
    # web_data_process.write_list_in_csv_a(writecsvname,zhuzhilist)


#去掉里面多的/t,/n等符号
def webTwo(readcsvname,writecsvname):
    print 'webTwo'
    csvdata = web_data_process.read_csv(readcsvname)
    formulalist=[]
    num=0
    for item in csvdata:
        # print num, item
        for itemdata in item:
            if itemdata!='':
                itemdata=itemdata.replace('\r','')
                itemdata = itemdata.replace('\n', '')
                itemdata = itemdata.replace('\t', '')
                itemdata = itemdata.replace('"', '')
                itemdata = itemdata.replace('\xc2\xa0', '')
                itemdata = itemdata.replace('\xe3\x80\x80\xe3\x80\x80', ' ')
                itemdata = itemdata.replace('\xe3\x80\x80', ' ')
                itemdata = itemdata.replace('】 ', '】')
                itemdata = itemdata.strip()
                print 'zz',num,itemdata
                formulalist.append(itemdata.decode('utf-8'))
                # formulalist.append(itemdata)
        # print num,item
        num+=1
    web_data_process.write_list_in_csv(writecsvname,formulalist)

def webThree(readcsvname,writecsvname):
    print 'webThree'
    csvdata = web_data_process.read_csv(readcsvname)
    formulalist = []
    num = 0
    for item in csvdata:
        # print 'item',item
        for itemdata in item:
            itemdata=itemdata.replace('﻿','')
            #把 “各” 字 单独处理
            # itemdata = itemdata.replace('各', '*')
            itemdata = itemdata.replace('【组成】', ' ')
            itemdata = itemdata.replace('，', ' ')
            itemdata = itemdata.replace('。', ' ')
            itemdata = itemdata.replace('、', '')
            itemdata = itemdata.replace('(原书未注用量)', '')
            itemdata = itemdata.replace('(原书未著用量)', '')
            itemdata = itemdata.replace('酒洗', '')
            itemdata = itemdata.replace('洗', '')
            itemdata = itemdata.replace('汤洗七次', '')
            print 'itemdata', itemdata
            formulalist.append(itemdata)
    web_data_process.write_list_in_csv(writecsvname, formulalist)

def webFour(readcsvname,writecsvname):
    print 'webFour'

if __name__ == '__main__':
    print ('爬取数据预处理进行....')
    #step 1
    # readcsvname1 = 'all_tcm166.csv'
    # readcsvname2 = 'all_zhongyoo.csv'
    # webOne(readcsvname1)
    # webOne(readcsvname2)

    #step 2
    # readcsvname = 'webFormula.csv'
    # writecsvname='webFormula_1.csv'
    # webTwo(readcsvname,writecsvname)
    #
    # readcsvname = 'webFunction.csv'
    # writecsvname = 'webFunction_1.csv'
    # webTwo(readcsvname,writecsvname)
    #
    # readcsvname = 'webZhuzhi.csv'
    # writecsvname = 'webZhuzhi_1.csv'
    # webTwo(readcsvname,writecsvname)

    #step 3 处理配伍信息
    # readcsvname = 'webFormula_1.csv'
    # writecsvname = 'webFormula_2.csv'
    # webThree(readcsvname,writecsvname)

    readcsvname = 'webFormula_2.csv'
    writecsvname = 'webFormula_3.csv'
    webFour(readcsvname,writecsvname)