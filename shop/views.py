# Django Import
from django.http import Http404, QueryDict
from django.shortcuts import render
from django.db.models import Q

# rest_framework Import
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin

# seriallizer & model Import
from .serializers import ShopDataSerializer
from .models import ShopData

# type hint import
from typing import Dict
from django.db.models.query import QuerySet

# Create your views here.


class ShopInfo(ListModelMixin, CreateModelMixin, UpdateModelMixin, GenericAPIView):
    queryset = ShopData.objects.all()
    serializer_class = ShopDataSerializer
    
    def search(self, request) -> tuple:
        """query 검색하는 함수
        :param 
            name, location, shopType

        :return
            쿼리에 맞는 검색데이터 return
        """

        name: str = ''
        location: str = ''
        shoptype: str = ''

        # GET Method인 경우
        name = request.GET.get('name', None)
        location = request.GET.get('location', None)
        shoptype = request.GET.get('shopType', None)

        # POST Method인 경우
        name = request.POST.get('name', None)
        location = request.POST.get('location', None)
        shoptype = request.POST.get('shopType', None)

        # 필터링 옵션 적용
        search_option = Q()

        # 특정 매장 검색(특정문자열이 포함된 쿼리셋 반환)
        if name:
            search_option.add(Q(name__contains=name), Q.AND)

        # 지역 옵션 있는 경우
        if location:
            search_option.add(Q(location=location), Q.AND)

        # 매장 형태 옵션 있는 경우
        if shoptype:
            search_option.add(Q(shopType=shoptype), Q.AND)
            
        queryset = ShopData.objects.filter(search_option).distinct()
            
        return queryset, bool(queryset)
        

    def get(self, request, format=None):
        """ HTTP GET 요청 처리하는 함수
        :param request: http request가 담긴 데이터
            * name
            * location
            * shopType

        :return
            쿼리에 맞는 검색데이터 return
        """
        
        queryset, check = self.search(request)

        # 데이터 시리얼라이징
        result = ShopInfo.serializer_class(queryset, many=True)

        return Response(result.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
