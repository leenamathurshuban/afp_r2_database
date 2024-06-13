from django.contrib import admin
from product.models import (
    WareHouse,
    Product,
    ProductImage,
    WipingQuestionnaire,
    ProductCheckOut,
)

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['uid','serial_number','device_type','warehouse','model_number','model_family','storage_type']


class WareHouseAdmin(admin.ModelAdmin):
    list_display = ['uid','warehouse_name']

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id','uid','product','image','type']

class WipingQuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['id','uid','product','first_name','last_name','data_wiped','software_used','software_reason']

class ProductCheckOutAdmin(admin.ModelAdmin):
    list_display = ['id','uid','product','first_name','last_name','created_at']



admin.site.register(Product, ProductAdmin)
admin.site.register(WareHouse,WareHouseAdmin)
admin.site.register(ProductImage,ProductImageAdmin)
admin.site.register(WipingQuestionnaire,WipingQuestionnaireAdmin)
admin.site.register(ProductCheckOut,ProductCheckOutAdmin)
