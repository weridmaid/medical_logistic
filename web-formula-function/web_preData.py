# coding=utf-8
import web_data_process
import web_dataDetailProcess
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

#去除一些不要的描述
def wordmatch(str):
    print 'wordmatch'
    pattern = re.compile(ur'(?:炙|微炙赤|不|蒸|炒|熬|炒香|炮|切|轧细|捣碎|裹煨|研粉|调下|另研|碎绵裹|微|生用|酒|捣细|煅)')
    str = re.sub(pattern, '', str)

    return str
#通过正则表达去除多余的单位，只保留数值+g的单位。 中文字符串一定要decode(utf-8)编码
#注意！！！！ 葛根十五两(450g) 会被处理为 葛(450g)这是错误的！请手动检查一下
def match(str):
    print 'match'
    print str
    pattern = re.compile(
        ur'(?:一|二|三|四|五|六|七|八|九|十|半|百|两|钱)*(半|两|钱|升|斤|枚|分|个|片个|条|份|张|枚|具|朵|只|粒|茎|挺|对|头|合)至(?:一|二|三|四|五|六|七|八|九|十|半|百|两|钱)*(半|两|钱|升|斤|枚|分|个|片个|根|条|份|张|枚|具|朵|只|粒|茎|挺|对|头|合)(?=\(\d+)')
    pattern1 = re.compile(ur'(?:一|二|三|四|五|六|七|八|九|十|半|百|两|钱)*至(?:一|二|三|四|五|六|七|八|九|十|半|百|两)*(半|两|钱|升|斤|枚|分|个|片个|根|条|份|张|枚|具|朵|只|粒|茎|挺|对|头|合)(?=\(\d+)')
    pattern2 = re.compile(ur'(?:一|二|三|四|五|六|七|八|九|十|半|百|两|钱)*(半|两|钱|升|斤|枚|分|个|片个|根|条|份|张|枚|具|朵|只|粒|茎|挺|对|头|合)(?=\(\d+)')
    pattern3 = re.compile(ur'(?:一|二|三|四|五|六|七|八|九|十|半|百|两|钱)*(半|两|钱|升|斤|枚|分|个|片个|根|条|份|张|枚|具|朵|只|粒|茎|挺|对|头|合)(?=\()')
    str = re.sub(pattern, '', str)
    str = re.sub(pattern1, '', str)
    str = re.sub(pattern2, '', str)
    str = re.sub(pattern3, '', str)

    # print '替换str',str
    return str

#通过正则表达去除多余的单位，只保留数值+g的单位。 中文字符串一定要decode(utf-8)编码
#注意！！！！ 葛根十五两(450g) 会被处理为 葛(450g)这是错误的！请手动检查一下
def match1(str):
    print 'match'
    print str
    pattern1 = re.compile(ur'(?:一|二|三|四|五|六|七|八|九|十|半|百|两|钱){2}(?:半|两|钱|升|斤|枚|分|个|片|把|片个|根|条|枝|份|张|枚|具|朵|只|粒|茎|挺|对|头|合)')
    pattern2 = re.compile(ur'(?:一|二|三|四|五|六|七|八|九|十|半|百|两|钱){1}(?:半|两|钱|升|斤|枚|分|个|片|把|片个|根|条|枝|份|张|枚|具|朵|只|粒|茎|挺|对|头|合)')
    str = re.sub(pattern1, '', str)
    str = re.sub(pattern2, '', str)
    # print '替换str',str
    return str




#把爬取到的【组成】【功效】【主治】信息分开提取出来
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


