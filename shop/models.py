from distutils.command.upload import upload
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

    class Meta:
        db_table = 'ShopType'


class Location(models.Model):
    location = models.CharField(
        max_length=50,
        help_text="지역 입력(예: 서울)"
    )

    def __str__(self) -> str:
        """
        Display title instead of ID
        """
        return self.location

    class Meta:
        db_table = 'Location'


class GenderStyle(models.Model):
    gender = models.CharField(
        max_length=50,
        help_text="매장이 취급하는 상품요소(여성향, 남성향) 입력"
    )

    def __str__(self) -> str:
        """
        Display title instead of ID
        """
        return self.gender

    class Meta:
        db_table = 'GenderStyle'


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
    # 매장 이름
    name = models.CharField(
        max_length=100,
        help_text="매장 이름 입력"
    )
    # 매장 지역 1:N
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True
    )
    # 매장 상세주소
    address = models.CharField(
        max_length=200,
        help_text="매장 상세주소 입력"
    )
    # 매장 운영시간
    workTime = models.TextField(
        help_text="매장 운영시간 입력"
    )
    # 매장 연락처
    contact = models.TextField(
        help_text="매장 연락처 입력"
    )
    # 매장 상세정보
    content = models.TextField(
        help_text="매장 상세정보 입력"
    )
    # 매장종류 N:M
    shopType = models.ManyToManyField(
        ShopType,
        help_text="매장 종류 선택 - "
    )
    # 매장 홈페이지주소
    homePage = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="매장 홈페이지 URL 입력"
    )
    # 매장 트위터주소
    twitter = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="twitter URL 입력"
    )
    # 매장의 성향 N:M
    genderStyle = models.ManyToManyField(
        GenderStyle,
        help_text="매장 성별 성향 선택 - "
    )
    # 매장 사진
    photo = models.ImageField(
        blank=True,
        null=True,
        upload_to='%Y%m%d%m'
    )

    def __str__(self) -> str:
        """
        Display title instead of ID
        """
        return self.name

    class Meta:
        db_table = 'ShopData'


class Comment(models.Model):
    '''Comments of ShopData
        * Nickname
        * Content of comment
        * Date of comment
    '''
    # 닉네임
    nickName = models.CharField(
        max_length=100
    )
    # 댓글 내용
    content = models.TextField()
    # 댓글 쓴 날짜
    date = models.DateTimeField()
    # 댓글을 달 샵 정보
    shop = models.ForeignKey(
        ShopData,
        on_delete=models.CASCADE,
        null=True)

    def __str__(self) -> str:
        """
        Display title instead of ID
        """
        return self.nickName

    class Meta:
        db_table = 'Comment'
