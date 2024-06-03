from django.urls import path
from product.product_api.views import (
    PostWareHouse,
    UpdateWareHouse,
    GetWareHouseList,
    DeleteWareHouse,
    DetailWareHouse
)

urlpatterns = [
path('ware-house-post-api/',PostWareHouse.as_view(),name='post-ware-house-api'),
path('ware-house-update-api/<str:uid>/',UpdateWareHouse.as_view(),name="role-update-api"),
path('ware-house-list-api/',GetWareHouseList.as_view(),name='ware-house-get-api'),
path('ware-house-delete-api/<str:uid>/',DeleteWareHouse.as_view(),name='ware-house-delete-api'),
path('ware-house-detail-api/<str:uid>/',DetailWareHouse.as_view(),name='ware-house-detail-api'),

]