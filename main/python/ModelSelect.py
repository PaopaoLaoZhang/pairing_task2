# -*- coding: utf-8 -*- 
# @Time : 2022/10/4 20:08 
# @Author : zhangqinming
# @File : ModelSelect.py
from sklearn.metrics import accuracy_score as acc




def get_score(test_datas, algorithm):
    """
    结队作业算法评估标准E，测试数据使用的是生成的五门课共100次的点名记录。
    :Parameters
    -----------
    test_datas:五门课共100次的点名记录数据,数据的维度要和算法要求的维度一致。
    algorithm:点名算法。
    :Returns
    --------
    score:评估得分。
    """
    hit_num = 0  # 点名命中次数
    request_num = 0  # 请求次数（点名次数）
    for record in test_datas:
        record_label = record["come"]  # train_y
        record = record.drop("come", axis=1)  # train_X
        result = algorithm.predict(record)  # predict_y
        request_num += 90 - sum(result)  # 统计请求次数(点名次数)
        ids = result.argsort()[:90 - sum(result)]  # 获取被点名学生的id
        hit_num += (record_label[ids] == result[ids]).sum()  # 统计点名命中率
    # print("hit_num:{} \n request_num:{}".format(hit_num, request_num))
    score = hit_num / request_num  # 统计得分
    # print(score)
    return score


def model_select(models, test_data):
    """
    测试算法性能，比较依据为结队作业算法评估标准E,测试数据使用的是生成的五门课共100次的点名记录。
    :Parameters
    -----------
    test_data:五门课共100次的点名记录数据,数据的维度要和算法要求的维度一致。
    model:点名算法。
    :Returns
    --------
    best_model:最适合的模型
    """
    min_score = 0
    best_model = None
    for model in models:
        model_score = get_score(test_data, model)
        if model_score > min_score:
            min_score = model_score
            best_model = model
    return best_model


def show_model_acc(models, train_data):
    """
    可视化各模型在训练集上的准确率，训练和测试都使用train_data
    :Parameters
    -----------
    test_data:五门课共100次的点名记录数据,数据的维度要和算法要求的维度一致。
    model:点名算法。
    :Returns
    --------
    print accuracy rate of every model
    """
    train_y = train_data["come"]  # train_y
    train_x = train_data.drop("come", axis=1)  # train_X
    for model in models:
        model.fit(train_x, train_y)
        predict_y = model.predict(train_x)
        print("acc of model:", acc(train_y, predict_y))
