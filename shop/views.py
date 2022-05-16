# Django Import
from django.http import Http404, QueryDict
from django.shortcuts import render
from django.db.models import Q

# rest_framework Import
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin

# seriallizer & model Import
from .serializers import ShopDataSerializer
from .models import ShopData

# type hint import
from typing import Dict
from django.db.models.query import QuerySet

# Create your views here.


class ShopInfo(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = ShopData.objects.all()
    serializer_class = ShopDataSerializer

    def get(self, request, format=None):
        """ HTTP GET 요청 처리하는 함수
        :param request: http request가 담긴 데이터
            * name
            * location
            * shopType

        :return
            쿼리에 맞는 검색데이터 return
        """

        # query요청 데이터 담기
        name = request.GET.get('name', None)
        location = request.GET.get('location', None)
        shoptype = request.GET.get('shopType', None)

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

        # 데이터 불러오기
        queryset = ShopData.objects.filter(search_option).distinct()

        # 데이터 시리얼라이징
        result = ShopInfo.serializer_class(queryset, many=True)

        return Response(result.data)

    def post(self, request, *args, **kwargs):
        """ HTTP POST 요청 처리하는 함수
        param
        * name
        * location
        """
        '''
        serializer_class = ShopDataSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        '''
        return self.create(request, *args, **kwargs)
