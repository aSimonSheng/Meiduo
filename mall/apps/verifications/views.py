from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from django.http import HttpResponse
from rest_framework.generics import GenericAPIView
from libs.yuntongxun.sms import CCP
from .serializers import RegisterSMSCodeserializaer
from random import randint
from rest_framework.response import Response



class RegisterImageCodeView(APIView):
    """
    生成验证码
    GET verifications/imagecodes/(?P<image_code_id>.+)/
    需要通过JS生成一个唯一码,以确保后台对图片进行校验
    """

    def get(self,request,image_code_id):
        """
        通过第三方库,生成图片和验证码,我们需要对验证码进行redis保存

        思路为:
        创建图片和验证码
        通过redis进行保存验证码,需要在设置中添加 验证码数据库选项
        将图片返回
        """
        # 创建图片和验证码
        text,image = captcha.generate_captcha()
        # 通过redis进行保存验证码
        redis_conn = get_redis_connection('code')
        redis_conn.setex('img_%s'%image_code_id,60,text)
        # 将图片返回
        #注意,图片是二进制,我们通过HttpResponse返回
        return HttpResponse(image,content_type='image/jpeg')

class RegisterSMSCodeView(GenericAPIView):
    """
    smscodes/(?P<mobile>1[345789]\d{9})/?text=xxxx & image_code_id=xxxx
    """
    serializer_class = RegisterSMSCodeserializaer
    def get(self, requset, mobile):
        serializer = self.get_serializer(data = requset.query_params)
        serializer.is_valid(raise_exception = True)

        sms_code = "%06d"%randint(0, 999999)

        redis_conn = get_redis_connection('code')

        redis_conn.setex('sms_%s' %mobile, 5*60, sms_code)


        from celery_tasks.sms.tasks import send_sms_code
        send_sms_code.delay(mobile, sms_code)


        return Response({'message':'OK'})