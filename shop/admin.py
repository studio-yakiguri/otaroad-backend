from django.contrib import admin
from .models import ShopData, ShopType, Location, GenderStyle


@admin.register(ShopData)
class ShopDataAdmin(admin.ModelAdmin):
    search_fields = ['name', 'shopType__type', 'location__location']  # 검색옵션
    list_filter = ['shopType__type', 'location__location']  # 표시 필터 옵션
    list_per_page = 25  # 한 페이지당 몇 표시
    list_display = ['id', 'name', 'location', 'shoptag']  # 리스트에 표시되는 attribute
    list_display_links = ['name']

    # admin에서 가져온 쿼리셋에서 릴레이션 된거 가져오기
    def get_queryset(self, obj):
        qs = super(ShopDataAdmin, self).get_queryset(obj)
        return qs.prefetch_related('shopType')

    # shopType 관련된거 모두 리스트로 밷기
    def shoptag(self, obj):
        return list(obj.shopType.all())


# Register your models here.
admin.site.register(ShopType)
admin.site.register(Location)
admin.site.register(GenderStyle)
