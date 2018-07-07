# -*-coding:utf-8-*-
from libs.yuntongxun.sms import CCP

from celery_tasks.main import app
# 定义任务
# 注意装饰器是task
# name 级是任务执行的名字

@app.task(name='send_code')
def send_sms_code(mobile, sms_code):
    ccp = CCP()

    ccp.send_template_sms(mobile, [sms_code, 5], 1)
