from django.contrib import admin
from product.models import (
    WareHouse,
    Product,
    ProductImage
)

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['uid','serial_number','device_type','warehouse','model_number','model_family','storage_type']


class WareHouseAdmin(admin.ModelAdmin):
    list_display = ['uid','warehouse_name']

admin.site.register(Product, ProductAdmin)
admin.site.register(WareHouse,WareHouseAdmin)
admin.site.register(ProductImage)
