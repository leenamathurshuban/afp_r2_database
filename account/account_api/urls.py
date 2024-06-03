from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView
)
from account.account_api.views import (
    RegisterAPI,
    LoginView,
    
    UserdetailApi,
    UserDeleteApi,
    UserUpdateView,
    UserListView,

    RolePostApi,
    RoleUpdateApi,
    RoleGetApi,
    RoleDeleteApi,
    
)

urlpatterns = [

    path('api/token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('user-login/',LoginView.as_view(), name='user-login'),

    path('user-register-view/',RegisterAPI.as_view(), name='user-register-view'),
    path('user-update-api/<str:uid>/',UserUpdateView.as_view(), name='user-update-api'),
    path('user-list-view/',UserListView.as_view(), name='user-list-view'),
    path('user-detail-api/<str:uid>/',UserdetailApi.as_view(),name='user-detail-api'),
    path('user-delete-view/<str:uid>/',UserDeleteApi.as_view(),name='user-delete-view'),

    path('role-post-api/', RolePostApi.as_view(),name="role-post-api"),
    path('role-update-api/<str:uid>/',RoleUpdateApi.as_view(),name="role-update-api"),
    path('role-get-api/',RoleGetApi.as_view(),name="role-get-api"),
    path('role-delete-api/<str:uid>/',RoleDeleteApi.as_view(),name="role-delete-api"), 
    
]
