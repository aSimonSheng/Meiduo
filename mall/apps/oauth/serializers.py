# -*-coding:utf-8-*-
from django_redis import get_redis_connection
from rest_framework import serializers

from users.models import User
from .models import OAuthQQUser

class QQOauthCreatSerializer(serializers.Serializer):

    access_token = serializers.CharField(label='操作token')
    mobile = serializers.RegexField(label='手机号', regex=r'^1[345789]\d{9}$')  #通过设置正则匹配,进行验证
    password = serializers.CharField(label='密码', max_length=20, min_length=8)
    sms_code = serializers.CharField(label='短信验证码', max_length=6, min_length=6)



    def validate(self, attrs):
        # 验证用户提交的数据access_token
        # 通过在modil模块中进行功能的封装,实现对于access_token数据的校验,与处理
        openid = OAuthQQUser.check_openid(attrs.get('access_token'))

        if openid is None:
            raise serializers.ValidationError('数据错误')
        attrs['openid'] = openid
            # 验证短信码
        mobile = attrs['mobile']
        redis_conn = get_redis_connection('code')

        redis_code = redis_conn.get('sms_%s' % mobile)
        if redis_code.decode() != attrs['sms_code']:
            raise serializers.ValidationError('验证码错误')


        # 判断手机绑定的用户是否存在
        try:
            user = User.objects.get(mobile = mobile)
        except User.DoesNotExist:
            # 没有注册用户
            pass
        else:
            # 有注册用户,校验密码
            if not user.check_password(attrs.get('password')):
                raise  serializers.ValidationError('密码输入错误')
            attrs['user'] = user


        return attrs


    def create(self, validated_data):
        user = validated_data.get('user')
        if user is None:
            # 如果没有查找到用户,则新建用户信息
            user = User.objects.create(
                mobile = validated_data.get('mobile'),
                password = validated_data.get('password'),
                username = validated_data.get('usernaem')
            )
            user.set_password(validated_data.get('password'))
            user.save()
        # 如果能够查找到用户消息,则帮绑定用户消息
        OAuthQQUser.objects.create(
            openid = validated_data.get('openid'),
            user = user
        )

        return user
