from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import (
    AllowAny
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from rest_framework_simplejwt.backends import TokenBackend

from account.models import (
    User,
    Role
)
from account.account_api.serializers import (
    CustomTokenSerializer,
    UserRegisterSerializer,
    UserUpdateSerializer,
    UserDetailSerializer,
    UserListSerializer,

    RoleSerializer,
    RoleUpdateSerializer,
    
    
)
from account.helpers import (
    get_exception_context,
    get_serializer_context,
)


class RegisterAPI(APIView):

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = UserRegisterSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return get_serializer_context(serializer.data)
            
            else:
                # serializer_error = [serializer.errors[error][0] for error in serializer.errors]
                return get_exception_context(serializer.errors)

        except Exception as exception:
            return get_exception_context(str(exception))


class LoginView(APIView):
    permission_classes  = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            get_username = request.data.get('username')
            get_password = request.data.get('password')

            if get_username is None or get_username == '':
                return get_exception_context('username field is required!')
            if get_password is None or get_password == '':
                return get_exception_context('password field is required!')
            
            try:
                get_user_obj = User.objects.get(username = get_username)
            except Exception as exception:
                return get_exception_context(str(exception))
            
            user = authenticate(username = get_username, password = get_password)

            if user is not None:
                token = CustomTokenSerializer().get_token(user)
                context = {
                    'status':status.HTTP_200_OK,
                    'success':True,
                    'refresh':str(token),
                    'access':str(token.access_token),
                    'user_uid':get_user_obj.user_uid,
                    'username':get_user_obj.username,
                }
                return Response(context,status=status.HTTP_200_OK)
            
            else:
                return get_exception_context('Invalid Password!')
        
        except Exception as exception:
            return get_exception_context(str(exception))


class UserUpdateView(APIView):
    def put(self, request,uid, *args, **kwargs):
        try:
            data = request.data
            get_user_obj = User.objects.get(user_uid= uid)

            serializer = UserUpdateSerializer(get_user_obj,data=data,context={'user':get_user_obj},partial=True)
            if serializer.is_valid():
                serializer.save()
                return get_serializer_context(serializer.data)
            else:
                # serializer_error = [serializer.errors[error][0] for error in serializer.errors]
                return get_exception_context(serializer.errors)

        except Exception as exception:
            return get_exception_context(str(exception))


class UserListView(ListAPIView):
    def get(self, request, *args, **kwargs):
        try:
            get_user_qs = User.objects.filter(is_superuser=False).select_related('user_role').order_by('id')
            serializer = UserListSerializer(get_user_qs,many=True)
            return get_serializer_context(serializer.data)

        except Exception as exception:
            return get_exception_context(str(exception))


# Worked on below code 26/05/2024 By Tasmiya

class RolePostApi(APIView):
    def post(self,request,*args,**kwargs):
        try:
            serializer =RoleSerializer(data=request.data)  
            if  serializer.is_valid():
                serializer.save()
                return get_serializer_context(serializer.data)      
            else:
                return get_exception_context(serializer.errors)

        except Exception as exception:
           return get_exception_context(str(exception))
# Worked on above code 27/05/2024 By Tasmiya

        
# Worked on below code 26/05/2024 By Tasmiya      
class RoleUpdateApi(APIView):
    def put(self, request,*args,**kwargs):
        
        uuid = kwargs.get('uid', None)
        print("uuid===",uuid)     
        try:
            get_role = Role.objects.get(role_uid=uuid)
            serializer = RoleUpdateSerializer(get_role,data=request.data,partial=True)
            if  serializer.is_valid():
                serializer.save()
                # serializer_error = [serializer.errors[error][0] for error in serializer.errors]
                return get_serializer_context(serializer.data)
            else:
                return get_exception_context(serializer.errors)
        except Exception as exception:
            return get_exception_context(str(exception))
# Worked on above code 27/05/2024 By Tasmiya
            
# Worked on below code 27/05/2024 By Tasmiya  
class RoleGetApi(APIView):

    def get(self,request):
        try:
            get_role = Role.objects.all().order_by('-id')
            serializer = RoleSerializer(get_role,many=True)
            return get_serializer_context(serializer.data)      
        except Exception as exception:
            return get_exception_context(str(exception))
# Worked on above code 27/05/2024 By Tasmiya

# Worked on below code 27/05/2024 By Tasmiya  
class RoleDeleteApi(APIView):

    def delete(self,request,*args,**kwargs):
        uuid = kwargs.get('uid', None)
        try:
            try:
                get_role = Role.objects.get(role_uid=uuid)
                get_role.delete()
                return get_serializer_context("Role Deleted Successfully !")
            except Exception as exception:
                return get_exception_context("Role matching query does not exist !") 
        except Exception as exception:
            return get_exception_context(str(exception))
# Worked on above code 27/05/2024 By Tasmiya

# Added below code on 06/06/2024
class RoleDetailView(APIView):
    
    def get(self,request,uid,*args, **kwargs):
        try:
            get_role = Role.objects.get(role_uid=uid)
            serializer = RoleSerializer(get_role)
            return get_serializer_context(serializer.data) 

        except Exception as exception:
            return get_exception_context(str(exception))
# Added above code on 06/06/2024

# Worked on below code 27/05/2024 By Tasmiya  
class UserdetailApi(APIView):
    def get(self,request,**kwargs):
        uuid = kwargs.get('uid', None)
        try:
            try:
                get_object = User.objects.select_related('user_role').get(user_uid=uuid)
                serializer = UserDetailSerializer(get_object)
                return get_serializer_context(serializer.data)
            except Exception as exception:
                # serializer_error = [serializer.errors[error][0] for error in serializer.errors]
                return get_exception_context(serializer.errors)
        except Exception as exception:
             return get_exception_context(str(exception))
        
# Worked on above code 27/05/2024 By Tasmiya

# Worked on below code 27/05/2024 By Tasmiya  
class UserDeleteApi(APIView):
    def delete(self,request,*args,**kwargs):
        uuid = kwargs.get('uid', None)
        try:
            try:
                get_user = User.objects.get(user_uid=uuid)
                get_user.delete()
                return get_serializer_context('User Deleted Successfully !')
            except Exception as exception:
                return get_exception_context('User matching query does not exist !')           
        except Exception as exception:
                return get_exception_context(str(exception))

# Worked on above code 27/05/2024 By Tasmiya


            
        
