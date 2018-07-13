#coding:utf8
from rest_framework import serializers


from .models import User
from django_redis import get_redis_connection
from django.conf import settings

#ModelSerializer
#Serializer

# 第一点: 可以自动创建create方法
# 第二点: 有模型关联
class CreateUserSerializer(serializers.ModelSerializer):


    # 反序列化[将数据转换为模型]中的数据校验
    # read_only 只读 序列化的时候使用
    # write_only 必须传入
    password2 = serializers.CharField(label='确认密码',write_only=True,
                                      allow_null=False,allow_blank=False)
    sms_code = serializers.CharField(label='短信验证码', max_length=6,
                                     min_length=6, allow_null=False,
                                     allow_blank=False,
                                     write_only=True)
    allow = serializers.CharField(label='是否同意协议', allow_null=False,
                                  allow_blank=False, write_only=True)

    token = serializers.CharField(label='token', read_only=True)

    class Meta:
        model = User
        fields = ['id','username','password','mobile','password2','sms_code','allow', 'token']
        extra_kwargs = {
            'id':{
                'read_only':True
            },
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    # 我们需要把 用户名 密码,确认密码,手机号,短信验证码, 是否同意

    # 单个字段校验
    # 手机号,是否同意
    def validate_mobile(self,value):
        import re
        if not re.match(r'1[3-9]\d{9}',value):
            raise serializers.ValidationError('手机号错误')

        return value

    def validate_allow(self,value):

        if value != 'true':
            raise serializers.ValidationError('您未同意协议')


        return value

    #多个字段校验
    #密码,确认密码  短信验证码,
    def validate(self, attrs):


        # 1.密码
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password2 != password:
            raise serializers.ValidationError('密码不一致')

        # 2.短信验证码
        # 获取用户提交的验证码
        code = attrs.get('sms_code')

        # 获取redis的验证码
        redis_conn = get_redis_connection('code')

        # 获取之后需要进行判断

        redis_code = redis_conn.get('sms_%s'%attrs.get('mobile'))
        if redis_code is None:
            raise serializers.ValidationError('验证码过期')
        #校验
        # redis的值 是bytes类型
        if redis_code.decode() != code:
            raise serializers.ValidationError('验证码错误')


        return attrs


    # 因为我们在序列化器中 添加了3个字段
    # 这3个字段是不应该入库的

    #重写 create方法
    def create(self, validated_data):

        #validated_data 包含 那3个字段
        del validated_data['password2']
        del validated_data['allow']
        del validated_data['sms_code']

        #重新入库
        # user = User.objects.create(**validated_data)
        # print(validated_data)
        user = super().create(validated_data)

        #入库的问题密码还是明文
        #User 继承 AbstractUser
        user.set_password(validated_data['password'])
        #保存密码
        user.save()

        # 注册后直接登录 注册后返回一个token
        from rest_framework_jwt.settings import api_settings

        # 获取这两个方法
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        data = jwt_payload_handler(user)
        token = jwt_encode_handler(data)

        user.token = token

        return user



class UserCenterInfoserializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email', 'email_active')


class EmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email']
        extra_kwargs = {
            'email':{
                'required':True
            }
        }


    def update(self, instance, validated_data):
        # 更新数据
        email = validated_data.get('email')
        instance.email = email
        instance.save()


        verify_url = instance.generic_email_url(email)

        # 更新邮箱信息的时候发送邮件
            # 发送主题
        subject = '邮件验证'
            # 发送的简单内容
        message = ''
            # 发送人邮件
        from_email = settings.EMAIL_FROM
            # 收件人列表
        recipient_list = [email]
            # 发送的内容(复杂的html页面)
        html_message = '<p>尊敬的用户您好！</p>' \
                       '<p>感谢您使用美多商城。</p>' \
                       '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                       '<p><a href="%s">%s<a></p>' % (email, verify_url, verify_url)

        # send_mail(
        #     subject=subject,
        #     message=message,
        #     from_email=from_email,
        #     recipient_list=recipient_list,
        #     html_message=html_message,
        #     )
        from celery_tasks.email.tasks import send_verify_emali
        send_verify_emali(subject=subject, message= message, from_email=from_email, recipient_list=recipient_list, html_message=html_message)

        return instance


