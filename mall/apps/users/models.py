from django.db import models
from django.contrib.auth.models import AbstractUser
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData
from django.conf import settings
# Create your models here.
# 通过继承系统的数据库模型,构建自己的数据库模型


class User(AbstractUser):

    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def generic_email_url(self, email):

        serializer = Serializer(settings.SECRET_KEY, 3600)

        tokrn = serializer.dumps({
            'email':email,
            'id':self.id
        })

        return 'http://www.meiduo.site:8080/success_verify_email.html?token=' + tokrn.decode()

    @staticmethod
    def check_verify_token(token):
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            result = serializer.loads(token)
        except BadData:
            return None
        else:
            id = result.get('id')
            email = result.get('email')
            try:
                user = User.objects.get(id=id)
            except User.DoseNotExist:
                return None

        return user


