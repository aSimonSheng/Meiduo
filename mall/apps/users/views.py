from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from .models import User
from .serializers import CreateUserSerializer


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

