from django.contrib import admin
from product.models import (
    WareHouse,
    Product,
    ProductImage
)

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['uid','serial_number','device_type','warehouse','model_number','model_family','storage_type']



admin.site.register(Product, ProductAdmin)
admin.site.register(WareHouse)
admin.site.register(ProductImage)
