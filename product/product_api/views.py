from django.shortcuts import render
from account.helpers import (
    get_exception_context,
    get_serializer_context,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from product.models import (
    WareHouse,
    Product,
    ProductImage,
)
from account.models import (
    User
)
from product.product_api.serializers import (
    WareHouseSerializer,
    UpdateWareHouseSerializer,
    ProductSerializer,
    GetProductListSerializer,
)
import uuid
import barcode
from barcode.writer import ImageWriter


# Create your views here.
# Worked on below code 27/05/2024 By Tasmiya

class PostWareHouse(APIView): 

    def post(self,request,*args,**kwargs):
        try:
            data = request.data
            serializer = WareHouseSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return get_serializer_context(serializer.data)
            else:
                # serializer_error = [serializer.errors[error][0] for error in serializer.errors]
                return get_exception_context(serializer.errors)

        except Exception as exception:
            return get_exception_context(str(exception))
    
 
class UpdateWareHouse(APIView):    
    def put(self, request,uid,*args,**kwargs):
        uuid = kwargs.get('uid',None)
        try:
            get_warehouse = WareHouse.objects.get(warehouse_uid=uuid)
            serializer = WareHouseSerializer(get_warehouse,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return get_serializer_context(serializer.data)
            else:
                # serializer_error = [serializer.errors[error][0] for error in serializer.errors]
                return get_exception_context(serializer.errors)
        except Exception as exception:
            return get_exception_context(str(exception))


class GetWareHouseList(APIView):   
    def get(self,request,*args,**kwargs):
        try:
            get_warehouse = WareHouse.objects.all().order_by('-id')
            serializer =WareHouseSerializer(get_warehouse,many=True)
            return get_serializer_context(serializer.data)
            
        except Exception as exception:
            return get_exception_context(str(exception))
        
 
class DeleteWareHouse(APIView):  
    def delete(self,request,uid,*args,**kwargs):
        try:
            try:
                get_warehouse = WareHouse.objects.get(uid=uid)
                get_warehouse.delete()
                return get_serializer_context('Ware House Deleted Successfully !')
            except Exception as exception:
                return get_exception_context('Ware House matching query does not exist !')

        except Exception as exception:
            return get_exception_context(str(exception))
        

class DetailWareHouse(APIView):
    def get(self,request,uid,*args,**kwargs):
        try:
            get_warehouse = WareHouse.objects.get(uid=uid)
            serializer = WareHouseSerializer(get_warehouse)
            return get_serializer_context(serializer.data)
            
        except Exception as exception:
             return get_exception_context(str(exception))

# Worked on above code 27/05/2024 By Tasmiya


class ProductPostApi(APIView):
    def post(self,request,*args,**Kwargs):
        try:
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
                if get_product_image:
                    for image in get_product_image:
                        create_image_obj = ProductImage.objects.create(product_id=get_product_id, image=image, type='uploaded')
                # else:
                #     create_image_obj = ProductImage.objects.create(product_id=get_product_id, image='product_image/default_product_image.jpg', type='default')

                return get_serializer_context("Product Created Successfully!")
            else:
                return get_exception_context(serializer.errors)
            
        except Exception as exception:
            return get_exception_context(str(exception))


class GetProductListAPI(APIView):

    def get(self, request, *args, **kwargs):
        try:
            get_product_qs = Product.objects.all().select_related('warehouse','created_by').prefetch_related('product_image')
            serializer = GetProductListSerializer(get_product_qs, many=True)
            return get_serializer_context(serializer.data)
            
        except Exception as exception:
            return get_exception_context(str(exception))

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