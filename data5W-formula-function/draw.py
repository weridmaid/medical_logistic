# coding=utf-8
import data_process

readcsvname = '../formulaData_Experiment/ExResult_onehot_QRJD.csv'
readdata = data_process.read_csv(readcsvname)
datalist=[]
data=[]
for item in readdata:
    print 'item',item[0]
    num=0
    for i in item[0].split(' '):
        print '1',i
        if(num==3):
            print '2',i
            print i.split('：')[-1]
            maxiter=i.split('：')[-1]
            data.append(float(maxiter))

        num+=1
    acc=item[1].split('acc:')[-1]
    acc=acc.replace('"','')
    print acc
    data.append(float(acc))
    datalist.append(data)
    data=[]

writecsvname = '../formulaData_1/L1_draw.csv'
medicaldata = data_process.write_in_csv(writecsvname,datalist)