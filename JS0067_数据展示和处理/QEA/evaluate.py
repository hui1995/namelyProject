from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

def evaluate_P(P,instance,tab,number,population,m):
    Pf = []
    delete = []
    n = 0 #选择的特征数
    new_instance = instance.copy()
    for i in range(population):
        for j in range(m):
            if P[i][j] == 0:
                delete.append(j)
            else:
                n = n + 1

        if n == 0:
            Pf.append(0)
            delete.clear()
        else:
            for k in range(number):
                new_instance[k] = [new_instance[k][g] for g in range(len(new_instance[k])) if g not in delete]
            #print(new_instance)
            #划分训练集和测试集
            X_train, X_test, y_train, y_test = train_test_split(new_instance, tab, test_size=0.4, random_state=0)
            clf = svm.SVC(gamma='scale', decision_function_shape='ovo').fit(X_train, y_train)
            #分类精度
            s = clf.score(X_test, y_test)
            #基于svm分类法的适应度函数
            j = s ** (1 + n ** 0.5)
            Pf.append(j)
            # print(Pf)
            # print(n)
            n = 0
            delete.clear()
            new_instance = instance.copy()

    return Pf