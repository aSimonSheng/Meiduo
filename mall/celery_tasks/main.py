# -*-coding:utf-8-*-
# 创建一个celery实例对象

from celery import Celery

app = Celery(main='celeary_tasks')
