# -*- coding: utf-8 -*- 
# @Time : 2022/10/11 8:03 
# @Author : zhangqinming
# @File : draw.py

import matplotlib.pyplot as plt
from attendance_table import AttendanceTableBuilder
from calling_algorithm import get_algorithm
import warnings

# 忽略警告
warnings.filterwarnings("ignore")


def algorithm_score(algorithm, test_table_builder):
    # 生成测试数据
    test_table_builder.build_tables()
    test_courses_records = test_table_builder.get_courses_records()
    test_table_builder.save_in_local()
    # 输出点名名单
    calling_scheme, score = algorithm.get_calling_scheme(test_courses_records)
    return score


if __name__ == '__main__':
    # 生成数据
    train_table_builder = AttendanceTableBuilder(5, 20, 90)
    train_table_builder.build_tables()
    train_courses_records = train_table_builder.get_courses_records()

    # 生成算法
    algorithm = get_algorithm(train_courses_records)

    times = list(range(10))
    scores = []
    for i in range(10):
        scores.append(algorithm_score(algorithm, train_table_builder))

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure()
    plt.plot(times, scores, '--', c='g', marker='+')
    plt.xticks(times)
    plt.xlabel("times")
    plt.ylabel("score")
    plt.title("算法稳定性测试")
    plt.savefig("算法稳定性测试.jpg")
    plt.show()