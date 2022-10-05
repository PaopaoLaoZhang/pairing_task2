# -*- coding: utf-8 -*- 
# @Time : 2022/10/4 20:07 
# @Author : zhangqinming
# @File : TestDemo.py

from AttendanceTableBuilder import AttendanceTableBuilder
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from ModelSelect import *
import warnings

# 镇压警告
warnings.filterwarnings("ignore")
if __name__ == '__main__':
    test_table_builder = AttendanceTableBuilder.get_test_table_builder()

    train_data, test_data_list = test_table_builder.get_train_data()  # 获取训练数据
    train_x, train_y = split_x_y(train_data)
    # 初始化模型
    # 逻辑回归
    LR = LogisticRegression(random_state=0, max_iter=5000)
    # KNN
    KNN = KNeighborsClassifier(n_neighbors=5)
    # 高斯贝叶斯
    GNB = GaussianNB()
    # 随机森林
    RFC = RandomForestClassifier()
    models = [LR, KNN, GNB, RFC]

    # 训练并显示各模型拟合数据的准确率
    show_model_acc(models, train_data)

    # 选择模型
    best_model = model_select(models, test_data_list)
    score = get_score(test_data_list, best_model)
    print(score)
