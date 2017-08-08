# coding=utf-8
import data_process
import dataDetailProcess
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

def pickData(csv_name,csvname1,csvname2):
    print 'pickData'
    preslist=[]
    funclist=[]
    write_csv_name=''
    #取出功能主治
    funcContent=data_process.extract_ingredients(csv_name,write_csv_name,col_index=4)
    presContent = data_process.extract_ingredients(csv_name, write_csv_name, col_index=2)
    num=0
    for item in funcContent:
        bianhao='#'+str(num)+'# '
        funclist.append(bianhao+item)
        num+=1
    print '功效个数:',len(funclist)
    num=0
    for item in presContent:
        bianhao='#'+str(num)+'# '
        preslist.append(bianhao+item)
        num+=1
    print '方剂个数:', len(preslist)

    data_process.write_list_in_csv(csvname1,preslist)
    data_process.write_list_in_csv(csvname2, funclist)

def extractnumfromstr(readcsvname,writecsvname):
    print ('extractnumwithstr')
    csvdata = data_process.read_csv(readcsvname)

    # 正则匹配要用' ur'' '才能正确匹配中文
    # (?:..):(...)的不分组版本，用于使用| 或 后接数量词
    pattern1 = re.compile(ur'\d+.\d+(?:g|kg|ml|l|千克|克|钱半|斤半|分半|升半|升|个|钱|片|根|条|份|张|枚|寸|具|朵|只|粒|茎|两半|斤|文|挺|对|头|L|ML|分|节|cm|握|株|两|铢)')
    pattern2 = re.compile(ur'\d+(?:g|kg|ml|l|千克|克|钱半|分半|斤半|升半|升|个|钱|片|根|条|份|张|枚|寸|具|朵|只|合|粒|茎|两半|斤|文|挺|对|头|L|ML|分|节|cm|握|株|两|铢)')
    pattern3 = re.compile(
        ur'\d+(?:g|kg|ml|l|千克|克|钱半|分半|斤半|升半|升|个|钱|片|根|条|份|张|枚|寸|具|朵|只|粒|茎|两半|斤|文|挺|合|对|头|L|ML|分|节|cm|握|株|两|铢)\d+(?:g|kg|ml|l|克|钱半|分半|斤半|升半|升|个|钱|片|根|条|份|张|枚|具|朵|只|粒|茎|两半|斤|文|挺|对|头|L|ML|分|节|cm|握|株|两|铢)')
    pattern4 = re.compile(
        ur'(?:一|二|三|四|五|六|七|八|九|十|两|半)(?:g|kg|ml|l|千克|克|钱半|斤半|分半|升半|升|个|钱|片|根|条|份|合|张|枚|寸|具|朵|只|粒|茎|两半|斤|文|挺|对|头|L|ML|分|节|cm|握|株|两|铢)')

    pattern_other=re.compile(ur'(?:等分|适量|少许)')
    medicallist = []
    for item in csvdata:
        print '****************************************************************** 处方： ', item[0]
        checkBH = 0
        medical = []
        for itemdata in item:
            check_ge=False
            weight = 'None'
            if checkBH:
                itemdata = itemdata.replace('﻿', '')
                itemdata = itemdata.replace('．', '.')
                itemdata = itemdata.replace('o', '0')
                itemdata = itemdata.decode('utf8')
                # print 'itemdata', itemdata
                if itemdata.find('各')>-1:
                    check_ge=True
                itemdata = itemdata.replace('各', '')
                itemdata = re.sub(pattern_other, '', itemdata)
                match1 = pattern3.search(itemdata)#组合，1两2钱
                match2 = pattern1.search(itemdata)#小数
                match3 = pattern2.search(itemdata)#整数
                match4 = pattern4.search(itemdata)#汉字单位

                if match1:
                    yaowu = re.sub(pattern3, '', itemdata)
                    weight = match1.group()
                    if yaowu:
                        medical.append(yaowu)
                    medical.append(weight)
                    if medical[-2] == 'None':
                        medical.pop(-2)
                elif match2:
                    yaowu = re.sub(pattern1, '', itemdata)
                    weight = match2.group()
                    if yaowu:
                        medical.append(yaowu)
                    medical.append(weight)
                    if medical[-2] == 'None':
                        medical.pop(-2)
                elif match3:
                    yaowu = re.sub(pattern2, '', itemdata)
                    weight = match3.group()
                    if yaowu:
                        medical.append(yaowu)
                    medical.append(weight)
                    if medical[-2] == 'None':
                        medical.pop(-2)
                elif match4:
                    yaowu = re.sub(pattern4, '', itemdata)
                    weight = match4.group()
                    if yaowu:
                        medical.append(yaowu)
                    medical.append(weight)
                    if medical[-2] == 'None':
                        medical.pop(-2)
                else:
                    if itemdata:
                        medical.append(itemdata)
                        medical.append('None')

                if check_ge:
                    num=0
                    for i in medical:
                        if i=='None':
                            medical[num]=weight
                        num+=1
            else:
                medical.append(itemdata)
            checkBH+=1
            # print 'medical',medical
        medicallist.append(medical)
        medical=[]
    finalmedicallist=[]
    for content in medicallist:
        num=0
        for icontent in content:
            if icontent.find('～')>-1:
                content[num]=icontent[icontent.find('～')+1:]
            if icontent.find('-') > -1:
                content[num] = icontent[icontent.find('-') + 1:]
            num+=1
        finalmedicallist.append(content)
    return finalmedicallist


