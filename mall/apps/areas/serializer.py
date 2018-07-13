# -*-coding:utf-8-*-
from  rest_framework import serializers

from .models import Area


class AreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = ['id', 'name']



class SubAreaSerializer(serializers.ModelSerializer):

    # area_set = AresSerializer(many=True, read_only=True)
    # 这个subs在models中起的名字
    subs = AreaSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        fields = ['id', 'name', 'subs']

