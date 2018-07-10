# -*-coding:utf-8-*-
from django.conf.urls import url
from . import views

urlpatterns = [
    # qq/statues/
    url(r'^qq/statues/$', views.QQAuthURLView.as_view()),
    # /oauth/qq/users/
    url(r'^qq/users/$', views.QQOauthCreateView.as_view()),
]