from django.urls import path
from product.product_api.views import (
    PostWareHouse,
    UpdateWareHouse,
    GetWareHouseList,
    DeleteWareHouse,
    DetailWareHouse,
    ProductPostApi,
    GetProductListAPI,

    ProductPostApi,
    ProductGetApi,
    ProductDeleteApi,
    ProductUpdateApi,
    ProductDetailApi,

    generate_barcode, # For testing Purpose

)

urlpatterns = [
path('ware-house-post-api/',PostWareHouse.as_view(),name='post-ware-house-api'),
path('ware-house-update-api/<str:uid>/',UpdateWareHouse.as_view(),name="role-update-api"),
path('ware-house-list-api/',GetWareHouseList.as_view(),name='ware-house-get-api'),
path('ware-house-delete-api/<str:uid>/',DeleteWareHouse.as_view(),name='ware-house-delete-api'),
path('ware-house-detail-api/<str:uid>/',DetailWareHouse.as_view(),name='ware-house-detail-api'),


path('product-post-api/',ProductPostApi.as_view(),name='product-post-api'),
path('product-get-api/',ProductGetApi.as_view(),name='product-get-api'),
path('product-delete-api/<str:uid>/',ProductDeleteApi.as_view(),name='product-delete-api'),
path('product-update-api/<str:uid>/',ProductUpdateApi.as_view(),name='product-update-api'),
path('product-detail-api/<str:uid>/',ProductDetailApi.as_view(),name='product-detail-api'),
path('product-list-view/',GetProductListAPI.as_view(),name='product-list-view'),

path('bar-code/',generate_barcode.as_view()), # For testing Purpose

]
