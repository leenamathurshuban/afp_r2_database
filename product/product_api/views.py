from django.shortcuts import render
from account.helpers import (
    get_exception_context,
    get_serializer_context,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from product.models import (
    WareHouse,
    Product,
    ProductImage,
    WipingQuestionnaire,
    ProductCheckOut,
)
from account.models import (
    User,
    UserRolePermission
)
from product.product_api.serializers import (
    WareHouseSerializer,
    UpdateWareHouseSerializer,

    ProductSerializer,
    ProductUpdateSerializer,
    ProductdetailSerializer,
    GetProductListSerializer,

    WipingQuestionSerializer,
    WipingQuestionUpdateSerializer,
    WipingQuestionGetSerializer,

    ProductCheckOutSerializer,
    ProductCheckOutUpdateSerializer,
    ProductCheckoutGetSerializer,

    ProductSerializerForMultipleProduct,
    DashBoardSerializer
)
from account.models import (
    User
)

import uuid
import barcode
from barcode.writer import ImageWriter
from account.helpers import get_user_from_token

from rest_framework import viewsets
from rest_framework import filters as search_fil 
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import (
    ProductFilter,
    WareHouseFilter
)
from django.core.paginator import Paginator


# Create your views here.
# Worked on below code 27/05/2024 By Tasmiya

class PostWareHouse(APIView):
   
    def post(self,request,*args,**kwargs):
        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_add=True,permission_module='warehouse')
            if get_permission:
                data = request.data
                serializer = WareHouseSerializer(data=data)
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
    
 
class UpdateWareHouse(APIView):

    def put(self, request,uid,*args,**kwargs):
        uuid = kwargs.get('uid',None)
        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_update=True,permission_module='warehouse')
            if get_permission:
                get_warehouse = WareHouse.objects.get(warehouse_uid=uuid)
                serializer = WareHouseSerializer(get_warehouse,data=request.data,partial=True)
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


class GetWareHouseList(viewsets.ModelViewSet):
    serializer_class = WareHouseSerializer
    queryset = WareHouse.objects.all().order_by('-id')
    filter_backends = (DjangoFilterBackend,search_fil.SearchFilter)
    # filterset_class = WareHouseFilter 
    search_fields = ['warehouse_name']
    
    def list(self,request,*args,**kwargs):
        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_list=True,permission_module='warehouse')
            if get_permission:
                page = request.GET.get('page',1)
                limit = request.GET.get('limit',10)
                queryset = self.filter_queryset(self.get_queryset())
                paginator = Paginator(queryset,limit)
                get_page = paginator.page(page)
                total_page = paginator.num_pages
                serializer =WareHouseSerializer(get_page,many=True)
                context = {
                    'status':status.HTTP_200_OK,
                    'success': True,
                    'current_page':page,
                    'total_page':total_page,
                    'next_page':False if int(page)==total_page else True,
                    'response':serializer.data
                }
                return Response(context,status=status.HTTP_200_OK)
            else:
                return get_exception_context("Unauthorized access!")
        
        except Exception as exception:
            return get_exception_context(str(exception))
        
 
class DeleteWareHouse(APIView):  
    def delete(self,request,uid,*args,**kwargs):
        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_delete=True,permission_module='warehouse')
            if get_permission:
                try:
                    get_warehouse = WareHouse.objects.get(uid=uid)
                    get_warehouse.delete()
                    return get_serializer_context('Ware House Deleted Successfully !')
                except Exception as exception:
                    return get_exception_context('Ware House matching query does not exist !')
            else:
                return get_exception_context("Unauthorized access!")
        except Exception as exception:
            return get_exception_context(str(exception))
        

class DetailWareHouse(APIView):
    def get(self,request,uid,*args,**kwargs):
        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_list=True,permission_module='warehouse')
            if get_permission:
                get_warehouse = WareHouse.objects.get(uid=uid)
                serializer = WareHouseSerializer(get_warehouse)
                return get_serializer_context(serializer.data)
            else:
                return get_exception_context("Unauthorized access!")
        except Exception as exception:
             return get_exception_context(str(exception))

# Worked on above code 27/05/2024 By Tasmiya


# class ProductPostApi(APIView):
#     def post(self,request,*args,**Kwargs):
#         try:
#             get_warehouse = request.data.get('warehouse_uid',None)
#             if get_warehouse is None or get_warehouse == '':
#                 return get_exception_context({'warehouse_uid':['warehouse_uid is required']})

#             request.data._mutable = True
#             get_warehouse=WareHouse.objects.get(uid=request.data['warehouse_uid'])

