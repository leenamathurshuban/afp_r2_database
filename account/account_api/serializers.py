from rest_framework import serializers
from account.models import (
    User,
    Role
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class CustomTokenSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.username
        token['email'] = user.email
        return token


class UserRegisterSerializer(serializers.ModelSerializer):
    role_uid  = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id','user_uid','username','first_name','last_name','email','phone_number','employee_number','profile_image','role_uid','password']
    
    def validate(self,attrs):

        get_username = attrs.get('username',None)
        get_first_name = attrs.get('first_name',None)
        get_last_name = attrs.get('last_name',None)
        get_role_uid = attrs.get('role_uid',None)
        get_phone_number = attrs.get('phone_number',None)
        get_employee_number = attrs.get('employee_number',None)
        get_password = attrs.get('password',None)
        get_profile_image = attrs.get('profile_image',None)


        if get_username is None or get_username == '':
            raise serializers.ValidationError({'error':'username field is required!'})

        if get_first_name is None or get_first_name == '':
            raise serializers.ValidationError({'error':'first_name field is required!'})

        if get_last_name is None or get_last_name == '':
            raise serializers.ValidationError({'error':'last_name field is required!'})

        if get_role_uid is None or get_role_uid == '':
            raise serializers.ValidationError({'error':'role_uid field is required!'})

        if get_phone_number is None or get_phone_number == '':
            raise serializers.ValidationError({'error':'phone_number field is required!'})

        if get_password is None or get_password == '':
            raise serializers.ValidationError({'error':'password field is required!'})
        
        if len(get_password) < 8:
            raise serializers.ValidationError({"Error":"Password must contain min 8 characters"})

        if get_profile_image is None or get_profile_image == '':
            raise serializers.ValidationError({'error':'profile_image field is required!'})
        
        return attrs


    def create(self,validated_data):

        role_obj = Role.objects.get(role_uid= validated_data['role_uid'])
        password = validated_data.pop('password', None)
        role_uid = validated_data.pop('role_uid', None)
        validated_data['user_role'] = role_obj

        instance = User(**validated_data)
        
        if password is not None:
            instance.set_password(password)
        instance.save()

        if instance.id:
            if instance.id <= 9:
                if not instance.afp_code:
                    instance.afp_code = 'AFP00' + str(instance.id)
            if instance.id >= 10:
                if not instance.afp_code:
                    instance.afp_code = 'AFP0' + str(instance.id)
            if instance.id >= 100:
                if not instance.afp_code:
                    instance.afp_code = 'AFP' + str(instance.id)
        instance.save()
        return instance
    

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id','role_uid','role_name','image','status']
    
    
    def validate(self, attrs):
       get_role_name = attrs.get('role_name',None)
       get_role_image = attrs.get('image',None)
       get_role_status = attrs.get('status',None)
       

       if get_role_name is None or get_role_name == '':
           raise serializers.ValidationError({'error':'role name is required'})
       
       if get_role_image is None or get_role_image == '':
           raise serializers.ValidationError({'error':'image field is required'}) 
       
       if get_role_status is None or get_role_status == '':
           raise serializers.ValidationError({'error':'status is required'})    
       return attrs
    
class RoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id','role_uid','role_name','image','status']

    

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','user_uid','username','first_name','last_name','email','user_role','phone_number','profile_image',
                  'employee_number','afp_code','created_at','updated_at']