if __name__ == '__main__':
    print 'dataFrom5w main...'
    ######################  一、先把数据单独提出来 分别预处理
    # readexcelname='../exceldata/5w_data.xlsx'
    # csv_name='../formulaData_1/data5W.csv'

    #step 1 把5w_data.xlsx表的全部内容存放在一个csv里(后续可略去
    # sheet_index=0
    # data_process.exceltocsv(readexcelname,sheet_index,csv_name)

    # step 2 把功效和配伍单独提出来放在单独的csv里处理
    # csvname1 = '../formulaData_1/pres_5W.csv'
    # csvname2 = '../formulaData_1/func_5W.csv'
    # pickData(csv_name,csvname1,csvname2)


    ###################### 二、开始正式处理配伍数据
    #step 1 处理文本中的空格逗号、分号等,切割
    # readcsvname='../formulaData_1/pres_5W.csv'
    # writecsvname='../formulaData_1/pres_5W_1.csv'
    # dataDetailProcess.composition_process(readcsvname,writecsvname)

    #step 2 处理用空格切割后还存在的多余的空格？       7-31 不需要这步
    # readcsvname='../formulaData_1/pres_5W_1.csv'
    # writecsvname='../formulaData_1/pres_5W_2.csv'
    # dataDetailProcess.process_blank(readcsvname,writecsvname)

    # step 3 去括号等一些附加说明
    # (1)去掉‘各’字或括号内容（还有小部分扩号需人工去除
    # readcsvname ='../formulaData_1/pres_5W_1.csv'
    # datalist=dataDetailProcess.splitnumandstr(readcsvname)
    # writecsvname='../formulaData_1/pres_5W_2.csv'
    # data_process.write_in_csv(writecsvname, datalist)

    # (2)删除没有内容的项  start（需重复做两~三次 处理,,,这种连着的情况
    # readcsvname ='../formulaData_1/pres_5W_2.csv'
    # writecsvname='../formulaData_1/pres_5W_3.csv'
    # csvdata = data_process.read_csv(readcsvname)
    # datas = []
    # for item in csvdata:
    #     num = 0
    #     for itemdata in item:
    #         if itemdata == '':
    #             item.pop(num)
    #         num += 1
    #     datas.append(item)
    # data_process.write_in_csv(writecsvname, datas)
    #删除没有内容的项  end


    # # (3)药名-数量单位 一一提取匹配；处理“各”的情况 补填；处理“等分”，“少许”等词清除
    readcsvname='../formulaData_1/pres_5W_3.csv'
    writecsvname='../formulaData_1/pres_5W_4.csv'
    finalmedicallist=extractnumfromstr(readcsvname, writecsvname)
    data_process.write_in_csv(writecsvname, finalmedicallist)

    #8-1 目前考虑用one-hot表示，先不做这步
    # #step 5 把单位kg,钱，两 统一为 g（克）
    # csvname='../formulaData_1/pres_5W_4.csv'
    # normalList= dataDetailProcess.unitTransformation(csvname)
    # writecsvname='../formulaData_1/pres_5W_5.csv'
    # data_process.write_in_csv(writecsvname, normalList)
    #
    # #step 6 清洗一些none单位的杂音 如‘等分，少许’
    # csvname='../formulaData_1/pres_5W_5.csv'
    # noneList= dataDetailProcess.noneStandard(csvname)
    # writecsvname='../formulaData_1/pres_5W_6.csv'
    # data_process.write_in_csv(writecsvname, noneList)


