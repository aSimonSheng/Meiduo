from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from urllib.parse import urlencode

from rest_framework_jwt.settings import api_settings

from .utils import QQOauth
from .models import OAuthQQUser
from .serializers import QQOauthCreatSerializer



class QQAuthURLView(APIView):
    """
    # /oauth/qq/statues/
    """

    def get(self, request):
        """

        :param request:
        :return: 申请地三方入口的详细地址
        """

        qq = QQOauth()

        auth_url = qq.get_url()

        return Response({'auth_url':auth_url})


class QQOauthCreateView(APIView):
    """
    根据 返回的code 生成 openid,并完成用户的绑定
    """
    # /oauth/qq/users/
    def get(self, request):
        """
        通过第三方获取到了openid,通过openid产找数据库,若找到数据库中绑定了该openid
        则返回一个登录token,否则,则进行openid绑定,进行post请求
        :param request:
        :return: token
        """
        code = request.query_params.get('code')

        qq = QQOauth()
        token = qq.get_token(code)

        openid = qq.get_openid(token)

        try:
            qquser = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 说明未查找到用户,这跳转到绑定页面进行用户绑定
            access_token = OAuthQQUser.genericte_open_id_token(openid)

            return Response({'access_token':access_token})
        else:
            user = qquser.user
            # 说明查找到了用户,直接返回主页,并惊醒登录
            # 生成已登录的token
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            response = Response({
                'token': token,
                'user_id': user.id,
                'username': user.username
            })

            return response


    def post(self, request):
        """
        通过前面get请求访问不到数据后,通过post请求,惊醒绑定用户
        1.将手机号 ,密码, 短信验证码,以及access_token(openid)提交到后端
        2.对手机号,access_token进行校验
        3.讲校验信息,晕openid进行处理
        :param request:
        :return: token
        """

        # 创建序列化器
        serializer = QQOauthCreatSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        # 生成已登录的token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        response = Response({
            'token': token,
            'user_id': user.id,
            'username': user.username
        })

        return response



