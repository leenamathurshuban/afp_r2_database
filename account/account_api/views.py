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
from rest_framework_simplejwt.backends import TokenBackend  #17/07/2023

from account.models import (
    User,
    Role
)
from account.account_api.serializers import (
    CustomTokenSerializer,
    UserRegisterSerializer,
    RoleSerializer,
    UserDetailSerializer,
    RoleUpdateSerializer
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
                serializer_error = [serializer.errors[error][0] for error in serializer.errors]
                return get_exception_context(serializer_error)

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
        
# Worked on below code 26/05/2024 By Tasmiya
class RolePostApi(APIView):
    def post(self,request,*args,**kwargs):
        try:
            serializer =RoleSerializer(data=request.data)  
            if not serializer.is_valid():
                context = {
                    'status':status.HTTP_400_BAD_REQUEST,
                    'success':False,
                    'response':serializer.errors
                }
                return Response(context,status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            context = {
                'status':status.HTTP_200_OK,
                'success':True,
                'response':serializer.data
            }
            return Response(context,status=status.HTTP_200_OK)
        except Exception as exception:
           
           context = {
                    'status':status.HTTP_400_BAD_REQUEST,
                    'success':False,
                    'response':str(exception)
            }
           return Response(context,status=status.HTTP_400_BAD_REQUEST)
# Worked on above code 27/05/2024 By Tasmiya

        
# Worked on below code 26/05/2024 By Tasmiya      
class RoleUpdateApi(APIView):
    def put(self, request,*args,**kwargs):
        
        uuid = kwargs.get('uid', None)
        print("uuid===",uuid)
        if uuid:       
            try:
                get_role = Role.objects.get(role_uid=uuid)
                serializer = RoleUpdateSerializer(get_role,data=request.data,partial=True)
                if not serializer.is_valid():
                    context = {
                        'status':status.HTTP_400_BAD_REQUEST,
                        'success':False,
                        'response':serializer.errors
                    }
                    return Response(context,status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                context = {
                    'status':status.HTTP_200_OK,
                    'success':True,
                    'response':serializer.data
                }
                return Response(context,status=status.HTTP_400_BAD_REQUEST)
            except Exception as exception:
                context = {
                    'status':status.HTTP_400_BAD_REQUEST,
                    'success':False,
                    'response': str(exception)
                }
                return Response(context,status=status.HTTP_400_BAD_REQUEST)
# Worked on above code 27/05/2024 By Tasmiya
            
# Worked on below code 27/05/2024 By Tasmiya  
class RoleGetApi(APIView):

    def get(self,request):
        try:
            get_role = Role.objects.all()
            serializer = RoleSerializer(get_role,many=True)
            if serializer:
                context = {
                    'status':status.HTTP_200_OK,
                    'success':True,
                    'response':serializer.data
                }
                return Response(context,status=status.HTTP_200_OK)         
        except Exception as exception:
            context = {
                'status':status.HTTP_400_BAD_REQUEST,
                'success':False,
                'response':str(exception)
            }
            return Response(context,status=status.HTTP_400_BAD_REQUEST)
# Worked on above code 27/05/2024 By Tasmiya

# Worked on below code 27/05/2024 By Tasmiya  
class RoleDeleteApi(APIView):

    def delete(self,request,*args,**kwargs):
        uuid = kwargs.get('uid', None)
        try:
            get_role = Role.objects.get(role_uid=uuid)
            get_role.delete()
            context = {
                'status':status.HTTP_200_OK,
                'success':True,
                'response':"Role Deleted Successfully !"
            }
            return Response(context,status=status.HTTP_200_OK)
             
        except Exception as exception:
            context = {
                'status':status.HTTP_400_BAD_REQUEST,
                'success':True,
                'response':str(exception)
            }
            return Response(context,status=status.HTTP_400_BAD_REQUEST)
# Worked on above code 27/05/2024 By Tasmiya

# Worked on below code 27/05/2024 By Tasmiya  
class UserdetailApi(APIView):
    def get(self,request,**kwargs):
        uuid = kwargs.get('uid', None)
        try:
            try:
                get_object = User.objects.get(user_uid=uuid)
                serializer = UserDetailSerializer(get_object)
                return get_serializer_context(serializer.data)
            except Exception as exception:
                serializer_error = [serializer.errors[error][0] for error in serializer.errors]
                return get_exception_context(serializer_error)
        except Exception as exception:
             return get_exception_context(str(exception))
        
# Worked on above code 27/05/2024 By Tasmiya

# Worked on below code 27/05/2024 By Tasmiya  
class UserDeleteApi(APIView):
    def delete(self,request,*args,**kwargs):
        uuid = kwargs.get('uid', None)
        if uuid:
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


            
        