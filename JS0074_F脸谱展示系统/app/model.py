# import torch
# from torch import nn
# from torch.nn import functional as F
#
#
#
# #定义lenet5
# class LeNet5(nn.Module):
#     def __init__(self):
#         '''构造函数，定义网络的结构'''
#         super().__init__()
#         #定义卷积层，1个输入通道，6个输出通道，5*5的卷积filter，外层补上了两圈0,因为输入的是32*32
#         self.conv1 = nn.Conv2d(3, 6, 5, padding=2)
#         #第二个卷积层，6个输入，16个输出，5*5的卷积filter
#
#         self.conv2 = nn.Conv2d(6, 16, 5)
#
#         #最后是三个全连接层
#         self.fc1 = nn.Linear(16*6*6, 120)
#         self.fc2 = nn.Linear(120, 84)
#         self.fc3 = nn.Linear(84, 6)
#
#     def forward(self, x):
#         '''前向传播函数'''
#         #先卷积，然后调用relu激活函数，再最大值池化操作
#        # 6 x 16 x16
#         x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
#         #第二次卷积+池化操作,16 x 6 x 6
#         x = F.max_pool2d(F.relu(self.conv2(x)), (2, 2))
#         #重新塑形,将多维数据重新塑造为二维数据，256*400
#         x = x.view(-1, self.num_flat_features(x))#在pytorch中view函数的作用为重构张量的维度，当view(-1)时，其作用是将一个矩阵展开为一个向量
#         # print('size', x.size())
#         #第一个全连接
#         x = F.relu(self.fc1(x))
#         x = F.relu(self.fc2(x))
#         x = self.fc3(x)
#         return x
#
#     def num_flat_features(self, x):
#         #x.size()返回值为(256, 16, 5, 5)，size的值为(16, 5, 5)，256是batch_size
#         size = x.size()[1:]  #x.size返回的是一个元组，size表示截取元组中第二个开始的数字
#         num_features = 1#size的第一个纬度是该批次样本的个数，其余的纬度相乘为特征数
#         for s in size:
#             num_features *= s
#
#         return num_features