#             get_super_user_for_testing = User.objects.get(is_superuser=True)
#             request.data['warehouse'] = get_warehouse.id
#             request.data['created_by'] = get_super_user_for_testing.id
#             request.data._mutable = False

#             get_product_image = request.FILES.getlist('product_image')

#             serializer = ProductSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()

#                 get_product_id = serializer.data.get('id')

#                 # Added below code on 20/06/2024
#                 serial_number = serializer.data.get('serial_number')
#                 get_barcode_name = f'AFP{serial_number}{get_product_id}'
#                 from barcode.writer import ImageWriter
#                 import uuid

#                 ean = barcode.codex.Code128(get_barcode_name, writer=ImageWriter())
#                 unique_filename = uuid.uuid4()

#                 get_product_obj = Product.objects.get(id=get_product_id)
#                 get_product_obj.bar_code = ean.save(f'media/bar_code/{unique_filename}')
#                 get_product_obj.bar_code_number = get_barcode_name
#                 get_product_obj.save()
#                 # Added above code on 20/06/2024

#                 if get_product_image:
#                     for image in get_product_image:
#                         create_image_obj = ProductImage.objects.create(product_id=get_product_id, image=image, type='uploaded')
#                 # else:
#                 #     create_image_obj = ProductImage.objects.create(product_id=get_product_id, image='product_image/default_product_image.jpg', type='default')

#                 return get_serializer_context(serializer.data)
#             else:
#                 return get_exception_context(serializer.errors)
            
#         except Exception as exception:
#             return get_exception_context(str(exception))

class ProductPostApi(APIView):
    def post(self,request,*args,**Kwargs):
        try:
            # user = get_user_from_token(request)
            # role_name = user.user_role.role_name
            # get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_add=True,permission_module='product')
            # if get_permission:
            get_warehouse = request.data.get('warehouse_uid',None)
            if get_warehouse is None or get_warehouse == '':
                return get_exception_context({'warehouse_uid':['warehouse_uid is required']})

            request.data._mutable = True
            get_warehouse=WareHouse.objects.get(uid=request.data['warehouse_uid'])

            get_super_user_for_testing = User.objects.get(is_superuser=True)
            request.data['warehouse'] = get_warehouse.id
            request.data['created_by'] = get_super_user_for_testing.id
            request.data._mutable = False

            get_product_image = request.FILES.getlist('product_image')

            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                get_product_id = serializer.data.get('id')

                # Added below code on 20/06/2024
                serial_number = serializer.data.get('serial_number')
                get_barcode_name = f'AFP{serial_number}{get_product_id}'
                ean = barcode.codex.Code128(get_barcode_name, writer=ImageWriter())
                unique_filename = uuid.uuid4()

                get_product_obj = Product.objects.get(id=get_product_id)
                get_product_obj.bar_code = ean.save(f'media/bar_code/{unique_filename}')
                get_product_obj.bar_code_number = get_barcode_name
                get_product_obj.save()
                # Added above code on 20/06/2024
                
                if get_product_image:
                    for image in get_product_image:
                        create_image_obj = ProductImage.objects.create(product_id=get_product_id, image=image, type='uploaded')
                # else:
                #     create_image_obj = ProductImage.objects.create(product_id=get_product_id, image='product_image/default_product_image.jpg', type='default')

                return get_serializer_context(serializer.data)
            else:
                return get_exception_context(serializer.errors)
            # else:
            #     return get_exception_context("Unauthorized access!")
                
        except Exception as exception:
            return get_exception_context(str(exception))


# class GetProductListAPI(APIView):

#     def get(self, request, *args, **kwargs):
#         try:
#             get_product_qs = Product.objects.all().select_related('warehouse','created_by').prefetch_related('product_image').order_by('-id')
#             serializer = GetProductListSerializer(get_product_qs, many=True)
#             return get_serializer_context(serializer.data)
            
#         except Exception as exception:
#             return get_exception_context(str(exception))

from barcode.writer import ImageWriter
class generate_barcode(APIView):
    
    def get(self, request, *args, **kwargs):
        # Make sure to pass the number as string 
        number ="AFP0002-af9b425c"

        # barcode_writer = ImageWriter()
        from django.conf import settings
        import os

        ean = barcode.codex.Code128(number, writer=ImageWriter())

        # unique_filename = uuid.uuid4()

        get_product_obj = Product.objects.get(uid='af9b425c-f730-41cd-a352-b009cedde80c')

        get_product_obj.bar_code = ean.save('media/bar_code/ayan17')
        get_product_obj.save()
        
        # Now, let's create an object of EAN13 
        # class and pass the number 
        # my_code = Code128(number)
        
        # Our barcode is ready. Let's save it. 
        # file = my_code.save("new")

        return Response('filename')


