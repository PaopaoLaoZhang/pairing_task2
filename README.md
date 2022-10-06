# CallAlgorithm

软件工程第二次结队作业

- [CallAlgorithm](#CallAlgorithm)

  - [项目结构](##项目结构)

  - [环境要求](##环境要求)

  - [快速开始](##快速开始)

  - [API](##API)

## 项目结构

```
:.
│  list.txt
│  README.md
│  
└─main
    │          
    └─python
        │  AttendanceTableBuilder.py
        │  main.py
        │  ModelSelect.py
        │  TestDemo.py
```

## 环境要求

see:[环境依赖](./requirements.txt)

**导入依赖：**

命令行输入:`pip install -r requirements.txt`

## 快速开始

可以参考：[TestDemo.py](./main/python/TestDemo.py)

- 生成出勤记录

```python
from AttendanceTableBuilder import AttendanceTableBuilder

# 初始化构建器
test_table_builder = AttendanceTableBuilder.get_test_table_builder()
# 获取出勤记录
courses_records = test_table_builder.get_courses_records()
```

- 训练算法

```python
from sklearn.neighbors import KNeighborsClassifier
from ModelSelect import *

# 获取训练数据和测试数据
train_data, test_datas = test_table_builder.get_train_data() 
train_x, trian_y = split_x_y(train_data)
KNN = KNeighborsClassifier(n_neighbors=5)
KNN.fit(train_x, trian_y)

# 测试E值
score = get_score(test_datas,KNN)
print(score)
```

## API

没有做，就先看注释吧