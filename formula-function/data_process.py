# coding=utf-8
import xlrd
import csv
import codecs

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def readexcel(excel_name,sheet_index):
    print ('readexcel')
    data = xlrd.open_workbook('../exceldata/%s'%excel_name)
    # 获取一个工作表
    table = data.sheet_by_index(sheet_index)   #通过索引顺序获取 sheet从0张开始排序
    # 获取行数和列数
    nrows = table.nrows   #行数
    excelrow=[]
    for i in range(nrows) :
        excelrow.append(table.row_values(i))
    return excelrow

 #从excel中读出数据保存在csv里
def exceltocsv(excel_name,sheet_index,csv_name):
    print ('exceltocsv')
    excelrow=readexcel(excel_name, sheet_index)
    print ('********************excel****************************')
    write_in_csv(csv_name,excelrow)

#csv_name:要写入的cvs名称，datas：对应要写入的数据
def write_in_csv(csv_name,datas):
    print ('write_in_csv')
    csvfile = file('../formulaData/%s'%csv_name, 'wb')
    csvfile.write(codecs.BOM_UTF8)
    writer = csv.writer(csvfile)
    writer.writerows(datas)
    #wb中的w表示写入模式，b是文件模式;写入一行用writerow;多行用writerows
    csvfile.close()

#把一个list即只有excel里的一列存入csv里，list=['','','']
#该函数专门使用在保存某列内容
def write_list_in_csv(csv_name,datas):
    print ('write_list_in_csv')
    csvfile = file('../formulaData/%s' % csv_name, 'wb')
    csvfile.write(codecs.BOM_UTF8)
    writer = csv.writer(csvfile)
    for item in datas:
        # item = item.encode('utf-8')
        writer.writerow([item])
    csvfile.close()

# 功能：将一个二重列表[[],[]]写入到csv文件中
# 输入：文件名称，数据列表
def createListCSV(fileName, dataList):
        csvFile = file('../formulaData/%s' % fileName, 'wb')
    # with csv.writer('../formulaData/%s' %fileName, "wb") as csvFile:
        csvWriter = csv.writer(csvFile)
        for data in dataList:
            csvWriter.writerow(data)
        csvFile.close()

def read_csv(csv_name):
        print ('read_csv')
        # python2.7
        csvfile = file('../formulaData/%s' % csv_name, 'rb')
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
        for col in row:
            if i==col_index:
                content.append(col)
            i+=1
        i=0
    # 查看取出的data end
    write_list_in_csv(write_csv_name, content)

if __name__ == '__main__':
    print ('excel or csv 数据读写进行....')

   #step 1
    #读取excel某张表存放在一个csv里 start
    # excel_name='TCMdata.xls'
    # sheet_index=0     # 配伍功效{4:祛风解表；5：胜湿止痛；6：透疹；胜湿止痛；7：止痉；8：散肝舒脾；9：明目}
    # csv_name='zongfang.csv'
    # exceltocsv(excel_name, sheet_index, csv_name)
    # 读取excel某张表存放在一个csv里 end

    # step 2
    #读csv的某列出来单独放在另一个csv里 start
    # read_csv_name='zongfang.csv'
    # # write_csv_name = 'prescription.csv' #配伍
    # write_csv_name = 'indications.csv' #主治
    # col_index = 10  # 要提取是csv中的那一列属性内容
    # extract_ingredients(read_csv_name, write_csv_name,col_index)
    # #读csv的某列出来单独放在另一个csv里  end

