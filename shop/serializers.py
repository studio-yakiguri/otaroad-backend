from dataclasses import field
from rest_framework import serializers
from .models import ShopData


class ShopDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopData
        fields = '__all__'
        '''
        field = (
                'id',
                'name',
                'location',
                'workTime',
                'contact',
                'content',
                'shopType',
                'photo'
        )
        '''
