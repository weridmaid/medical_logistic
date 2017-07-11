# coding:utf-8
import excelprocess
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from sklearn.feature_extraction import DictVectorizer
from sklearn import metrics
from sklearn.metrics import (accuracy_score,precision_score,recall_score,f1_score)
from sklearn import cross_validation
from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np
from numpy import random

def readmydata():
  print ('readmydata')
  # readcsvnamex = 'prescriptionFeature.csv'
  # readcsvnamey = 'labelFeature.csv'

  readcsvnamex = 'prescriptionFeature4.csv'
  readcsvnamey = 'labelFeature.csv'

  x_data = excelprocess.read_csv(readcsvnamex)
  y_data = excelprocess.read_csv(readcsvnamey)

  X=[]
  Y=[]

  for item in x_data:
    xx=[]
    for itemdata in item:
      itemdata = itemdata.replace('﻿', '')
      xx.append(float(itemdata))
    X.append(xx)

  for item in y_data:
    yy=[]
    for itemdata in item:
      itemdata = itemdata.replace('﻿', '')
      yy.append(float(itemdata))
    Y.append(yy)

  print ('X.lenth:',len(X))
  print ('Y.lenth:',len(Y))

  return X,Y


def multiclassSVM():
  print ('multiclassSVM')
  X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, Y, test_size=0.2,random_state=0)

  print ('X_train',X_train)
  print ('y_train', y_train)
  print ('X_test',X_test)
  print ('y_test',y_test)

  model = OneVsRestClassifier(SVC())

  model.fit(X_train, y_train)

  predicted = model.predict(X_test)
  print ('predicted',predicted)



#多标签分类必须把label二值化
def multilabelSVM(X,Y):
  print ('multilabelSVM')
  Y_enc = MultiLabelBinarizer().fit_transform(Y)
  print ('Y_enc:',Y_enc[:5])
  # X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X, Y_enc, test_size=0.2, random_state=0)

  X_train, X_test, Y_train, Y_test = train_test_split(X, Y_enc, test_size=0.1)



  print ('X_train',X_train[:5])
  print ('Y_train', Y_train[:5])
  print ('X_test',X_test[:5])
  print ('Y_test',Y_test[:5])
  print ('Y_test.lenth', len(Y_test))

  # model = OneVsRestClassifier(SVC())
  model = OneVsRestClassifier(LinearSVC(random_state=0))

  # model.decision_function_shape = "ovr"
  # ovo为一对一
  # model.decision_function_shape = "ovo"

  model.fit(X_train, Y_train)
  Y_predicted = model.predict(X_test)

  print (' Y_predicted',  Y_predicted[:5])
  print ('Y_predicted.lenth', len(Y_predicted))

  print  ('precision_macro:',precision_score(Y_test, Y_predicted, average='macro'))
  print ('precision_micro:', precision_score(Y_test, Y_predicted, average='micro'))
  print ('precision_weighted:', precision_score(Y_test, Y_predicted, average='weighted'))

  print  ('precision_sample:', precision_score(Y_test, Y_predicted, average='samples'))
  print  ('recall:', recall_score(Y_test, Y_predicted, average='samples'))
  print  ('F1:', f1_score(Y_test, Y_predicted, average='samples'))

  print("\tPrecision: %1.3f" % precision_score(Y_test, Y_predicted))
  print("\tRecall: %1.3f" % recall_score(Y_test, Y_predicted))
  print("\tF1: %1.3f\n" % f1_score(Y_test, Y_predicted))

  # writecsvname = 'Y_predicted_normal.csv'
  # excelprocess.write_in_csv(writecsvname , Y_predicted)
  #
  # writecsvname = 'Y_test_normal.csv'
  # excelprocess.write_in_csv(writecsvname , Y_test)


if __name__ == '__main__':
    print ('tcm_analysis.py  main')

    # multiclassSVM()
    X,Y=readmydata()
    multilabelSVM(X,Y)



