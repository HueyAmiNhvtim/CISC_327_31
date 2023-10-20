# Django

## 一、创建工程项目

> cd进入要创建项目的文件夹，运行命令：django-admin startproject 项目名

## 二、创建应用

```python
python manage.py startapp db
```

## 三、创建数据库表

```python
# 在models.py中建类，类名即表名
python manage.py migrate
```

## 四、创建超级管理员

```python
# 以便使用django自带的admin管理页http://127.0.0.1:8000/admin
python manage.py createsuperuser

# 同时要将创建的数据表注册到dbapi应用下的admin.py中
from dbapi import models
admin.site.register(models.UserInfo)
```

## 五、运行django服务

首先需将app添加到setting.py的INSTALLED_APPS中

```python
python manage.py runserver
```
