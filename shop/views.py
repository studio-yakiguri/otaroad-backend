# Django Import
from django.http import HttpResponseNotAllowed
from django.shortcuts import render
from django.db.models import Q
from django.db import transaction

# rest_framework Import
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin

# seriallizer & model Import
from .serializers import ShopDataSerializer
from .models import ShopData

# type hint import
from django.db.models.query import QuerySet

# Create your views here.


def search(request) -> tuple:
    """query 검색하는 함수
    :param
        name, location, shopType

    :return
        쿼리에 맞는 검색데이터 return
    """

    name: str = ''
    location: str = ''
    shoptype: str = ''

    if bool(request.GET) is True:
        name: str = request.GET.get('name', None)
        location: str = request.GET.get('location', None)
        shoptype: str = request.GET.get('shopType', None)

    if bool(request.POST) is True:
        name: str = request.POST.get('name', None)
        location: str = request.POST.get('location', None)
        shoptype: str = request.POST.get('shopType', None)

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


class ShopList(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = ShopData.objects.all()
    serializer_class = ShopDataSerializer

    def get(self, request, format=None) -> Response:
        queryset = search(request)[0]
        result = ShopList.serializer_class(queryset, many=True)
        return Response(result.data)

    def post(self, request, *args, **kwargs) -> Response:
        check = search(request)[1]
        if check is False:
            return self.create(request, *args, **kwargs)
        else:
            return Response()


class ShopInfo(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    queryset = ShopData.objects.all()
    serializer_class = ShopDataSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs) -> Response:
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs) -> Response:
        return self.update(request, *args, **kwargs)
