# coding=utf-8
import data_process
from numpy import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def loadDataSet(funcCsvname,presCsvname):
    dataMat = []; labelMat = []
    funcdata = data_process.read_csv(presCsvname)
    labeldata=data_process.read_csv(funcCsvname)
    for i in funcdata:
        dataMat.append(i)
    for j in labeldata:
        labelMat.append(j)

    return dataMat,labelMat

def sigmoid(inX):
    return 1.0/(1+exp(-inX))

if __name__ == '__main__':
    print ('正在训练logistic模型中....')
    funcCsvname='funcFeature.csv'
    presCsvname='presFeature_realValue.csv'