#去掉爬取网页里出现的/t,/n等符号
def webTwo(readcsvname,writecsvname):
    print 'webTwo'
    csvdata = web_data_process.read_csv(readcsvname)
    formulalist=[]
    num=0
    for item in csvdata:
        # print num, item
        for itemdata in item:
            if itemdata!='':
                itemdata = itemdata.decode('utf8')
                itemdata=itemdata.replace('\r','')
                itemdata = itemdata.replace('\n', '')
                itemdata = itemdata.replace('\t', '')
                itemdata = itemdata.replace('"', '')
                itemdata = itemdata.replace('\xc2\xa0', '')
                itemdata = itemdata.replace('\xe3\x80\x80\xe3\x80\x80', ' ')
                itemdata = itemdata.replace('\xe3\x80\x80', ' ')
                itemdata = itemdata.replace('】 ', '】')
                #webThree
                itemdata = itemdata.replace('﻿', '')
                itemdata = itemdata.replace('【组成】', ' ')
                itemdata = itemdata.replace('，', ' ')
                itemdata = itemdata.replace('。', ' ')
                itemdata = itemdata.replace('、', '')
                itemdata = itemdata.replace('(原书未注用量)', '')
                itemdata = itemdata.replace('(原书未著用量)', '')
                itemdata = itemdata.replace('酒洗', '')
                itemdata = itemdata.replace('洗', '')
                itemdata = itemdata.replace('汤洗七次', '')
                # webThree
                itemdata = itemdata.strip()
                print 'zz',num,itemdata
                formulalist.append(itemdata.decode('utf-8'))
                # formulalist.append(itemdata)
        # print num,item
        num+=1
    web_data_process.write_list_in_csv(writecsvname,formulalist)

#按空格分割提取每个成分；
#eg.地骨皮30g  防风30g  甘草15g(微炙) =============> 地骨皮30g,防风30g,甘草15g(微炙)
def webFour(readcsvname,writecsvname):
    print 'webFour'
    data=web_dataDetailProcess.composition_process(readcsvname)
    web_data_process.write_in_csv(writecsvname, data)

def webFive(readcsvname,writecsvname):
    print 'webFive'
    csvdata = web_data_process.read_csv(readcsvname)
    data=[]
    num=0
    for content in csvdata:
       j=0
       for item in content:
           item=item.decode('utf-8')
           pos=item.find('去')
           if pos>-1:
               item=item[0:pos]

           x = wordmatch(item)
           # x = item.replace('炙', '')
           # x = x.replace('不', '')
           # x = x.replace('蒸', '')
           # x = x.replace('炒', '')
           # x = x.replace('熬', '')
           # x = x.replace('锉', '')
           # x = x.replace('炒香', '')
           # x = x.replace('炮', '')
           # x = x.replace('切', '')
           # x = x.replace('轧细', '')
           # x = x.replace('捣碎', '')
           # x = x.replace('裹煨', '')
           # x = x.replace('研粉', '')
           # x = x.replace('调下', '')
           # x = x.replace('另研', '')
           # x = x.replace('碎绵裹', '')


           # 通过正则表达去除多余的单位，只保留数值+g的单位。
           str = match(x)
           content[j]=str
           # print 'item - x',num,j,item,x
           j+=1
       data.append(content)
       num+=1
    web_data_process.write_in_csv(writecsvname, data)

#
def webSix(readcsvname,writecsvname):
    print 'webFive'
    csvdata = web_data_process.read_csv(readcsvname)
    data=[]
    num=0
    for content in csvdata:
       j=0
       for item in content:
           item=item.decode('utf-8')
           str=match1(item)
           content[j]=str
           # print 'item - x',num,j,item,x
           j+=1
       data.append(content)
       num+=1
    web_data_process.write_in_csv(writecsvname, data)

