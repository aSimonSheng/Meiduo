# -*-coding:utf-8-*-
from django.conf.urls import url,include
from rest_framework.routers import DefaultRouter
from .views import AreasView

router = DefaultRouter()
router.register(r'infos',AreasView,base_name='area')

urlpatterns = [
    # url(r'^',include(router.urls))
]

#添加省市区信息查询路由
urlpatterns += router.urls