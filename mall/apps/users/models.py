from django.db import models
from django.contrib.auth.models import AbstractUser
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData
from django.conf import settings
# Create your models here.
# 通过继承系统的数据库模型,构建自己的数据库模型
from utils.models import BaseModel


class User(AbstractUser):

    mobile = models.CharField(max_length=11,
                              unique=True,
                              verbose_name='手机号')
    # 将默认地址放在user中,相对于放在用户地址中,不会浪费资源
    # 节省空间
    default_address = models.ForeignKey('Address',
                                        related_name='users',
                                        null=True, blank=True,
                                        on_delete=models.SET_NULL,
                                        verbose_name='默认地址')
    email_active = models.BooleanField(default=False,
                                       verbose_name='邮箱验证状态')


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

class Address(BaseModel):
    """
    用户地址
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    title = models.CharField(max_length=20, verbose_name='地址名称')
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    #### 这里的外键,当用到是,只接通过应用.模型  可以找到相对应的模型
    province = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='province_addresses', verbose_name='省')
    city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='city_addresses', verbose_name='市')
    district = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='district_addresses', verbose_name='区')
    place = models.CharField(max_length=50, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    tel = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='固定电话')
    email = models.CharField(max_length=30, null=True, blank=True, default='', verbose_name='电子邮箱')
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']
