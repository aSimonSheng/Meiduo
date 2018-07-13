from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Area
from .serializer import AreaSerializer, SubAreaSerializer

class AreasView(ReadOnlyModelViewSet):


    def get_queryset(self):

        if self.action == 'list':

            return Area.objects.filter(parent=None)
        else:
            return Area.objects.all()

    def get_serializer_class(self):

        if self.action == 'list':

            return AreaSerializer

        else:

            return SubAreaSerializer

    pass