class GetProductListAPI(viewsets.ModelViewSet):
    serializer_class = GetProductListSerializer
    queryset =  Product.objects.all().select_related('warehouse','created_by').prefetch_related('product_image').order_by('-id')
    filter_backends = (DjangoFilterBackend,search_fil.SearchFilter)
    filterset_class = ProductFilter
    search_fields = ['serial_number','device_type']
   
    def list(self, request, *args, **kwargs):
        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_list=True,permission_module='product')
            if get_permission:
                page = request.GET.get('page', 1)
                limit = request.GET.get('limit',10)
                queryset = self.filter_queryset(self.get_queryset())
                paginator = Paginator(queryset,limit)
                queryset = paginator.page(page)
                total_page = paginator.num_pages
                serializer = self.serializer_class(queryset, many=True)
                context = {
                    'status':status.HTTP_200_OK,
                    'success':True,
                    'current_page':page,
                    'total_page':total_page,
                    'next_page':False if int(page)== total_page else True,
                    'response':serializer.data
                }
                return Response(context, status=status.HTTP_200_OK)
            else:
                return get_exception_context("Unauthorized access!")
            
        except Exception as exception:
            return get_exception_context(str(exception)) 

    
class ProductDeleteApi(APIView):

    def delete(self,request,uid,*args,**kwargs):
        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_delete=True,permission_module='product')
            if get_permission:
                try:
                    get_product = Product.objects.get(uid=uid)
                    get_product.delete()
                    return get_serializer_context("Product Delete Successfully!")
                except Exception as exception:
                    return get_exception_context('Product does not exist!')
            else:
                return get_exception_context("Unauthorized access!")
        except Exception as exception:
            return get_exception_context(str(exception))
    
class ProductUpdateApi(APIView):
    def put(self,request,uid,*args,**kwargs):

        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_update=True,permission_module='product')
            if get_permission:
                get_product = Product.objects.get(uid=uid)
                get_data = request.data.get('warehouse_uid',None)
                if get_data:
                    request.data._mutable = True
                    get_warehouse=WareHouse.objects.get(uid=request.data['warehouse_uid'])   
                    request.data['warehouse'] = get_warehouse.id
                    request.data._mutable = False
                get_product_image = request.FILES.getlist('product_image')
                serializer = ProductUpdateSerializer(get_product,request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    get_product_id = serializer.data.get('id')

                    if get_product_image:
                        for image in get_product_image:
                            create_image_obj = ProductImage.objects.create(product_id=get_product_id, image=image,type='uploded')
                            get_obj = ProductImage.objects.get(product=get_product_id,type='default')
                            print('get_obj====',get_obj)
                            get_obj.delete()
    
                    return get_serializer_context(serializer.data)
                else:
                    return get_exception_context(serializer.errors)
            else:
                return get_exception_context("Unauthorized access!")
            
        except Exception as exception:
            return get_exception_context(str(exception))
        
class ProductDetailApi(APIView):
    def get(self,request,uid,*args,**kwargs):
        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_list=True,permission_module='product')
            if get_permission:
                get_product = Product.objects.select_related('warehouse','created_by').prefetch_related('wiping_product','product_checkout','product_image').get(uid=uid)
                serializer = ProductdetailSerializer(get_product)
                return get_serializer_context(serializer.data) 
            else:
                return get_exception_context("Unauthorized access!")
        except Exception as exception:
            return get_exception_context(str(exception))

        
class ProductImageDeleteApi(APIView):
    def delete(self,request,uid,*args,**kwargs):
        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_delete=True,permission_module='product')
            if get_permission:
                try:
                    get_obj = ProductImage.objects.get(uid=uid)
                    get_obj.delete()
                    return get_serializer_context("Product Image Deleted!")
                except Exception as exception:
                    return get_exception_context("Image Not Found")
            else:
                return get_exception_context("Unauthorized access!")
        except Exception as exception:
            return get_exception_context(str(exception))

# Worked on below code 13/06/2024 By Tasmiya

