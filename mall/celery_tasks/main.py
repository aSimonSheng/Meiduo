# -*-coding:utf-8-*-
# 创建一个celery实例对象
# 通过celery配置文件,设置broker
# 需要让selery自动检测任务
# worker执行 在虚拟环境中 通过指令 等待broker 分配任务

#进行Celery允许配置
# 为celery使用django配置文件进行设置
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mall.settings'



from celery import Celery

app = Celery(main='celeary_tasks')
# 文件路径
app.config_from_object('celery_tasks.config')

# 自动检测
# 参数[]
# 每一项 就是队形celery_tasks,sms
app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.email'])


# celery -A 脚本路径.celery实例锁对应的文件  work -l info
# celery -A celery_tasks.main worker -l info
