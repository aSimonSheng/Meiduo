from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
# 通过继承系统的数据库模型,构建自己的数据库模型


class User(AbstractUser):

    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name