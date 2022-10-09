# -*- coding: utf-8 -*-
# @Time : 2022/10/8 21:48 
# @Author : zhangqinming
# @File : exp_demo.py

from AttendanceTableBuilder import AttendanceTableBuilder
from calling_algorithm import get_algorithm
import warnings

# 忽略警告
warnings.filterwarnings("ignore")
if __name__ == '__main__':
    # 生成数据
    train_table_builder = AttendanceTableBuilder(5, 20, 90)
    train_table_builder.build_tables()
    train_courses_records = train_table_builder.get_courses_records()
    df = train_courses_records[0][0]
    come_cnt = df["come"].sum()

    # 生成算法
    algorithm = get_algorithm(train_courses_records)

    # 生成测试数据
    test_table_builder = AttendanceTableBuilder(5, 20, 90)
    test_table_builder.build_tables()
    test_courses_records = test_table_builder.get_courses_records()
    test_table_builder.save_in_local()
    # 输出点名名单
    calling_scheme = algorithm.get_calling_scheme(test_courses_records)
