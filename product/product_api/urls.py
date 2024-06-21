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
    GetProductListAPI,
    ProductDeleteApi,
    ProductUpdateApi,
    ProductDetailApi,

    ProductImageDeleteApi,

    WipingQuestionsPostApi,
    WipingQuestionsUpdateApi,
    WipingQuestionsGetApi,
    WipingQuestionsDeleteApi,
    WipingQuestionListApi,

    ProductCheckOutPostApi,
    ProductCheckOutUpdateApi,
    ProductCheckOutGetApi,
    ProductCheckOutListApi,
    ProductCheckOutDeleteApi,

    generate_barcode, # For testing Purpose

)

urlpatterns = [
path('ware-house-post-api/',PostWareHouse.as_view(),name='post-ware-house-api'),
path('ware-house-update-api/<str:uid>/',UpdateWareHouse.as_view(),name="role-update-api"),
path('ware-house-list-api/',GetWareHouseList.as_view(),name='ware-house-get-api'),
path('ware-house-delete-api/<str:uid>/',DeleteWareHouse.as_view(),name='ware-house-delete-api'),
path('ware-house-detail-api/<str:uid>/',DetailWareHouse.as_view(),name='ware-house-detail-api'),


path('product-post-api/',ProductPostApi.as_view(),name='product-post-api'),
path('product-delete-api/<str:uid>/',ProductDeleteApi.as_view(),name='product-delete-api'),
path('product-update-api/<str:uid>/',ProductUpdateApi.as_view(),name='product-update-api'),
path('product-detail-api/<str:uid>/',ProductDetailApi.as_view(),name='product-detail-api'),
path('product-list-view/',GetProductListAPI.as_view(),name='product-list-view'),

path('product-image-delete-api/<str:uid>/',ProductImageDeleteApi.as_view(),name="product-image-delete-api"),

path('wiping-questions-post-api/',WipingQuestionsPostApi.as_view(),name='wiping-questions-post-api'),
path('wiping-questions-update-api/<str:uid>/',WipingQuestionsUpdateApi.as_view(),name='wiping-questions-update-api'),
path('wiping-questions-get-api/<str:uid>/',WipingQuestionsGetApi.as_view(),name='wiping-questions-get-api'),
path('wiping-questions-delete-api/<str:uid>/',WipingQuestionsDeleteApi.as_view(),name='wiping-questions-delete-api'),
path('wiping-questions-list-api/',WipingQuestionListApi.as_view(),name='wiping-questions-list-api'),

path('proudct-checkout-post-api/',ProductCheckOutPostApi.as_view(),name='proudct-checkout-post-api'),
path('product-checkout-update-api/<str:uid>/',ProductCheckOutUpdateApi.as_view(),name='product-checkout-update-api'),
path('product-checkout-get-api/<str:uid>/',ProductCheckOutGetApi.as_view(),name='product-checkout-get-api'),
path('product-checkout-list-api/',ProductCheckOutListApi.as_view(),name='product-check-list-api'),
path('product-checkout-delete-api/<str:uid>/',ProductCheckOutDeleteApi.as_view(),name='product-checkout-delete-api'),


path('bar-code/',generate_barcode.as_view()), # For testing Purpose

]