def webProcessNum(readcsvname,writecsvname):
    print 'webProcessNum'
    csvdata = web_data_process.read_csv(readcsvname)
    finaldata = []
    num = 0

    pattern3 = re.compile(ur'\d+(?:g|kg|ml|l|个|Kg|钱|片|根|条|份|张|枚|具|朵|只|粒|茎|两|斤|挺|对|头|L|ML|分|节|cm|握|株)')
    pattern4 = re.compile(ur'\d+.\d+(?:g|kg|ml|Kg|l|个|钱|片|根|条|份|张|枚|具|朵|只|粒|茎|两|斤|挺|对|头|L|ML|分|节|cm|握|株)')

    pattern1 = re.compile(ur'[\u4e00-\u9fa5]+(\(|（)')
    pattern2 = re.compile(ur'(?:\(|（|）|\))')

    pattern5=re.compile(ur'(?<![\u4e00-\u9fa5])(?:\(|（)\d+(?:g|kg|ml|l|个|Kg|钱|片|根|条|份|张|枚|具|朵|只|粒|茎|两|斤|挺|对|头|L|ML|分|节|cm|握|株)(?:\)|）)(?![\u4e00-\u9fa5])')
    pattern6 = re.compile(ur'(?:\)|）)(?=[\u4e00-\u9fa5]+)')

    pattern7=re.compile(ur'(?:\(|（)')
    for content in csvdata:
        j = 0
        medicallist = []
        yaowulist=[]
        try:
            content.remove('')
        except:
            pass
        for item in content:
            item = item.decode('utf-8')
            if j==0:
                medicallist.append(content[0])
            else:
                #情况一：升麻 =》只有字
                if not pattern3.search(item):
                    print '1', item
                    word =item
                    wordnumber='None'
                    medicallist.append(word)
                    medicallist.append(wordnumber)

                #情况三：（6g）=>只有数量
                if pattern5.search(item):
                    print '3',item
                    wordnumber = re.sub(pattern2, '', item)
                    k=0
                    for item in medicallist:
                        if item == 'None':
                            medicallist[k] = wordnumber
                        k += 1

                #情况五：处理‘各’：各(30g) or 焦栀各(各9g)
                if item.find('各')>-1:
                    # print '各',item
                    item=item.replace('各','')
                    item = re.sub(pattern2, '', item)
                    #找到整数 或者 小数
                    weight1 = pattern4.findall(item) #小数
                    weight2 = pattern3.findall(item) #整数
                    # 把正确的值放在变量weight中
                    if (weight1):
                        wordnumber = weight1[0]
                        yaowulist=pattern4.split(item)
                    elif (weight2):
                        wordnumber = weight2[0]
                        yaowulist = pattern3.split(item)
                        # 把处方的每味药提出来重新放在medicallist列表元素[0]里，同时已经去除了药的数量单位
                    if (yaowulist):
                            try:
                                for zz in yaowulist:
                                    if zz!=u'':
                                        word=zz
                                        # print 'word',word
                                        medicallist.append(word)
                                        medicallist.append(wordnumber)
                            except:
                                pass
                    k=0
                    for item in medicallist:
                        if item =='None':
                            medicallist[k]=wordnumber
                        k+=1

                #情况二：麻黄（6g）
                if pattern1.search(item):
                    # print '麻黄（6g）',item
                    word=item[0:pattern7.search(item).start()]
                    # print 'bb',word
                    wordnumber=item[pattern7.search(item).end():]
                    wordnumber=re.sub(pattern2,'',wordnumber)
                    # print 'nn',wordnumber

                    medicallist.append(word)
                    medicallist.append(wordnumber)

                #情况四：（6g）麻黄
                if pattern6.search(item):
                    wordnumber = item[:pattern6.search(item).start()]
                    wordnumber = re.sub(pattern2, '', wordnumber)
                    word = item[pattern6.search(item).end():]

                    medicallist.append(wordnumber)
                    medicallist.append(word)

            j+=1
        finaldata.append(medicallist)
        num += 1
    web_data_process.write_in_csv(writecsvname,finaldata)




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

    #step3已和step2合并，所以删除了

    #step 4 按空格切割为数组
    # readcsvname = 'webFormula_2.csv'
    # writecsvname = 'webFormula_3.csv'
    # webFour(readcsvname,writecsvname)

    #step 5  处理配伍信息 和 step 2 一个意思
    # readcsvname = 'webFormula_3.csv'
    # writecsvname = 'webFormula_4.csv'
    # webFive(readcsvname,writecsvname)

    #step 6 通过正则表达去除多余的单位，只保留 数值+g 的单位。
    # readcsvname = 'webFormula_4.csv'
    # writecsvname = 'webFormula_5.csv'
    # webSix(readcsvname,writecsvname)


    #最后一步
    readcsvname = 'webFormula_5.csv'
    writecsvname = 'webFormula_6.csv'
    webProcessNum(readcsvname,writecsvname)



    #正则表达式 test
    # str='青子芩钱半至三钱(4.5g～9g)'.decode('utf8')
    # # str = '黄芩三两(9g)'.decode('utf8')
    # match(str)
    # 正则表达式 test

    # pattern6 = re.compile(ur'(?:\)|）)(?=[\u4e00-\u9fa5]+)')
    # str='（6g）麻黄'.decode('utf8')
    # match = pattern6.search(str)
    # print match.group()



