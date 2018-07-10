from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from urllib.parse import urlencode
from .utils import QQOauth
from .models import OAuthQQUser



class QQAuthURLView(APIView):
    """
    # /oauth/qq/statues/
    """

    def get(self, request):

        qq = QQOauth()

        auth_url = qq.get_url()

        return Response({'auth_url':auth_url})


class QQOauthCreateView(APIView):
    """
    根据 返回的code 生成 openid
    """
    # /oauth/qq/users/
    def get(self, request):
        code = request.query_params.get('code')

        qq = QQOauth()
        token = qq.get_token(code)

        openid = qq.get_openid(token)

        try:
            qquser = OAuthQQUser.object.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 说明未查找到用户,这跳转到绑定页面进行用户绑定
            return
        else:
            # 说明查找到了用户,直接返回主页,并惊醒登录

