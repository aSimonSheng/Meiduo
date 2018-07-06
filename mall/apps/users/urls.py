# -*-coding:utf-8-*-
from django.conf.urls import url
from . import views

urlpatterns = [
    # usernames/(?P<username>\w{5,20})/count/
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.RegisterUsernameView.as_view()),
    # GET /users/phones/(?P<mobile>1[345789]\d{9})/count/
    url(r'^phones/(?P<mobile>1[345789]\d{9})/count/$', views.MobileConutView.as_view())

]