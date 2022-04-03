from dataclasses import field
from rest_framework import serializers
from .models import ShopData


class ShopDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopData
        fields = '__all__'  # field를 모두 가져오는 것
        '''
        field = (
                'id',
                'name',
                'address',
                'workTime',
                'contact',
                'content',
                'homePage',
                'photo'
                'location',
                'shopType',
        )
        '''
