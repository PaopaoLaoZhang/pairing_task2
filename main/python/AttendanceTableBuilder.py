# -*- coding: utf-8 -*- 
# @Time : 2022/10/3 20:09 
# @Author : zhangqinming
# @File : AttendanceTableBuilder.py
import random
import pandas as pd
import numpy as np


def get_random_sample(sample_list, a, b):
    """
    在指定样本集合中随机选出[a,b]个样本点

    :Parameters
    -----------
    sample_list:指定的集合


    :Returns
    --------
    rand_samples:随机选出的样本数据
    """
    rand_num = random.randint(a, b)  # 在[a,b]内随机生成一个数
    rand_samples = random.sample(sorted(sample_list), rand_num)  # 从样本集合中选出随机的样本点
    return rand_samples


def scale(data, a, b):
    """
    将数据归一化到区间[a,b]
    :Parameters
    -----------
    data:数据
    a:区间左端
    b:区间右端

    :Returns
    --------
    new_data:归一化后的数据
    """
    max_value = max(data)
    min_value = min(data)
    k = (b - a) / (max_value - min_value)
    new_data = (data - min_value) * k + a
    return new_data


class AttendanceTableBuilder:

    def __init__(self, n_courses, n_time, n_members):
        """
        初始化类
        :Parameters
        -----------
        n_courses：课程数
        n_time:每门课程的课时
        n_members:课程成员人数
        random_state:随机数种子，默认为不固定
        """
        self.courses_records_statistics = None
        self.course_records_statistics = None
        self.courses_records = None
        self.n_courses = n_courses
        self.n_time = n_time
        self.n_members = n_members

    @staticmethod
    def get_test_table_builder():
        test_table_builder = AttendanceTableBuilder(5, 20, 90)
        return test_table_builder

    def get_courses_records(self) -> list[list[pd.DataFrame]]:
        """
        获取所有课程的点名记录
        Returns
        -------
        courses_records:所有课程的点名记录
        """
        if self.courses_records is None:
            self.build_tables()
        return self.courses_records

    def grade_point_generate(self) -> np.ndarray:
        a = np.random.randn(self.n_members)
        grade_points = scale(a, 1, 4)
        return grade_points

    def save_in_local(self):
        """
        将点名记录保存为csv文件
        """

        course_id = -1
        for course_data in self.courses_records:
            course_id += 1
            time = 0
            for time_data in course_data:
                time += 1
                time_data.to_csv(r"../data/course{}_time{}_records.csv".format(course_id, time))

    # 随机生成学生到勤信息
    def build_tables(self):
        """
        随机生成课程到勤信息，即每节课一张表，每张表的表头为学生的序号(id),课程id(course_id),到勤信息(come)
        先生成经常没到的同学的id，然后随机指定其每门课的未到的课。

        :Returns
        --------
        """
        if self.courses_records is not None:
            return
        feature_name = ["id", "course_id", "come"]
        ids = list(range(self.n_members))
        course_ids = list(range(self.n_courses))
        periods = list(range(self.n_time))

        # 生成每位同学的平均绩点
        avg_grade_points = self.grade_point_generate()
        # 选择范围[1,2.5]的绩点，随机挑选出几个赋给经常爱逃课的同学
        where_res = np.where(avg_grade_points <= 2.5)[0]

        # 生成DataFrame
        self.courses_records = []  # 初始化每门课的点名列表
        for course_id in course_ids:
            course_records = []  # 初始化每次课点名的列表
            cnt = 0  # 计数器，记录是第几次课

            # 随机生成经常逃课的同学其未到的课程id
            # 从绩点[1,2.5]的同学中随机生成每个课程固定没到的同学名单
            no_come_members_dict = {}
            no_come_members = get_random_sample(where_res, 5, 8)  # 随机生成每门课80%课程没到的同学的id
            num_p80 = int(self.n_time * 0.8)  # 计算80%的课程次数
            for no_come_member in no_come_members:
                no_come_periods = random.sample(periods, num_p80)  # 随机生成每位固定缺勤人员的缺勤的那几节课
                no_come_members_dict[no_come_member] = no_come_periods  # 记录每个人对应的缺勤课

            # 生成除经常没到的同学之外的同学的名单
            other_ids = ids.copy()
            for no_come_member in no_come_members:
                other_ids.remove(no_come_member)

            # 生成每节课的出勤表
            for i in range(self.n_time):
                # 初始化某门课程某次课程的点名数据表
                attendance_record = pd.DataFrame(columns=feature_name)
                attendance_record["id"] = ids
                attendance_record["course_id"] = course_id
                attendance_record["avg_grade_point"] = avg_grade_points
                attendance_record["come"] = 1  # 1表示到，0表示没到

                # 为固定没到的同学出勤记录赋值缺勤
                for no_come_member in no_come_members:
                    if cnt in no_come_members_dict[no_come_member]:
                        # attendance_record["come"].loc[no_come_member] = 0  # 标记这位同学这次课没到
                        attendance_record.loc[no_come_member, "come"] = 0  # 标记这位同学这次课没到

                # 记额外的0-3名没到的同学的出勤记录
                random.seed(None)  # 减少这些同学重复的概率
                other_no_come_members = get_random_sample(other_ids, 0, 3)
                for other_no_come_member in other_no_come_members:
                    # attendance_record["come"].loc[other_no_come_member] = 0
                    attendance_record.loc[other_no_come_member, "come"] = 0
                cnt += 1
                course_records.append(attendance_record)

            self.courses_records.append(course_records)


    def get_course_statistics(self, mean=False, std=False):
        """
        统计每门课每位同学的总出勤信息(总出勤次数，总出勤率[总出勤率均值，总出勤率标准差])

        :Parameters
        -----------
        mean:bool,是否需要统计课程的平均出勤率
        std:bool,是否需要统计课程出勤率的标准差
        :Returns
        course_records_statistics:课程总的出勤信息
        """
        self.course_records_statistics = []
        for course_records in self.courses_records:
            # 初始化新表
            df = course_records[0][["id", "course_id"]].copy()
            df["course_comes"] = 0
            sum_ = 0

            # 统计出勤率
            for course_record in course_records:
                sum_ += 1
                df["course_comes"] += course_record["come"]  # 统计出勤次数
            df["course_come_rate"] = df["course_comes"] / sum_
            if mean:
                # 统计这门课的平均出勤率
                df["mean_course_come_rate"] = df.describe()["course_come_rate"]["mean"]
            if std:
                # 统计这门课出勤率的标准差
                df["std_course_come_rate"] = df.describe()["course_come_rate"]["std"]
            self.course_records_statistics.append(df)
        return self.course_records_statistics

    def get_courses_statistics(self, mean=False, std=False):
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
        courses_records_statistics = self.course_records_statistics[0].copy()
        courses_records_statistics["courses_comes"] = 0
        for i in self.course_records_statistics:
            courses_records_statistics["courses_comes"] += i["course_comes"]  # 统计所有课程的出勤次数
        courses_records_statistics = courses_records_statistics[["id", "courses_comes"]]  # 取子表
        courses_records_statistics["courses_comes_rate"] = courses_records_statistics[
                                                               "courses_comes"] / (
                                                                   self.n_courses * self.n_time)  # 统计所有课程的出勤率
        if mean:  # 计算总出勤率的均值
            courses_records_statistics["mean_courses_comes_rate"] = \
                courses_records_statistics.describe()["courses_comes_rate"]["mean"]
        if std:  # 计算总出勤率的标准差
            courses_records_statistics["std_courses_comes_rate"] = \
                courses_records_statistics.describe()["courses_comes_rate"]["std"]
        self.courses_records_statistics = courses_records_statistics
        return self.courses_records_statistics

    def get_train_data(self):
        """
        获取机器学习模型训练用的数据
        :Returns
        --------
        train_data:训练数据
        data_list:每节课的数据
        """
        data_list = []
        if self.courses_records is None:
            self.build_tables()
        for i in range(len(self.courses_records)):
            for course_records in self.courses_records[i]:
                data = course_records.copy()
                data.drop("course_id", axis=1)  # 去掉课程号
                # 为训练数据添加特征
                if self.course_records_statistics is None:
                    self.get_course_statistics()
                data[self.course_records_statistics[i].columns[3:]] = \
                    self.course_records_statistics[i].iloc[:, 3:]  # 每条数据增加该课程的出勤统计数据

                if self.courses_records_statistics is None:
                    self.get_courses_statistics()
                data[self.courses_records_statistics.columns[2:]] = \
                    self.courses_records_statistics.iloc[:, 2:]  # 每条数据增加该生所有课程的出勤统计数据

                data_list.append(data)
        train_data = pd.concat(data_list)  # 纵向连接所有数据
        return train_data, data_list
