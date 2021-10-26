# coding=gbk
import numpy as np


class FitnessFunction:
    def entropy(self, c):
        """
        entropy calculation

        :param c:

        :return:
        """
        c_normalized = c / float(np.sum(c))
        # 返回矩阵中的非0值
        c_normalized = c_normalized[np.nonzero(c_normalized)]
        H = -sum(c_normalized * np.log2(c_normalized))
        return H

    def feature_label_MIs(self, arr, y):
        """
        calculate feature-label mutual information
        互信息I(X;Y)可以等价的写为：
        I(X;Y)=H(X)+H(Y)-H(X,Y)

        :param arr: features_values

        :param y: features_label

        :return:
        """
        m, n = arr.shape  # 150, 4
        MIs = []
        # 表示分区后每个区间内有多少个元素
        p_y = np.histogram(y)[0]
        # p_y, uu = np.histogram(y)
        # print(p_y,uu)
        h_y = self.entropy(p_y)  # H(Y)
        # print("h_y:", h_y)

        for i in range(n):
            # p_i = np.histogram(arr[:, i])[0]
            p_i, uu = np.histogram(arr[:, i])
            # print(p_i,uu)
            p_iy = np.histogram2d(arr[:, 0], y)[0]
            # p_iy, uu, ii = np.histogram2d(arr[:, 0], y)
            # print(p_iy, uu, ii)
            h_i = self.entropy(p_i)
            h_iy = self.entropy(p_iy)

            MI = h_i + h_y - h_iy
            MIs.append(MI)
        MIs = np.array(MIs)
        mi = MIs.mean()
        return mi

    def feature_feature_MIs(self, x, y):
        """
        calculate feature-feature mutual information
        互信息I(X;Y)可以等价的写为：
        I(X;Y)=H(X)+H(Y)-H(X,Y)

        :param x:

        :param y:

        :return:
        """
        p_x = np.histogram(x)[0]
        p_y = np.histogram(y)[0]
        p_xy = np.histogram2d(x, y)[0]

        h_x = self.entropy(p_x)
        h_y = self.entropy(p_y)
        h_xy = self.entropy(p_xy)
        return h_x + h_y - h_xy

    def calculate_fitness(self, x, y):
        score = 0
        m, n = x.shape
        ff_mis = []
        mi = self.feature_label_MIs(x, y)  # 特征与标签的相关性

        # 计算特征与类的相关性
        if n == 1:
            FF_mis = 0
        else:
            for i in range(0, n - 1):
                for j in range(i + 1, n):
                    ff_mi = self.feature_feature_MIs(x[:, i], x[:, j])
                    ff_mis.append(ff_mi)
            ff_mis = np.array(ff_mis)
            FF_mis = ff_mis.std()
        score = mi - FF_mis
        return score
