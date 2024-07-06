import django_filters
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from product.models import (
    Product,
    WareHouse
)
from account.models import (
    Role,
    User
)


class ProductFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter(field_name='created_at')
    class Meta:
        model = Product
        fields = ['date']



class WareHouseFilter(django_filters.FilterSet):
    class Meta:
        model = WareHouse
        fields = ['warehouse_name']



class RoleFilter(django_filters.FilterSet):
    class Meta:
        model = Role
        fields = ['role_name']


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['email']
