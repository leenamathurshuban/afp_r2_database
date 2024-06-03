from django.contrib import admin
from product.models import (
    WareHouse
)

# Register your models here.
class WareHouseAdmin(admin.ModelAdmin):
    list_display = ['uid','warehouse_name']

admin.site.register(WareHouse,WareHouseAdmin)