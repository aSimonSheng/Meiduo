from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from urllib.parse import urlencode
from .utils import QQOauth



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
    根据 返回的code 生成 token
    """
    # /oauth/qq/users/
    def get(self, request):
        code = request.query_params.get('code')

        qq = QQOauth()
        token = qq.get_token(code)

        return token


