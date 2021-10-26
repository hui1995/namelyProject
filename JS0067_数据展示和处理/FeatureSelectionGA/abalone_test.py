# coding=gbk
import pandas as pd
import numpy as np
from FeatureSelectionGA.featureselection_ga import FeatureSelectionGA
from FeatureSelectionGA.SVM_acc import calculate_acc
def main(info):
    # abalone.data  0.2ʱ���ྫ�ȸ�һ��  �ܵ���˵����
    df = pd.read_csv(info)
    df = df.values
    sex = df[:, 0]
    for s in range(len(sex)):
        if df[s][0] == 'M':
            df[s][0] = 0
        elif df[s][0] == 'F':
            df[s][0] = 1
        else:
            df[s][0] = 2
    X = df[:, :-1]
    y = df[:, -1]

    fsga = FeatureSelectionGA(X, y)
    pop = fsga.generate(100, 0.25, 0.1, 10)

    #  ����ѡ���������ķ��ྫ��
    np_ind = np.asarray(pop)
    feature_idx = np.where(np_ind == 1)[0]
    features = X[:, feature_idx]
    labels = y.astype('int')

    #print(y, type(labels))
    acc_score = calculate_acc(features, labels)

    n = 0
    for i in range(len(pop)):
         if(pop[i]==1):
             n = n + 1
    result=[]
    result.append("������:{}".format( len(pop)))
    result.append("����ѡ�����Ž�:{}".format(pop))
    result.append("��ѡ��������:{}}".format(n))
    result.append("���ྫ��:{}".format(acc_score))
    return result
