from django.db import models
from datetime import datetime


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
        * shop content
        * shop type
        * shop email
        * shop phone
        * shop homepage
        * shop photo
    '''

    # Image save path Functions for image field
    def image_upload_path(instance, filename):
        ext: str = filename[-4:]
        uploaded_date = datetime.today().strftime('%Y%m%d%H%M%S')
        filename = f'{uploaded_date}{ext}'
        return f'shop_{instance.id}/{filename}'  # type: ignore

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

    # 매장 상세정보
    content = models.TextField(
        help_text="매장 상세정보(판매굿즈, 주차가능여부 등등) 입력"
    )

    # 매장종류 N:M
    shopType = models.ManyToManyField(
        ShopType,
        help_text="매장 종류 선택"
    )

    # 매장 이메일 주소
    email = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="매장 이메일 주소 입력 -> 'example@email.com'"
    )

    # 매장 홈페이지 주소
    phone = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="매장 전화번호 입력 -> '010-1234-5678'"
    )

    # 매장 홈페이지 주소
    homePage = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="매장 홈페이지 URL 입력 -> 'https://example.com'"
    )

    # 매장 트위터 주소
    twitter = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="트위터 URL 입력 -> 'https://twitter.com/트위터ID'"
    )

    # 매장의 성향 N:M
    genderStyle = models.ManyToManyField(
        GenderStyle,
        help_text="매장 성별 성향 선택"
    )

    # 매장 사진
    photo = models.ImageField(
        blank=True,
        null=True,
        upload_to=image_upload_path  # type: ignore
    )

    # 매장 x 좌표
    x = models.FloatField(
        help_text="x좌표 입력(자동입력 됨)",
        null=True
    )

    # 매장 y 좌표
    y = models.FloatField(
        help_text="y좌표 입력(자동입력 됨)",
        null=True
    )

    def __str__(self) -> str:
        """
        Display title instead of ID
        """
        return self.name

    class Meta:
        db_table = 'ShopData'
