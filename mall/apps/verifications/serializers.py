# -*-coding:utf-8-*-
from rest_framework import serializers
from django_redis import get_redis_connection


class RegisterSMSCodeserializaer(serializers.Serializer):
    text = serializers.CharField(label='图片验证码', max_length=4, min_length=4)
    image_code_id = serializers.UUIDField(label='uuid')
    """
    校验的四种方式
    1.字段类型
    2.字段选项
    3.单个字段
    4.多个字段
    """
    def validate(self, attrs):
        text = attrs.get('text')
        image_code_id = attrs.get('image_code_id')
        redis_conn = get_redis_connection('code')

        redis_text = redis_conn.get('img_%s'%image_code_id)

        if redis_text is None:
            raise serializers.ValidationError('验证码过期')
        # 比较
        if redis_text.decode().lower() != text.lower():
            raise serializers.ValidationError('验证码输入有误')

        redis_conn.delete('img_%s'%image_code_id)



        return attrs
