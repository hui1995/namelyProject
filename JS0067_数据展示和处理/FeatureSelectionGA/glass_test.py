# coding=gbk
import pandas as pd
import numpy as np
from FeatureSelectionGA.featureselection_ga import FeatureSelectionGA
from FeatureSelectionGA.SVM_acc import calculate_acc
def main(info):
    # abalone.data  0.2时分类精度高一点  总的来说不高
    df = pd.read_csv(info)
    # glass.data  0.2
    df = pd.read_csv(r'C:\Users\dell\Desktop\dataset\glass.data')
    df = df.values
    X = df[:, 1:-1]
    y = df[:, -1]

    fsga = FeatureSelectionGA(X, y)
    pop = fsga.generate(100, 0.5, 0.5, 100)

    #  估算选择后的特征的分类精度
    np_ind = np.asarray(pop)
    feature_idx = np.where(np_ind == 1)[0]
    features = X[:, feature_idx]
    labels = y
    acc_score = calculate_acc(features, labels)

    n = 0
    for i in range(len(pop)):
         if(pop[i]==1):
             n = n + 1
    result = []
    result.append("特征数:{}".format(len(pop)))
    result.append("特征选择最优解:{}".format(pop))
    result.append("已选择特征数:{}}".format(n))
    result.append("分类精度:{}".format(acc_score))
    return result
