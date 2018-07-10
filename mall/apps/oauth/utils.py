# -*-coding:utf-8-*-
from urllib.request import urlopen
from urllib.parse import parse_qs, urlencode
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
import json



class QQOauth(object):


    def get_url(self):
        """
        这是一个通过验证开发着权限,返回一个code的功能模块
        :return: auth_url
        """
        # 用base_url
        # 生成auth_url
        # https://graph.qq.com/oauth2.0/authorize
        # 请求参数请包含如下内容：
        # response_type   必须      授权类型，此值固定为“code”。
        # client_id       必须      申请QQ登录成功后，分配给应用的appid。
        # redirect_uri    必须      成功授权后的回调地址，必须是注册appid时填写的主域名下的地址，建议设置为网站首页或网站的用户中心。注意需要将url进行URLEncode。
        # state           必须      client端的状态值。用于第三方应用防止CSRF攻击，成功授权后回调时会原样带回。请务必严格按照流程检查用户与state参数状态的绑定。
        # scope           可选      scope=get_user_info
        base_url = 'https://graph.qq.com/oauth2.0/authorize?'

        state = '/'
        # 组织参数
        params = {
            'response_type': 'code',
            'client_id': settings.QQ_APP_ID,
            'redirect_uri': settings.QQ_REDIRECT_URL,
            'state': state,
            # 'scope':'get_user_info'
        }

        auth_url = base_url + urlencode(params)

        return auth_url


    def get_token(self, code):
        '''
        这是一个通过qq返回的code向qq获取token的功能模块
        :param code:
        :return: token
        '''
        if code is None:
            return Response({'message':'缺少参数'},status=status.HTTP_400_BAD_REQUEST)

            # PC网站：https://graph.qq.com/oauth2.0/token
            # GET
            # grant_type      必须      授权类型，在本步骤中，此值为“authorization_code”。
            # client_id       必须      申请QQ登录成功后，分配给网站的appid。
            # client_secret   必须      申请QQ登录成功后，分配给网站的appkey。
            # code            必须      上一步返回的authorization
            # redirect_uri    必须      与上面一步中传入的redirect_uri保持一致。

        base_url = 'https://graph.qq.com/oauth2.0/token?'
        params = {
            'grant_type':'authorization_code',
            'client_id':settings.QQ_APP_ID,
            'client_secret':settings.QQ_APP_KEY,
            'code':code,
            'redirect_uri':settings.QQ_REDIRECT_URL,
        }


        token_url = base_url + urlencode(params)
        # 生成了URL需要自己请求

        response = urlopen(token_url)
        data = response.read().decode()

        dict = parse_qs(data)
        access_token = dict['access_token']

        toktn = access_token[0]

        return toktn


    def get_openid(self, token):
        '''
        这是一个通过qq返回的token向qq获取openid的功能模块
        :param token:
        :return: openid
        '''
        # https://graph.qq.com/oauth2.0/me
        # GET
        # access_token        必须      在Step1中获取到的accesstoken。

        # 返回数据PC网站接入时，获取到用户OpenID，返回包如下：
        # callback( {"client_id":"YOUR_APPID","openid":"YOUR_OPENID"} );
        # openid是此网站上唯一对应用户身份的标识，网站可将此ID进行存储便于用户下次登录时辨识其身份，
        # 或将其与用户在网站上的原有账号进行绑定

        base_uel = 'https://graph.qq.com/oauth2.0/me?'
        params = {
            'access_token':token
        }

        openid_url = base_uel + urlencode(params)

        # urlopen(openid_uel) 来获取数据
        response = urlopen(openid_url)
        data = response.read().decode()
        # 获取数据,并讲数据截取,处理.
        try:
            dict = json.loads(data[10:-4])
        except Exception:
            raise Exception('数据获取失败')

        openid = dict.get('openid')

        if openid is not None:
            return openid


        # print(data)