class WipingQuestionsPostApi(APIView):
    def post(self,request,*args,**kwargs):
        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_add=True,permission_module='product_check_in')
            if get_permission:
                get_product = request.data.get('product_uid',None)
                # print('get_product====',get_product)
                if get_product is None or get_product == '':
                    return get_exception_context({'product_uid':['product_uid is required']})
                request.data._mutable = True
                get_product = Product.objects.get(uid=request.data['product_uid'])
                request.data['product'] = get_product.id
                request.data._mutable = False
                serializer = WipingQuestionSerializer(data=request.data)
                if serializer.is_valid():
                    get_product.product_status = 'CHECKED-IN'
                    get_product.save()
                    serializer.save()
                    return get_serializer_context(serializer.data)
                else:
                    return get_exception_context(serializer.errors)
            else:
                return get_exception_context("Unauthorized access!")
            
        except Exception as exception:
            return get_exception_context(str(exception))
        

class WipingQuestionsUpdateApi(APIView):
    def put(self,request,uid,*args,**kwargs):
        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_update=True,permission_module='product_check_in')
            if get_permission:
                get_wiped = WipingQuestionnaire.objects.get(uid=uid)
                get_product = request.data.get('product_uid',None)
                if get_product:
                    request.data._mutable = True
                    get_product_obj = Product.objects.get(uid=request.data['product_uid'])
                    request.data['product'] = get_product_obj.id
                    request.data._mutable = False
                serializer = WipingQuestionUpdateSerializer(get_wiped,data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return get_serializer_context(serializer.data)
                else:
                    return get_exception_context(serializer.errors)
            else:
                return get_exception_context("Unauthorized access!")
        except Exception as exception:
            return get_exception_context(str(exception))
            
            
class WipingQuestionsGetApi(APIView):
    def get(self,request,uid,*args,**kwargs):
        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_list=True,permission_module='product_check_in')
            if get_permission:
                try:
                    get_wiped = WipingQuestionnaire.objects.select_related('product').get(uid=uid)
                    serializer = WipingQuestionGetSerializer(get_wiped)
                    return get_serializer_context(serializer.data)
                except Exception as exception:
                    return get_exception_context('Device Data Wiping Does Not Exist')   
            else:
                return get_exception_context("Unauthorized access!")   
        except Exception as exception:
            return get_exception_context(str(exception))
        
class WipingQuestionsDeleteApi(APIView):
    def delete(self,request,uid,*args,**kwargs):
        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_delete=True,permission_module='product_check_in')
            if get_permission:
                try:
                    get_wiped = WipingQuestionnaire.objects.get(uid=uid)
                    get_wiped.delete()
                    return get_serializer_context('Device Data Wiping Deleted Successfully')
                except Exception as exception:
                    return get_exception_context('Device Data Wiping Does Not Exist')
            else:
                return get_exception_context("Unauthorized access!")   
        except Exception as exception:
            return get_exception_context(str(exception))
        
class WipingQuestionListApi(APIView):
    def get(self,request,*args,**kwargs):
        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_list=True,permission_module='product_check_in')
            if get_permission:
                try:           
                    get_wiped = WipingQuestionnaire.objects.filter(product__product_status='CHECKED-IN').select_related('product').order_by('-id')
                    serializer = WipingQuestionGetSerializer(get_wiped,many=True)
                    return get_serializer_context(serializer.data)
                except Exception as exception:
                    return get_exception_context(serializer.errors)  
            else:
                return get_exception_context("Unauthorized access!")       
        except Exception as exception:
            return get_exception_context(str(exception))
        
# Worked on above code 27/05/2024 By Tasmiya


# Worked on below code 14/06/2024 By Tasmiya

class ProductCheckOutPostApi(APIView):

    def post(self,request,*args,**kwargs):
        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_add=True,permission_module='product_check_out')
            if get_permission:
                get_product = request.data.get('product_uid',None)
                if get_product is None or get_product == '':
                    return get_exception_context({'product_uid':['product_uid is required']})
                request.data._mutable = True
                get_obj = Product.objects.get(uid=request.data['product_uid'])
                request.data['product'] = get_obj.id
                request.data._mutable = False
                serializer = ProductCheckOutSerializer(data=request.data)
                if serializer.is_valid():
                    get_obj.product_status = 'CHECKED-OUT'
                    get_obj.save()
                    serializer.save()        
                    return get_serializer_context(serializer.data)
                else:
                    return get_exception_context(serializer.errors)
            else:
                return get_exception_context("Unauthorized access!")  
        except Exception as exception:
            return get_exception_context(str(exception))
            

