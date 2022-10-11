# -*- coding: utf-8 -*- 
# @Time : 2022/10/8 11:39 
# @Author : zhangqinming
# @File : calling_algorithm.py

import numpy as np
import pandas as pd
import random

from numpy import ndarray
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler


class CallingAlgorithm:
    def __init__(self):
        n_neighbors = random.randint(5, 8)
        self.knn = KNeighborsClassifier(n_neighbors)
        self.scale = MinMaxScaler()

    def get_calling_scheme(self, data: list[list[pd.DataFrame]]) -> (list[ndarray], float):
        """
        输出点名方案
        """
        flag = -1
        time = 1
        calling_scheme = []
        hit_num = 0  # 点名命中次数
        request_num = 0  # 请求次数（点名次数）
        # processing
        new_data = self.data_processing(data, concat=False)

        for course_data in new_data:
            # 记录课程号
            course_id = course_data["course_id"][0]
            if course_id != flag:
                time = 1
                flag = course_id

            # knn生成一部分点名名单
            x, y = self.split_x_y(course_data)
            x = self.scale.transform(x)
            result = self.knn.predict(x)
            request_num += 90 - sum(result)  # 统计请求次数(点名次数)
            ids: np.ndarray = result.argsort()[:90 - sum(result)]  # 获取被点名学生的id

            # 如果前面刚好一次都没点就随机抽点一个
            if len(ids) == 0:
                ids = np.append(ids, random.randint(0, 89))
                request_num += 1
            this_hit_num = (y[ids] == 0).sum()
            hit_num += this_hit_num  # 统计点名命中率
            student_status = []
            # student_status = y[ids]
            calling_scheme.append(ids)
            print("course{0}, time:{1} \ncall_students:{2} \nhit_num:{3}\n".
                  format(course_id, time, ids, this_hit_num))
            time += 1
        score = hit_num / request_num  # 统计得分
        print("all_request:{0}\nall_hit:{1}\nalgorithm score:{2}".format(request_num, hit_num, score))

        return calling_scheme, score

    def fit(self, data):
        new_data = self.data_processing(data, concat=True)
        x, y = self.split_x_y(new_data)
        x = self.scale.fit_transform(x)
        self.knn.fit(x, y)

    # 输入数据处理模块
    def data_processing(self, courses_records: list[list[pd.DataFrame]], concat: bool) -> pd.DataFrame | list[
        list[pd.DataFrame]]:
        course_records_statistics = get_course_statistics(courses_records)
        courses_records_statistics = get_courses_statistics(course_records_statistics)

        data_list = []
        for i in range(len(courses_records)):
            for course_records in courses_records[i]:
                data = course_records.copy()
                # data.drop("course_id", axis=1)  # 去掉课程号
                # 为训练数据添加特征
                data[course_records_statistics[i].columns[3:]] = \
                    course_records_statistics[i].iloc[:, 3:]  # 每条数据增加该课程的出勤统计数据

                data[courses_records_statistics.columns[2:]] = \
                    courses_records_statistics.iloc[:, 2:]  # 每条数据增加该生所有课程的出勤统计数据

                data_list.append(data)
        new_data = data_list
        if concat:
            new_data = pd.concat(data_list)  # 纵向连接所有数据
        return new_data

    def split_x_y(self, data: pd.DataFrame):
        df = data.copy()
        y = df["come"]
        x = df.drop(["course_id", "come"], axis=1)
        return x, y


# get algorithm
def get_algorithm(courses_records: list[list[pd.DataFrame]]) -> CallingAlgorithm:
    """
    Parameters:
    -----------
    courses_records:五门课程的全部人员到勤信息(id, course_id, avg_grade_point, come)

    Returns:
    --------
    calling_algorithm:点名算法
    """
    calling_algorithm = CallingAlgorithm()
    calling_algorithm.fit(courses_records)
    return calling_algorithm


def get_course_statistics(courses_records) -> list[pd.DataFrame]:
    """
    统计每门课每位同学的总出勤信息(总出勤次数，总出勤率[总出勤率均值，总出勤率标准差])

    :Parameters
    -----------
    mean:bool,是否需要统计课程的平均出勤率
    std:bool,是否需要统计课程出勤率的标准差
    :Returns
    course_records_statistics:课程总的出勤信息
    """
    course_records_statistics = []
    for course_records in courses_records:
        # 初始化新表
        df = course_records[0][["id", "course_id"]].copy()
        df["course_comes"] = 0
        sum_ = 0

        # 统计出勤率
        for course_record in course_records:
            sum_ += 1
            df["course_comes"] += course_record["come"]  # 统计出勤次数
        df["course_come_rate"] = df["course_comes"] / sum_
        course_records_statistics.append(df)
    return course_records_statistics


def get_courses_statistics(course_records_statistics):
    """
    统计每位同学所有课程总的出勤信息(总出勤次数，总出勤率[总出勤率均值，总出勤率标准差])
    :Parameters
    -----------
    mean:是否统计均值
    std：是否统计标准差
    :Returns
    courses_records_statistics:所有课程总的出勤信息
    -----
    """
    # 初始化新表
    courses_records_statistics = course_records_statistics[0].copy()
    courses_records_statistics["courses_comes"] = 0
    for i in course_records_statistics:
        courses_records_statistics["courses_comes"] += i["course_comes"]  # 统计所有课程的出勤次数
    courses_records_statistics = courses_records_statistics[["id", "courses_comes"]]  # 取子表
    courses_records_statistics["courses_comes_rate"] = courses_records_statistics[
                                                           "courses_comes"] / (
                                                           90)  # 统计所有课程的出勤率
    return courses_records_statistics
