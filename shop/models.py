from django.db import models
from django.forms import ImageField

# Create your models here.
class ShopType(models.Model):
    type = models.CharField(max_length=50, help_text="매장 종류를 입력(예: 서점)")
    def __str__(self) -> str:
        """
        Display title instead of ID
        """
        return self.type
    
class Location(models.Model):
    location = models.CharField(max_length=50, help_text="지역 입력(예: 서울)")
    def __str__(self) -> str:
        """
        Display title instead of ID
        """
        return self.location
    
class ShopData(models.Model):
    '''Contained info of ShopData
        * shopname
        * shop location
        * shop WorkTime
        * shop contact
        * shop content
        * shop type
        * shop homepage
        * shop photo
    '''
    name = models.CharField(max_length=100, help_text="매장 이름 입력")   # 매장 이름
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True) # 매장 지역
    address = models.CharField(max_length=200, help_text="매장 상세주소 입력") # 매장 상세주소
    workTime = models.TextField(help_text="매장 운영시간 입력")  # 매장 운영시간
    contact = models.TextField(help_text="매장 연락처 입력")  # 매장 연락처
    content = models.TextField(help_text="매장 상세정보 입력")   # 매장 상세정보
    shopType = models.ManyToManyField(ShopType, help_text="매장 종류 선택", )  # 매장종류
    homePage = models.CharField(max_length=100, blank=True, null=True) # 매장 홈페이지주소
    photo = models.ImageField(blank=True, null=True)  # 매장 사진

    def __str__(self) -> str:
        """
        Display title instead of ID
        """
        return self.name

class Comments(models.Model):
    '''Comments of ShopData
        * Nickname
        * Content of comment
        * Date of comment
    '''
    nickName = models.CharField(max_length=100)  # 닉네임
    content = models.TextField()   # 댓글 내용
    date = models.DateTimeField()   # 댓글 쓴 날짜

    def __str__(self) -> str:
        """
        Display title instead of ID
        """
        return self.nickName
