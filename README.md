# CallAlgorithm

软件工程第二次结队作业

## 项目结构

:.
│  list.txt
│  README.md
│  
└─main
    ├─.idea
    │  │  .gitignore
    │  │  main.iml
    │  │  misc.xml
    │  │  modules.xml
    │  │  vcs.xml
    │  │  workspace.xml
    │  │  
    │  └─inspectionProfiles
    │          profiles_settings.xml
    │          Project_Default.xml
    │          
    └─python
        │  AttendanceTableBuilder.py
        │  main.py
        │  ModelSelect.py
        │  TestDemo.py
        │  
        ├─.idea
        │  │  .gitignore
        │  │  misc.xml
        │  │  modules.xml
        │  │  team_work.iml
        │  │  vcs.xml
        │  │  workspace.xml
        │  │  
        │  └─inspectionProfiles
        │          profiles_settings.xml
        │          
        └─__pycache__
                AttendanceTableBuilder.cpython-310.pyc
                ModelSelect.cpython-310.pyc

## 环境要求

- python3

- pandas

- random

- sklearn

如果环境中缺少某个python软件包，可以使用`pip`或`conda`命令安装。

例如：`pip install pandas`

​          `conda install pandas`

## 快速开始

可以参考：[TestDemo.py](main\python\TestDemo.py)

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