# -*-coding:utf-8-*-
import re

from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }

from django.contrib.auth.backends import ModelBackend


# 定义一个方法,根据正则匹配手机号,如果不满足手机号,则是使用用户名校验

def get_user_by_account(username):
    try:
        if re.match(r'1[3-9]\d{9}', username):

            user = User.objects.get(mobile=username)

        else:
            user = User.objects.get(username=username)
    except User.DoesNotExist:
        user=None

    return user

class LoginMobileUsernameModelBackend(ModelBackend):
    """
    如果用户输入手机号.通过手机号,找到该用户
    然后进行校验
    """


    def authenticate(self, request, username=None, password=None, **kwargs):

        user = get_user_by_account(username)
        if user is not None and user.check_password(password):
            return user
        return None