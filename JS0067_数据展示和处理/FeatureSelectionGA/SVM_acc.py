# coding=gbk
import time
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import svm


#  估算选择后的特征的分类精度

def calculate_acc(features, labels):
    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.33, random_state=0)
    time_2 = time.time()
    print('Start training...')
    clf = svm.SVC()
    clf.fit(train_features, train_labels)
    time_3 = time.time()
    print("training cost %f seconds" % (time_3 - time_2))

    print('Starting predicting...')
    test_predict = clf.predict(test_features)
    time_4 = time.time()
    print("predicting cost %f seconds" % (time_4 - time_3))

    acc_score = accuracy_score(test_labels, test_predict)
    return acc_score



