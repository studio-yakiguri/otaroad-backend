from rest_framework import serializers
from .models import ShopData
from .models import Comment


class ShopDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopData
        fields = '__all__'  # field를 모두 가져오는 것


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
