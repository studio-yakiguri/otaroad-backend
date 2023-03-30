# Django Import
from django.db.models import Q

# rest_framework Import
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin

# seriallizer & model Import
from .serializers import ShopDataSerializer
from .models import ShopData

# loogging Import
import logging

# type hint import
from django.db.models.query import QuerySet
from django.http import QueryDict

# Geocode Module import
from .module.naver import Geocoding as NaverGeo
from .module.kakao import Geocoding as KakaoGeo

# requests exception import
from requests import exceptions

# Create your views here.
logger = logging.getLogger('shop')


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

    queryset: QuerySet = ShopData.objects.filter(search_option).distinct()

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

        # 중복 데이터 생성 방지
        if check is True:
            return Response(
                'This Shop is already registered', status=status.HTTP_409_CONFLICT
            )

        # 지오코딩 객체 선언을 위한 깡통 변수 선언
        geocoding = None

        # x, y값이 임의로 입력된 경우가 없는 경우 -> API 좌표 요청
        if bool(request.data['x']) is not True:
            try:
                geocoding = KakaoGeo(request.data['address'])
            except ValueError or exceptions.ConnectionError or exceptions.HTTPError:
                print('Try to connect to NaverMap API')
                try:
                    geocoding = NaverGeo(request.data['address'])
                except ValueError as e:
                    return Response(
                        e, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                except exceptions.ConnectionError or exceptions.HTTPError as e:
                    return Response(
                        e, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            x, y = geocoding.cordinates()
            request_data: QueryDict = request.data.copy()
            request_data.update(request.data)
            request_data['x'] = x
            request_data['y'] = y

            # Twitter 주소가 mobile 주소가 들어왔을 경우
            twitter_id = request_data['twitter'][27:]
            if request_data['twitter'][0:26] == 'https://mobile.twitter.com':
                changed_address = 'https://twitter.com/' + twitter_id
                request_data['twitter'] = changed_address

            # Serialization override
            serializer = self.get_serializer(data=request_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return self.create(request, *args, **kwargs)


class ShopInfo(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    queryset = ShopData.objects.all()
    serializer_class = ShopDataSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs) -> Response:
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs) -> Response:
        return self.update(request, *args, **kwargs)
