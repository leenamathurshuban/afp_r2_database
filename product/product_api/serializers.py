from rest_framework import serializers
from django.db.models import Q
from product.models import (
    WareHouse,
    Product,
    ProductImage,
    WipingQuestionnaire
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
      fields = ['id','uid','product','image']

class ProductListSerializer(serializers.ModelSerializer):
   warehouse = WareHouseSerializer()
   created_by = UserListSerializerForProduct()
   product_image = ProductImageSerializer(many=True)

   class Meta:
      model = Product
      fields = '__all__'

   def to_representation(self, instance):
       data = super().to_representation(instance)
       if data['find_my_mac'] == True:
           data['find_my_mac'] = "Yes"
           
       if data['find_my_mac'] == False:
           data['find_my_mac'] = "No"
                
       if data['mdm'] == True:
           data['mdm'] = "Yes"

       if data['mdm'] == False:
           data['mdm'] = "No"

       return data


class ProductUpdateSerializer(serializers.ModelSerializer):
   warehouse = serializers.CharField()
   
   class Meta:
      model = Product
      fields = '__all__'

   # def update(self, instance, validated_data):

      
      # warehouse_obj = None
      # if validated_data.get('uid',None):
      #       warehouse_obj = WareHouse.objects.get(uid= validated_data['uid'])
      #       print('warehouse_obj====',warehouse_obj)
      #       validated_data.pop('uid')

      # instance.serial_number =validated_data.get('serial_number',instance.serial_number)
      # instance.year = validated_data.get('year',instance.year)
      # instance.product_size = validated_data.get('product_size',instance.product_size)
      # instance.device_type = validated_data.get('device_type',instance.device_type)
      # instance.product_status = validated_data.get('product_status',instance.product_status)
      # instance.model_number = validated_data.get('model_number',instance.model_number)
      # instance.emc_number = validated_data.get('emc_number',instance.emc_number)
      # instance.model_family = validated_data.get('model_family',instance.model_family)
      # instance.memory = validated_data.get('memory',instance.memory)
      # instance.storage_type =validated_data.get('storage_type',instance.storage_type)
      # instance.storage_size = validated_data.get('storage_size',instance.storage_size)
      # instance.battery_capacity = validated_data.get('battery_capacity',instance.battery_capacity)
      # instance.battery_cycles = validated_data.get('battery_cycles',instance.battery_cycles)
      # instance.grade = validated_data.get('grade',instance.grade)
      # instance.grade_notes = validated_data.get('grade_notes',instance.grade_notes)
      # instance.technical_notes = validated_data.get('technical_notes',instance.technical_notes)
      # instance.track_pad = validated_data.get('track_pad',instance.track_pad)
      # instance.keyboard = validated_data.get('keyboard',instance.keyboard)
      # instance.lcd_ghost_peel = validated_data.get('lcd_ghost_peel',instance.lcd_ghost_peel)
      # instance.headphone_jack = validated_data.get('headphone_jack',instance.headphone_jack)
      # instance.microphone = validated_data.get('microphone',instance.microphone)
      # instance.usb_port = validated_data.get('usb_port',instance.usb_port)
      # instance.bluetooth_wifi = validated_data.get('bluetooth_wifi',instance.bluetooth_wifi)
      # instance.face_time_camera = validated_data.get('face_time_camera',instance.face_time_camera)
      # instance.find_my_mac = validated_data.get('find_my_mac',instance.find_my_mac)
      # instance.mdm = validated_data.get('mdm',instance.mdm)
      # instance.warehouse = validated_data.get('warehouse')
      # print('instance.warehouse=====',instance.warehouse.uid)
      # instance.save()

      # if 'warehouse' in validated_data:
      #    get_warehouse = self.fields['warehouse']
      #    print('get_warehouse====',get_warehouse)
      #    instance = instance.warehouse.uid
      #    data =validated_data.pop('warehouse')
      #    get_warehouse.update(instance,data)
      # warehouse_uid  = validated_data.pop('warehouse') 
      # print('warehouse_uid====',warehouse_uid)
      # instance.warehouse_name = validated_data.get('warehouse_name',None)
      
      
         
      # return instance
   

class ProductdetailSerializer(serializers.ModelSerializer):
      warehouse = WareHouseSerializer()
      created_by = UserListSerializerForProduct()
      product_image = ProductImageSerializer(many=True)

      class Meta:
         model = Product
         fields = '__all__'

      def to_representation(self, instance):
       data = super().to_representation(instance)
       if data['find_my_mac'] == True:
           data['find_my_mac'] = "Yes"
           
       if data['find_my_mac'] == False:
           data['find_my_mac'] = "No"
                
       if data['mdm'] == True:
           data['mdm'] = "Yes"

       if data['mdm'] == False:
           data['mdm'] = "No"

       if len(data['product_image']) == 0:
             data['product_image'] = [{
                        'id': 'test', 
                        'uid': 'test', 
                        'product': 'test',
                        'image': '/media/product_image/default_product_image.jpg', 
                        'type': 'default'
                }]
           
       return data



class GetProductListSerializer(serializers.ModelSerializer):
    warehouse = WareHouseSerializer()
    created_by = UserListSerializerForProduct()
    product_image = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
       data = super().to_representation(instance)
       if data['find_my_mac'] == True:
           data['find_my_mac'] = "Yes"
           
       if data['find_my_mac'] == False:
           data['find_my_mac'] = "No"
                
       if data['mdm'] == True:
           data['mdm'] = "Yes"

       if data['mdm'] == False:
           data['mdm'] = "No"
           
       return data
# Added above code on 05/06/2024

class WipingQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WipingQuestionnaire
        fields = '__all__'

    def validate(self, attrs):
        print('attrs====',attrs)
        get_data_wiped = attrs.get('data_wiped',None)
        get_software_used =attrs.get('software_used',None)
        get_software_reason = attrs.get('software_reason',None)
        get_first_name = attrs.get('first_name',None)
        get_last_name = attrs.get('last_name',None)

        if get_data_wiped is None:
            raise serializers.ValidationError({'error':'data_wiped is required'})
         
        if get_data_wiped == True:
            if get_software_used is None or get_software_used == '':
                raise serializers.ValidationError({'error':'software_used is required'})
            
        if get_data_wiped == False:
            if get_software_reason is None or get_software_reason == '':
                raise serializers.ValidationError({'error':'software_reason is required'})
            
        if get_first_name is None or get_first_name == '':
            raise serializers.ValidationError({'error':'first_name is required'})
        
        if get_last_name is None or get_last_name == '':
            raise serializers.ValidationError({'error':'last_name is rquired'})
        
        # datawiped1 = Q(data_wiped=True)
        # print('datawiped1====',datawiped1)
        # datawiped2 = Q(data_wiped=False)
        # print('datawiped2====',datawiped2)
        get_wiped = WipingQuestionnaire.objects.filter(product=attrs['product'],data_wiped=attrs['data_wiped'])
        print('get wiped===',get_wiped)
        
        if get_wiped.exists():
            raise serializers.ValidationError({'error':'Device Data Wiping Already Submitted'})
       
        return attrs
            

class WipingQuestionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WipingQuestionnaire
        fields = '__all__'

    def validate(self, attrs):
        get_data_wiped = attrs.get('data_wiped',None)
        get_software_used =attrs.get('software_used',None)
        get_software_reason = attrs.get('software_reason',None)

        if get_data_wiped == True:
            if get_software_used is None or get_software_used == '':
                raise serializers.ValidationError({'error':'software_used is required'})
            
        if get_data_wiped == False:
            if get_software_reason is None or get_software_reason == '':
                raise serializers.ValidationError({'error':'software_reason is required'})
        return attrs

class ProductSerializerForWiping(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','uid','serial_number','year','product_size','device_type','product_status']

class WipingQuestionGetSerializer(serializers.ModelSerializer):
    product = ProductSerializerForWiping()
    class Meta:
        model = WipingQuestionnaire
        fields = '__all__'
            




