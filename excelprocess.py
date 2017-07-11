# coding=utf-8
import xlrd
import csv
import codecs

# python3.5
# import sys
# import importlib
# importlib.reload(sys)

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def readexcel(excel_name,sheet_index):
    print ('readexcel')
    data = xlrd.open_workbook('exceldata/%s'%excel_name)
    # 获取一个工作表
    table = data.sheet_by_index(sheet_index)   #通过索引顺序获取 sheet从0张开始排序
    # table = data.sheet_by_name(u'Sheet1')  # 通过名称获取

    # 获取行数和列数
    nrows = table.nrows   #行数
    # ncols = table.ncols   #列数

    excelrow=[]
    for i in range(nrows) :
        # table.row_values(i)
        # print 'rows',table.row_values(i)
        excelrow.append(table.row_values(i))
    # for i in range(ncols):
    #     # table.col_values(i)
    #     print 'cols', table.col_values(i)
    return excelrow

 #从excel中读出数据保存在csv里
def exceltocsv(excel_name,sheet_index,csv_name):
    print ('exceltocsv')
    # excel_name='TCMdata.xls'
    # sheet_index=4     # 配伍功效{4:祛风解表；5：胜湿止痛；6：透疹；胜湿止痛；7：止痉；8：散肝舒脾；9：明目}
    excelrow=readexcel(excel_name, sheet_index)
    print ('********************excel****************************')
    # 查看从excel取出的data是否正确 start
    # a=0
    # b=0
    # for i in excelrow:
    #     for j in i:
    #         print '行列',a,b
    #         print 'content',j
    #         b+=1
    #     a+=1
    #     b=0
    # 查看从excel取出的data是否正确 end

    # csv_name='class_1.csv'
    write_in_csv(csv_name,excelrow)

#csv_name:要写入的cvs名称，datas：对应要写入的数据
def write_in_csv(csv_name,datas):
    print ('write_in_csv')
    csvfile = csv.writer('experimentdata/%s'%csv_name, 'wb')
    csvfile.write(codecs.BOM_UTF8)
    writer = csv.writer(csvfile)
    # writer.writerow(['id', 'url', 'keywords'])
    # data = [
    #   ('1', 'http://www.xiaoheiseo.com/', '小黑'),
    #   ('2', 'http://www.baidu.com/', '百度'),
    #   ('3', 'http://www.jd.com/', '京东')
    # ]

    writer.writerows(datas)
    #wb中的w表示写入模式，b是文件模式;写入一行用writerow;多行用writerows
    csvfile.close()

#把一个list即只有excel里的一列存入csv里，list=['','','']
#该函数专门使用在保存某列内容
def write_list_in_csv(csv_name,datas):
    print ('write_list_in_csv')
    csvfile = csv.reader('experimentdata/%s' % csv_name, 'wb')
    csvfile.write(codecs.BOM_UTF8)
    writer = csv.writer(csvfile)
    for item in datas:
        item = item.encode('utf-8')
        writer.writerow([item])
    csvfile.close()

# 功能：将一个二重列表[[],[]]写入到csv文件中
# 输入：文件名称，数据列表
def createListCSV(fileName, dataList):
    with csv.writer('experimentdata/%s' %fileName, "wb") as csvFile:
        csvWriter = csv.writer(csvFile)
        for data in dataList:
            csvWriter.writerow(data)
        csvFile.close()


def read_csv(csv_name):
    print ('read_csv')
    # python2.7
    csvfile = file('experimentdata/%s'%csv_name, 'rb')
    # print ('zzzzzzzzzzzzzzzz')
    csv_data = csv.reader(csvfile)
    # 查看取出指定行列的data start
    # a=0   #行
    # b=0   #列
    # for row in csv_data:
    #     # print(row)
    #     for col in row:
    #         if a==10 and b==0:
    #             print '10,0',col
    #         b+=1
    #     a+=1
    #     b=0
    # 查看取出的data end
    # python2.7

    #python3.5
    # csvdata=[]
    # with open('experimentdata/%s'%csv_name, "r", encoding="utf-8") as csvfile:
    #     # 读取csv文件，返回的是迭代类型
    #     csv_data = csv.reader(csvfile)
    #     for i in csv_data:
    #         csvdata.append(i)
    #         # print(i)
    # # csvfile.close()
    # print ('zzzzzzzzzzzzzzzz')
    # python3.5 最后要改为return csvdata


    # print csv_data
    return csv_data

#从一个csv（read_csv_name）中读出某列（col_index）要使用的信息并单独保存在另个csv中（write_csv_name）
#eg,读取class_1.csv中‘组成’列（col_index=6）的内容，并单独保存在composition_1.csv中
def extract_ingredients(read_csv_name,write_csv_name,col_index):
    print ('extract_ingredients')
    csvdata=read_csv(read_csv_name)
    # 查看取出指定行列的data start
    i=0
    # col_index=6
    content=[]

    for row in csvdata:
        print ('row',row)
        for col in row:
            if i==col_index:
                # print '行，组成列',col
                content.append(col)
            i+=1
        i=0

    for item in content:
        print ('item',item)
    # 查看取出的data end
    write_list_in_csv(write_csv_name, content)



if __name__ == '__main__':
    print ('main')

    # 一、从csv里提取出要用的某列信息，并单独保存在另一个新的csv里。 start

    #test时使用 start
    # read_csv_name = 'csvtest.csv'
    # write_csv_name = 'writecsvtest.csv'
    # col_index=0
    # test时使用 end

    # read_csv_name='class_6.csv'

    # write_csv_name='composition_6_class.csv'
    # col_index = 9   #要提取是csv中的那一列属性内容

    # write_csv_name = 'composition_6.csv'
    # col_index = 6  # 要提取是csv中的那一列属性内容
    #
    # extract_ingredients(read_csv_name, write_csv_name,col_index)
    # 一、从csv里提取出要用的某列信息，并单独保存在另一个新的csv里。 end

    # 二、测试一下提取的属性内容有没有对应 start
    # read_csv('composition_1_class.csv')
    # read_csv('composition_1.csv')
    # 二、测试一下提取的属性内容有没有对应 end


    # excel_name='TCMdata.xls'
    # sheet_index=9     # 配伍功效{4:祛风解表；5：胜湿止痛；6：透疹；胜湿止痛；7：止痉；8：散肝舒脾；9：明目}
    # csv_name='class_6.csv'
    # exceltocsv(excel_name, sheet_index, csv_name)
    # 三、其他功能测试 start
    # readexcel()
    # write_in_csv()
    # csv_name='class_1.csv'
    # read_csv(csv_name)
    # exceltocsv()
    # 三、其他功能测试 end
