# -*-coding:utf-8-*-
from django.conf.urls import url
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    # usernames/(?P<username>\w{5,20})/count/
    url(r'^usernames/(?P<username>\w{5,20})/count/$',
        views.RegisterUsernameView.as_view()),
    # GET /users/phones/(?P<mobile>1[345789]\d{9})/count/
    url(r'^phones/(?P<mobile>1[345789]\d{9})/count/$',
        views.MobileConutView.as_view()),
    # POST/users/
    url(r'^$', views.RegisterCreateView.as_view()),
    #  POST /users/auths/
    url(r'^auths/$', obtain_jwt_token),
    #GET /users/infos/
    url(r'^infos/$', views.UserCenterInfoview.as_view()),

    # PUT/users/emails/
    url(r'^emails/$', views.EmailView.as_view()),

    # GET /users/emails/verification/
    url(r'^emails/verification/$', views.VerifyEmailView.as_view())

]