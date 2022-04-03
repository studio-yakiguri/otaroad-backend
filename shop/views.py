# Django Import
from django.http import Http404, QueryDict
from django.shortcuts import render
from django.db.models import Q

# rest_framework Import
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# seriallizer & model Import
from .serializers import ShopDataSerializer
from .models import ShopData

# type hint import
from typing import Dict
from django.db.models.query import QuerySet

# Create your views here.

# 지역 구분 코드(DB 필터링용)
LOCAL_CODE: Dict[str, int] = {
    "서울": 1,
    "부산": 2,
    "대구": 3,
    "인천": 4,
    "광주": 5,
    "대전": 6,
    "울산": 7,
    "세종": 8,
    "경기도": 9,
    "강원도": 10,
    "충청북도": 11,
    "충청남도": 12,
    "전라북도": 13,
    "전라남도": 14,
    "경상북도": 15,
    "경상남도": 16,
    "제주도": 17,
    "전국" : 18
}

# 샵 구분 코드(DB 필터링용)
SHOP_CODE: Dict[str, int] = {
    "카페": 1,
    "오락실": 2,
    "굿즈샵": 3,
    "식당": 4,
    "서점": 5,
    "전체": 6
}


class ShopInfo(APIView):
    def get(self, request, format=None):
        """ HTTP GET 요청 처리하는 함수
        param
            * name (봉인)
            * location
            * shopType
            
        return
            쿼리에 맞는 검색데이터 return
        """
        
        # query요청 데이터 담기
        name = request.GET.get('name', None)
        location = request.GET.get('location', None)
        shoptype = request.GET.get('shopType', None)
        
        #print(name, location, shoptype)
        
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
        '''
        name: str = query['name'] if 'name' in query else "" 
        location: int = LOCAL_CODE[query['location']] if 'location' in query else 18
        shoptype: int = SHOP_CODE[query['shopType']] if 'shopType' in query else 6
        queryset = None  # 쿼리셋 담는 변수
        '''
        
        # DB로 부터 데이터 가져오기 
        # distinct() 사용하여 중복 데이터 제거
        '''
        queryset: QuerySet = ShopData.objects.filter(
            Q(location=location) |
            Q(shopType=shoptype)
        ).distinct()
        '''
        
        # queryset = ShopData.objects.all()
                
        serializer = ShopDataSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        """ HTTP POST 요청 처리하는 함수
        param
        * name
        * location
        """
        serializer = ShopDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)