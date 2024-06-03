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
    UserListSerializer,
    RoleSerializer,
)
from account.helpers import (
    get_exception_context,
    get_serializer_context,
)



class RegisterAPI(APIView):

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = UserRegisterSerializer(data=data,context={'data':data})
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
                serializer_error = [serializer.errors[error][0] for error in serializer.errors]
                return get_exception_context(serializer_error)

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


class RolePostApi(APIView):
    def post(self,request,*args,**kwargs):
        try:
            serializer =RoleSerializer(data=request.data)  
            if not serializer.is_valid():
                serializer_error = [serializer.errors[error][0] for error in serializer.errors]
                context = {
                    'status':status.HTTP_400_BAD_REQUEST,
                    'success':False,
                    'response':serializer_error
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
        
class RoleUpdateApi(APIView):
    def put(self, request,*args,**kwargs):
        
        uuid = kwargs.get('uid', None)
        print("uuid===",uuid)
        if uuid:       
            try:
                get_role = Role.objects.get(role_uid=uuid)
                serializer = RoleSerializer(get_role,data=request.data,partial=True)
                if not serializer.is_valid():
                    serializer_error = [serializer.errors[error][0] for error in serializer.errors]
                    context = {
                        'status':status.HTTP_400_BAD_REQUEST,
                        'success':False,
                        'response':serializer_error
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
                    'response': str(exception)
                }
                return Response(context,status=status.HTTP_400_BAD_REQUEST)
            
class RoleGetApi(APIView):

    def get(self,request):
        try:
            get_role = Role.objects.all()
            serializer = RoleSerializer(get_role,many=True)
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

class RoleDeleteApi(APIView):

    def delete(self,request,*args,**kwargs):
        uuid = kwargs.get('uid', None)
        try:
            get_role = Role.objects.get(role_uid=uuid)
            get_role.delete()
            context = {
                'status':status.HTTP_200_OK,
                'success':True,
                'response':"Role Deleted Successfully!"
            }
            return Response(context,status=status.HTTP_200_OK)
             
        except Exception as exception:
            context = {
                'status':status.HTTP_400_BAD_REQUEST,
                'success':True,
                'response':str(exception)
            }
            return Response(context,status=status.HTTP_400_BAD_REQUEST)
