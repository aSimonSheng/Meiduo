from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from .models import User
from .serializers import CreateUserSerializer, EmailSerializer
from rest_framework.generics import RetrieveAPIView, UpdateAPIView

class RegisterUsernameView(APIView):
    """
    判断用户名是否已经使用
    GET     usernames/(?P<username>\w{5,20})/count/
    """
    def get(self, request, username):
        #查询对象
        count = User.objects.filter(username=username).count()
        context = {
            'count':count,
            'username':username
        }
        return Response(context)


class MobileConutView(APIView):
    """
    判断电话号码是否已经注册
    GET     mobiles/(?P<mobile>1[3-9]\d{9})/count
    """
    def get(self, request, mobile):
        count = User.objects.filter(mobile= mobile).count()
        data= {
            'mobile':mobile,
            'count':count
        }
        return Response(data)

class RegisterCreateView(CreateAPIView):
    """
    用户注册
    POST /users/
    """
    serializer_class = CreateUserSerializer

from rest_framework.permissions import IsAuthenticated
from .serializers import UserCenterInfoserializer

class UserCenterInfoview(APIView):
    """
    GET
    1.获取用户信息
    2.权限验证,必须为登录用户
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserCenterInfoserializer(request.user)
        # 只有登录的用户才能访问该函数
        return Response(serializer.data)

# class UserCenterInfoview(RetrieveAPIView):
#     """
#     GET
#     1.获取用户信息
#     2.权限验证,必须为登录用户
#     """
#     permission_classes = [IsAuthenticated]
#
#     serializer_class = UserCenterInfoserializer
#
#     def get_object(self):
#         return self.request.user


class EmailView(UpdateAPIView):
    """
    邮件
    1.登录用户显示页面
    2.当我们单机板寸的时候,把邮件信息发送过来,修改数据
    3.我们需要发送,验证吗邮件
    """
    permission_classes = [IsAuthenticated]

    serializer_class = EmailSerializer

    def get_object(self):

        return self.request.user
