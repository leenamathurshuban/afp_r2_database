from rest_framework import serializers
from product.models import WareHouse

class WareHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WareHouse
        fields = '__all__'

    def validate(self, attrs):

       get_warehouse_name = attrs.get('warehouse_name',None)

       if get_warehouse_name is None or get_warehouse_name == '':
           raise serializers.ValidationError({'error':'Ware House name is required'})
           
       return attrs

