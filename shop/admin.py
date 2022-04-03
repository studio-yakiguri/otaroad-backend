from django.contrib import admin
from .models import ShopData, Comments, ShopType, Location


class ShopDataAdmin(admin.ModelAdmin):
    search_fields = ['Name']
# Register your models here.


admin.site.register(ShopData, ShopDataAdmin)
admin.site.register(ShopType)
admin.site.register(Comments)
admin.site.register(Location)
