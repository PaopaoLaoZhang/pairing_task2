# CallAlgorithm

软件工程第二次结队作业

- [CallAlgorithm](#CallAlgorithm)
  - [环境要求](##环境要求)
  - [快速开始](##快速开始)

## 环境要求

see:[环境依赖](./requirements.txt)

**导入依赖：**

命令行输入:`pip install -r requirements.txt`

## 快速开始

可以参考：[exp_demo.py](./main/python/exp_demo.py)

- 生成出勤记录

```python
from AttendanceTableBuilder import AttendanceTableBuilder

# 初始化构建器
test_table_builder = AttendanceTableBuilder(5, 20, 90) 

# 随机生成记录
courses_records = test_table_builder.build_tables()

# 获取生成出勤记录
courses_records = test_table_builder.get_courses_records()

# 导出出勤记录
test_table_builder.save_in_local() #save data in path: '../dat'
```

- 获取算法

```python
from calling_algorithm import get_algorithm
# 生成算法
# put the courses_records generated by AttendanceTableBuilder
algorithm = get_algorithm(courses_records) 
```

- 模拟点名

```python
# 模拟点名
# put the courses_records generated by AttendanceTableBuilder then get the calling_scheme
calling_scheme = algorithm.get_calling_scheme(courses_records)
print(calling_scheme)
```

