# -*-coding:utf-8-*-
from django.conf.urls import url
from . import views

urlpatterns = [
    # imagecodes/(?P<image_code_id>.+)/
    url(r'^imagecodes/(?P<image_code_id>.+)/$', views.RegisterImageCodeView.as_view(), name='imagecode'),
    # smscodes/(?P<mobile>1[345789]\d{9})/?text=xxxx & image_code_id=xxxx
    url(r'^smscodes/(?P<mobile>1[345789]\d{9})/$', views.RegisterSMSCodeView.as_view())
]