from sklearn import svm
import numpy as np
X = np.array([[0, 0], [1, 1]])
y = np.array([0, 1])
clf = svm.SVC(gamma='scale')
clf.fit(X, y)