class ProductCheckOutUpdateApi(APIView):
    def put(self,request,uid,*args,**kwargs):
        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_update=True,permission_module='product_check_out')
            if get_permission:
                get_product_checkout = ProductCheckOut.objects.get(uid=uid)
                get_product = request.data.get('product_uid',None)
                if get_product:
                    request.data._mutable = True
                    get_product_obj  = Product.objects.get(uid=request.data['product_uid'])
                    request.data['product'] = get_product_obj.id
                    request.data._mutable = False
                serializer = ProductCheckOutUpdateSerializer(get_product_checkout,data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return get_serializer_context(serializer.data)
                else:
                    return get_exception_context(serializer.errors)
            else:
                return get_exception_context("Unauthorized access!")  
            
        except Exception as exception:
            return get_exception_context(str(exception))
        
class ProductCheckOutGetApi(APIView):
    def get(self,request,uid,*args,**kwargs):
        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_list=True,permission_module='product_check_out')
            if get_permission:
                get_product_checkout = ProductCheckOut.objects.select_related('product').get(uid=uid)
                serializer = ProductCheckoutGetSerializer(get_product_checkout)
                return get_serializer_context(serializer.data)
            else:
                return get_exception_context("Unauthorized access!")  
        except Exception as exception:
            return get_exception_context(str(exception))
            

class ProductCheckOutListApi(APIView):
    def get(self,request,*args,**kwargs):
        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_list=True,permission_module='product_check_out')
            if get_permission:
                get_obj = ProductCheckOut.objects.filter(product__product_status='CHECKED-OUT').select_related('product').order_by('-id')
                serializer = ProductCheckoutGetSerializer(get_obj,many=True)
                return get_serializer_context(serializer.data)
            else:
                return get_exception_context("Unauthorized access!")  
        except Exception as exception:
            return get_exception_context(str(exception))
        
class ProductCheckOutDeleteApi(APIView):
    def delete(self,request,uid,*args,**kwargs):
        try:
            user = get_user_from_token(request)
            role_name = user.user_role.role_name
            get_permission = UserRolePermission.objects.filter(role__role_name=role_name,can_delete=True,permission_module='product_check_out')
            if get_permission:
                try:
                    get_obj = ProductCheckOut.objects.get(uid=uid)
                    get_obj.delete()
                    return get_serializer_context('Product CheckOut Deleted Successfully!')
                except Exception as exception:
                    return get_exception_context('Product CheckOut does not exist!')
            else:
                return get_exception_context("Unauthorized access!")  
        except Exception as exception:
            return get_exception_context(str(exception))
        
# Worked on above code 14/06/2024 By Tasmiya

# Added below code on 21/06/2024
class GetProductDetailByBarCodeAPI(APIView):
    def get(self,request,bar_code_number,*args,**kwargs):
        try:
            get_barcode_product = Product.objects.select_related('warehouse','created_by').prefetch_related('wiping_product','product_checkout','product_image').get(bar_code_number=bar_code_number)
            serializer = ProductdetailSerializer(get_barcode_product)
            return get_serializer_context(serializer.data) 
        except Exception as exception:
            return get_exception_context(str(exception))
# Added above code on 21/06/2024


class MultipleProductForDetailApi(generics.ListAPIView):
     serializer_class = ProductdetailSerializer

     def get_queryset(self):
        # uids = self.request.data.getlist('uid', [])
        uids = self.request.query_params.getlist('uid',[])
        print('uid====',uids)
        return Product.objects.filter(uid__in=uids).select_related('warehouse','created_by').prefetch_related('wiping_product','product_checkout','product_image')
     def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            return get_serializer_context(serializer.data)  
        except Exception as exception:
            return get_exception_context(str(exception)) 
        

# class Multipleproductget(APIView):
#     def get(self,request,*args,**kwargs):
#         try:
#             uids = request.data.getlist('uid',None)
#             uids =self.request.query_params.get('uid',[])
#             print('uid===',uids)
#             get_obj = Product.objects.filter(uid__in=uids).select_related('warehouse','created_by').prefetch_related('wiping_product','product_checkout','product_image')
#             print('get-obj====',get_obj)
#             serializer = ProductSerializerForMultipleProduct(get_obj,many=True)
#             return get_serializer_context(serializer.data)
#         except Exception as exception:
#             return get_exception_context(str(exception))

from django.db.models import Count

class DashBoardAPI(APIView):
      def get(self, request):
        try:
          total_number_of_user = User.objects.all().count()
          total_nubmer_of_product = Product.objects.all().count()
          total_check_out_product = Product.objects.filter(product_status='CHECKED-OUT').count()
          total_check_in_product = Product.objects.filter(product_status='CHECKED-IN').count()
          context = {
              'total_number_of_user':total_number_of_user,
              'total_nubmer_of_product':total_nubmer_of_product,
              'total_check_out_product':total_check_out_product,
              'total_check_in_product':total_check_in_product
          }
          return get_serializer_context(context)
        except Exception as exception:
            return get_exception_context(str(exception))



          