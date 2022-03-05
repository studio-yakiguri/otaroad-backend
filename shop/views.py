from django.shortcuts import render

from rest_framework import viewsets
from .serializers import ShopDataSerializer
from .models import ShopData

# Create your views here.


class ShopDataViewSet(viewsets.ModelViewSet):
    queryset = ShopData.objects.all()
    serializer_class = ShopDataSerializer
