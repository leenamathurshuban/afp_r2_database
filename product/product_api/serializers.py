from rest_framework import serializers
from product.models import (
    WareHouse,
    Product,
    ProductImage
)
from account.models import (
    User
)

class WareHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WareHouse
        fields = ['id','uid','warehouse_name']

    def validate(self, attrs):

       get_warehouse_name = attrs.get('warehouse_name',None)

       if get_warehouse_name is None or get_warehouse_name == '':
           raise serializers.ValidationError({'warehouse_name':'warehouse_name is required'})
           
       return attrs

class UpdateWareHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WareHouse
        fields = ['id','uid','warehouse_name']


class ProductSerializer(serializers.ModelSerializer):
       
    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, attrs):
      
         get_serial_number = attrs.get('serial_number',None)
         get_year = attrs.get('year',None)
         get_product_size = attrs.get('product_size',None)
         get_device_type =attrs.get('device_type',None)
         get_product_status = attrs.get('product_status',None)
         get_model_number = attrs.get('model_number',None)
         get_emc_number = attrs.get('emc_number',None)
         get_model_family = attrs.get('model_family',None)
         get_memory = attrs.get('memory',None)
         get_storage_type = attrs.get('storage_type',None)
         get_storage_size = attrs.get('storage_size',None)
         get_battery_capacity = attrs.get('battery_capacity',None)
         get_battery_cycles = attrs.get('battery_cycles',None)
         get_grade = attrs.get('grade',None)
         get_grade_notes = attrs.get('grade_notes',None)
         get_technical_notes = attrs.get('technical_notes',None)

         
         if get_serial_number is None or get_serial_number == '':
            raise serializers.ValidationError({'serial_number':'serial_number is required'})
         
         if get_year is None or get_year == '':
            raise serializers.ValidationError({'year':'year is required'})
         
         if get_product_size is None or get_product_size == '':
            raise serializers.ValidationError({'product_size':'product_size is required'})
         
         if get_device_type is None or get_device_type == '':
            raise serializers.ValidationError({'device_type':'device_type is required'})
         
         if get_product_status is None or get_product_status == '':
            raise serializers.ValidationError({'product_status':'product_status is required'})
         
         if get_model_number is None or get_model_number == '':
            raise serializers.ValidationError({'model_number':'model_number is required'})
         
         if get_emc_number is None or get_emc_number == '':
            raise serializers.ValidationError({'emc_number':'emc_number is required'})
         
         if get_model_family is None or get_model_family == '':
            raise serializers.ValidationError({'model_family':'model_family is required'})
         
         if get_memory is None or get_memory == '':
            raise serializers.ValidationError({'memory':'memory is required'})
         
         if get_storage_type is None or get_storage_type == '':
            raise serializers.ValidationError({'storage_type':'storage_type is required'})
         
         if get_storage_size is None or get_storage_size == '':
            raise serializers.ValidationError({'storage_size':'storage_size is required'})
         
         if get_battery_capacity is None or get_battery_capacity == '':
            raise serializers.ValidationError({'battery_capacity':'battery_capacity is required'})
         
         if get_battery_cycles is None or get_battery_cycles == '':
            raise serializers.ValidationError({'battery_cycles':'battery_cycles is required'})
         
         if get_grade is None or get_grade == '':
            raise serializers.ValidationError({'grade':'grade is required'})
         
         if get_grade_notes is None or get_grade_notes == '':
            raise serializers.ValidationError({'grade_notes':'grade_notes is required'})
         
         if get_technical_notes is None or get_technical_notes == '':
            raise serializers.ValidationError({'technical_notes':'technical_notes is required'})
            
         get_product_instance = Product.objects.filter(warehouse= attrs['warehouse'],
                                                      serial_number=get_serial_number,
                                                      device_type= get_device_type,
                                                      product_status='CHECKED-IN',
                                                      model_number= get_model_number,
                                                      storage_type= get_storage_type,
                                                      storage_size= get_storage_size,
                                                      )

         if get_product_instance.exists():
               raise serializers.ValidationError({'error':'Product already Checked-in!'})
           
         return attrs

    
      


# Added below code on 05/06/2024
class UserListSerializerForProduct(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','user_uid','username','first_name','last_name']

class ProductImageSerializer(serializers.ModelSerializer):
       class Meta:
             model = ProductImage
             fields = ['id','uid','product','image','type']


class GetProductListSerializer(serializers.ModelSerializer):
    warehouse = WareHouseSerializer()
    created_by = UserListSerializerForProduct()
    product_image = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'

   

    def to_representation(self,instance):
          
         data = super(GetProductListSerializer, self).to_representation(instance)
         print('data:-====',data['product_image'])

         if len(data['product_image']) == 0:
                data['product_image'] = [{
                           'id': 'test', 
                           'uid': 'test', 
                           'product': 'test',
                           'image': '/media/product_image/default_product_image.jpg', 
                           'type': 'default'
                  }]
                
         
         if data['bar_code'] is not None and '/media/media/' in data['bar_code']:
               #  print('data:-====',data['bar_code'].split('/media/'))
                data['bar_code'] = 'http://127.0.0.1:8000/' + data['bar_code'].split('/media/')[1]
         return data
# Added above code on 05/06/2024


