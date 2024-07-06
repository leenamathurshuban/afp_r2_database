from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from rest_framework_simplejwt.backends import TokenBackend

from account.models import (
    User,
    Role,
    UserRolePermission,
)
from account.account_api.serializers import (
    CustomTokenSerializer,
    UserRegisterSerializer,
    UserUpdateSerializer,
    UserDetailSerializer,
    UserListSerializer,
    UserLoginSerializer,

    RoleSerializer,
    RoleUpdateSerializer,
    RoleSerializerForLogin,
    
    
)
from account.helpers import (
    get_exception_context,
    get_serializer_context,
)
from account.helpers import get_user_from_token



class RegisterAPI(APIView):

    def post(self, request, *args, **kwargs):
        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_add=True,permission_module='user')
            if get_permission:

                data = request.data
                serializer = UserRegisterSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return get_serializer_context(serializer.data)
                
                else:
                    # serializer_error = [serializer.errors[error][0] for error in serializer.errors]
                    return get_exception_context(serializer.errors)
            else:
                return get_exception_context("Unauthorized access!")

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
                get_user_obj = User.objects.select_related('user_role').prefetch_related('user_role__role_permissions').get(username = get_username)
            except Exception as exception:
                return get_exception_context(str(exception))
            
            user = authenticate(username = get_username, password = get_password)

            if user is not None:
                token = CustomTokenSerializer().get_token(user)

                # Added below code on 28/06/2024
                serializer = UserLoginSerializer(get_user_obj,context = {'refresh':str(token),'access':str(token.access_token),})
                context = {
                    'status':status.HTTP_200_OK,
                    'success':True,
                    'response':serializer.data
                }
                # Added below code on 28/06/2024

                # context = {
                #     'status':status.HTTP_200_OK,
                #     'success':True,
                #     'refresh':str(token),
                #     'access':str(token.access_token),
                #     'user_uid':get_user_obj.user_uid,
                #     'username':get_user_obj.username,
                # }
                return Response(context,status=status.HTTP_200_OK)
            
            else:
                return get_exception_context('Invalid Password!')
        
        except Exception as exception:
            return get_exception_context(str(exception))


class UserUpdateView(APIView):
    def put(self, request,uid, *args, **kwargs):
        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_user_permission = UserRolePermission.objects.filter(role__role_name=role_name, can_update=True, permission_module='user')

            if get_user_permission:
                data = request.data
                get_user_obj = User.objects.get(user_uid= uid)

                serializer = UserUpdateSerializer(get_user_obj,data=data,context={'user':get_user_obj},partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return get_serializer_context(serializer.data)
                else:
                    # serializer_error = [serializer.errors[error][0] for error in serializer.errors]
                    return get_exception_context(serializer.errors)
            else:
                return get_exception_context("Unauthorized access!")

        except Exception as exception:
            return get_exception_context(str(exception))


class UserListView(ListAPIView):
    def get(self, request, *args, **kwargs):
        try:
            user = get_user_from_token(request)
            get_role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=get_role_name,can_list=True,permission_module='user')
            if get_permission:

                get_user_qs = User.objects.filter(is_superuser=False).select_related('user_role').order_by('id')
                serializer = UserListSerializer(get_user_qs,many=True)
                return get_serializer_context(serializer.data)
            else:
                return get_exception_context("Unauthorized access!")

        except Exception as exception:
            return get_exception_context(str(exception))


# Worked on below code 26/05/2024 By Tasmiya

class RolePostApi(APIView):
    
    def post(self,request,*args,**kwargs):
        try:
            user = get_user_from_token(request)
            get_role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=get_role_name,can_add=True,permission_module='role')
            if get_permission:

                serializer =RoleSerializer(data=request.data)  
                if  serializer.is_valid():
                    serializer.save()

                    if not UserRolePermission.objects.filter(role_id=serializer.data.get('id')).exists():
                        module_list = ['all', 'permissions', 'warehouse', 'role', 'user', 'product', 'product_check_in', 'product_check_out', 'user_activity_log']
                        create_permission = [
                            UserRolePermission(role_id=serializer.data.get('id'),permission_module=module) for module in module_list
                        ]
                        UserRolePermission.objects.bulk_create(create_permission)
                    return get_serializer_context(serializer.data)      
                else:
                    return get_exception_context(serializer.errors)
            else:
                return get_exception_context("Unauthorized access!")

        except Exception as exception:
           return get_exception_context(str(exception))
# Worked on above code 27/05/2024 By Tasmiya

        
# Worked on below code 26/05/2024 By Tasmiya      
class RoleUpdateApi(APIView):
    def put(self, request,*args,**kwargs):
        
        uuid = kwargs.get('uid', None)
        print("uuid===",uuid)     
        try:
            user = get_user_from_token(request)
            get_role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=get_role_name,can_update=True,permission_module='role')
            if get_permission:

                get_role = Role.objects.get(role_uid=uuid)
                serializer = RoleUpdateSerializer(get_role,data=request.data,partial=True)
                if  serializer.is_valid():
                    serializer.save()
                    # serializer_error = [serializer.errors[error][0] for error in serializer.errors]
                    return get_serializer_context(serializer.data)
                else:
                    return get_exception_context(serializer.errors)
            else:
                return get_exception_context("Unauthorized access!")
        except Exception as exception:
            return get_exception_context(str(exception))
