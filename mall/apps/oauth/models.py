# Create your models here.
from django.db import models
from utils.models import BaseModel
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature
from django.conf import settings
class OAuthQQUser(BaseModel):
    """
    QQ登录用户数据
    """
    user = models.ForeignKey('users.User',
                             on_delete=models.CASCADE,
                             verbose_name='用户')
    openid = models.CharField(max_length=64,
                              verbose_name='openid',
                              db_index=True)

    class Meta:
        db_table = 'tb_oauth_qq'
        verbose_name = 'QQ登录用户数据'
        verbose_name_plural = verbose_name


    @classmethod
    def genericte_open_id_token(cls, openid):

        # 实力化 序列器
        serializer = Serializer(settings.SECRET_KEY, 3600)

        token = serializer.dumps({'openid':openid})
        # b'eyJpYXQiOjE1MzExOTE0OTYsImV4cCI6MTUzMTE5NTA5NiwiYWxnIjoiSFMyNTYifQ.eyJvcGVuaWQiOiIwMUM1MDhCNEIzQzUyMDY0ODNCOUNBMDBDRjJDMkQzQyJ9.VCbhAXLbeJ09r_ri2J5uqTMx7IBjYG4P_fGO1sZ9m24'
        return token.decode()

    @classmethod
    def check_openid(cls, token):
        # 创建实例化 序列化器
        serializer = Serializer(settings.SECRET_KEY, 3600)

        # 校验(过期, 数据错误)
        try:
            result = serializer.loads(token)
        except BadSignature:
            return None
        else:
            return result.get('openid')



