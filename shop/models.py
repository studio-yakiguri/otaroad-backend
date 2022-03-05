from django.db import models
from django.forms import ImageField

# Create your models here.


class Data(models.Model):
    '''
        ## 매장정보가 담겨있는 모델
        * 매장이름
        * 매장위치
        * 매장운영시간
        * 매장 연락처
        * 매장 정보
        * 매장 종류
        * 매장 사진
    '''
    name = models.CharField(max_length=100)   # 매장이름
    location = models.CharField(max_length=200)   # 매장위치
    workTime = models.CharField(max_length=100)   # 매장운영시간
    contact = models.CharField(max_length=100)   # 매장 연락처
    content = models.TextField()   # 매장 정보
    shopType = models.CharField(max_length=100)   # 매장 종류
    photo = models.ImageField()   # 매장 사진


class Comment(models.Model):
    '''
        ## 매장정보에 대한 댓글
        * 닉네임
        * 댓글 내용
        * 댓글 쓴 날짜
    '''
    nickName = models.CharField(max_length=100)  # 닉네임
    content = models.TextField()   # 댓글 내용
    date = models.DateTimeField()   # 댓글 쓴 날짜