# Worked on above code 27/05/2024 By Tasmiya
            
# Worked on below code 27/05/2024 By Tasmiya  
class RoleGetApi(APIView):
    
    def get(self,request):
        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_user_permission = UserRolePermission.objects.filter(role__role_name=role_name, can_list=True, permission_module='role')

            if get_user_permission:
                get_role = Role.objects.all().prefetch_related('role_permissions').order_by('-id')
                serializer = RoleSerializerForLogin(get_role,many=True)
                return get_serializer_context(serializer.data)

            else:
                return get_exception_context('Unauthorized access!')    
        except Exception as exception:
            return get_exception_context(str(exception))
# Worked on above code 27/05/2024 By Tasmiya

# Worked on below code 27/05/2024 By Tasmiya  
class RoleDeleteApi(APIView):

    def delete(self,request,*args,**kwargs):
        uuid = kwargs.get('uid', None)
        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_delete=True,permission_module='role')
            if get_permission:    
                try:
                    get_role = Role.objects.get(role_uid=uuid)
                    get_role.delete()
                    return get_serializer_context("Role Deleted Successfully !")
                except Exception as exception:
                    return get_exception_context("Role matching query does not exist !") 
            else:
                return get_exception_context('Unauthorized access!')
        except Exception as exception:
            return get_exception_context(str(exception))
# Worked on above code 27/05/2024 By Tasmiya

# Added below code on 06/06/2024
class RoleDetailView(APIView):
    
    def get(self,request,uid,*args, **kwargs):
        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_list=True,permission_module='role')
            if get_permission:   
                get_role = Role.objects.get(role_uid=uid)
                serializer = RoleSerializerForLogin(get_role)
                return get_serializer_context(serializer.data) 
            else:
                return get_exception_context('Unauthorized access!')
        except Exception as exception:
            return get_exception_context(str(exception))
# Added above code on 06/06/2024

# Worked on below code 27/05/2024 By Tasmiya  
class UserdetailApi(APIView):
    def get(self,request,**kwargs):
        uuid = kwargs.get('uid', None)
        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_list=True,permission_module='user')
            if get_permission:
                get_object = User.objects.select_related('user_role').get(user_uid=uuid)
                serializer = UserDetailSerializer(get_object)
                return get_serializer_context(serializer.data)
            else:
                return get_exception_context('Unauthorized access!')
        except Exception as exception:
             return get_exception_context(str(exception))
        
# Worked on above code 27/05/2024 By Tasmiya

# Worked on below code 27/05/2024 By Tasmiya  
class UserDeleteApi(APIView):
    def delete(self,request,*args,**kwargs):
        uuid = kwargs.get('uid', None)
        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_delete=True,permission_module='user')
            if get_permission:
                try:
                    get_user = User.objects.get(user_uid=uuid)
                    get_user.delete()
                    return get_serializer_context('User Deleted Successfully !')
                except Exception as exception:
                    return get_exception_context('User matching query does not exist !')  
            else:
                return get_exception_context('Unauthorized access!')

        except Exception as exception:
                return get_exception_context(str(exception))

# Worked on above code 27/05/2024 By Tasmiya


# Added below code on 02/07/2024
def get_obj(i,role_uid):
    try:
        obj = UserRolePermission.objects.get(uid=i['uid'],role__role_uid=role_uid)
        obj.can_add=i['can_add'] if 'can_add' in i else obj.can_add
        obj.can_update=i['can_update'] if 'can_update' in i else obj.can_update
        obj.can_list=i['can_list'] if 'can_list' in i else obj.can_list
        obj.can_delete=i['can_delete'] if 'can_delete' in i else obj.can_delete
        obj.can_do_all=i['can_do_all'] if 'can_do_all' in i else obj.can_do_all
        obj.can_assign_permission=i['can_assign_permission'] if 'can_assign_permission' in i else obj.can_assign_permission
        obj.can_list_log=i['can_list_log'] if 'can_list_log' in i else obj.can_list_log
        obj.save()

        if UserRolePermission.objects.filter(role__role_name = obj.role.role_name,can_do_all=True,permission_module='all').exists():
            get_qs = UserRolePermission.objects.filter(role__role_name = obj.role.role_name).update(
                    can_do_all = True,can_add = True,
                    can_update = True,can_delete = True,
                    can_list = True,can_assign_permission=True,can_list_log=True
                    )
        
        context = {
            'status':status.HTTP_200_OK,
            'success':True,
            'response':"Permissions Updated Successfully!"
        }
        return context

    except UserRolePermission.DoesNotExist:
        context = {
            'status':status.HTTP_400_BAD_REQUEST,
            'success':False,
            'response':"Permission Module does not exist!"
        }
        return context

class UpdateRolePermissions(APIView):

    def put(self, request, role_uid, *args, **kwargs):
        try:
            # user = get_user_from_token(request)
            # role_name = user.user_role.role_name
            # get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_update=True,permission_module='permissions')
            # if get_permission: 
            lst = [get_obj(i,role_uid) for i in request.data['data']]
            context = {
                'status':status.HTTP_200_OK,
                'success':True,
                'response':None
            }
            if len(lst) > 0:
                context['response'] = 'Permissions Updated Successfully!'
            return Response(context)
            # else:
            #     return get_exception_context('Unauthorized access!')
        
        except Exception as exception:
            return get_exception_context(str(exception))
# Added above code on 02/07/2024

