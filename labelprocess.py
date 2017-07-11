# coding=utf-8
import re
import excelprocess
# python3.5
# import sys
# import importlib
# importlib.reload(sys)

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

label_1=0
label_2=1
label_3=2
label_4=3
label_5=4
label_6=5
#没用label_other
label_other=6

# ****************************输入：compostion_1_class.csv ~ compostion_6_class.csv; 输出：alllabelData.csv***********************************
#取出allData_normal1.csv里每条处方对应的标签（注意：可对应多标签）
#把六个类的数据全部放在一个csv里:alllabelData.csv
#eg.*6*247,祛风解表(风热)　目
def createAllLableList():
    print ('createAllLableLis')
    addlist = []
    for inum in range(1,7):
        print ('inum',inum)
        readcsvname='composition_'+str(inum)+'_class.csv'
        csvdata = excelprocess.read_csv(readcsvname)
        pnum='*'+str(inum)
        # print 'csvdata',csvdata
        i=1
        for item in csvdata:
            pnum=pnum+'*'+str(i)
            item.insert(0,pnum)
            # print 'zzzz:',item
            addlist.append(item)
            pnum='*'+str(inum)
            i+=1
    # writecsvname = 'allLabelData.csv'
    # excelprocess.write_in_csv(writecsvname, addlist)


# ****************************输入：alllabelData.csv; 输出：allLabelDataValue.csv***********************************
def transLabelvalue():
    print ('transLabelvalue')
    readcsvname = 'allLabelData.csv'
    csvdata = excelprocess.read_csv(readcsvname)
    labelList=[]
    for item in csvdata:
        data_after = []
        # print 'item:',item
        mark = 0
        for itemdata in item:
            if(mark==0):
                data_after.append(itemdata)
                mark+=1
                continue
            else:
                itemdata = itemdata.replace('﻿', '')
                itemdata = itemdata.replace(';', '；')
                itemdata=itemdata.split('；')
                # print 'itemdata', itemdata
                for labelitem in itemdata:
                    if (labelitem.find('祛风解表')>-1):
                        # print 'itemdata', itemdata
                        data_after.append(label_1)
                    elif(labelitem.find('胜湿止痛')>-1):
                        data_after.append(label_2)
                    elif (labelitem.find('止痒') > -1 or labelitem.find('透疹')>-1):
                        data_after.append(label_3)
                    elif (labelitem.find('止痉') > -1 or labelitem.find('中风')> -1):
                        data_after.append(label_4)
                    elif (labelitem.find('散肝舒脾') > -1 ):
                        data_after.append(label_5)
                    elif (labelitem.find('目') > -1 or labelitem.find('明目')> -1):
                        data_after.append(label_6)
                    else:
                        # data_after.append(label_other)
                        print ('error:',item[0])
            labelList.append(data_after)

    # writecsvname = 'allLabelDataValue.csv'
    # excelprocess.write_in_csv(writecsvname, labelList)


if __name__ == '__main__':
    print ('labelprocess.py *** main')
    # createAllLableList()
    transLabelvalue()