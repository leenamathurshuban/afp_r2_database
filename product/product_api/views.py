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
    WipingQuestionnaire,
)
from account.models import (
    User
)
from product.product_api.serializers import (
    WareHouseSerializer,
    UpdateWareHouseSerializer,

    ProductSerializer,
    ProductListSerializer,
    ProductUpdateSerializer,
    ProductdetailSerializer,
    GetProductListSerializer,

    WipingQuestionSerializer,
    WipingQuestionUpdateSerializer,
    WipingQuestionGetSerializer,
)
from account.models import (

    User
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
                for image in get_product_image:
                    create_image_obj = ProductImage.objects.create(product_id=get_product_id, image=image)

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


class generate_barcode(APIView):
    
    def get(self, request, *args, **kwargs):
        # Make sure to pass the number as string 
        number = "AFP0002"
        ary = {}
        # barcode_writer = ImageWriter()

        ean = barcode.codex.Code39(number, add_checksum=False)

        unique_filename = uuid.uuid4()

        filename = ean.save(unique_filename)
        
        # Now, let's create an object of EAN13 
        # class and pass the number 
        # my_code = Code128(number)
        
        # Our barcode is ready. Let's save it. 
        # file = my_code.save("new")

        return Response(filename)


class ProductPostApi(APIView):
    def post(self,request,*args,**Kwargs):
        try:
            get_warehouse = request.data.get('warehouse_uid',None)
            if get_warehouse is None or get_warehouse == '':
                return get_exception_context({'warehouse_uid':['warehouse_uid is required']})     
            request.data._mutable = True
            # print('request data===',request.data)
            get_warehouse=WareHouse.objects.get(uid=request.data['warehouse_uid'])
            get_super_user_for_testing = User.objects.get(is_superuser=True)
            # print('get_warehouse:===',get_warehouse)
            request.data['warehouse'] = get_warehouse.id
            request.data['created_by'] = get_super_user_for_testing.id
            request.data._mutable = False
            get_product_image = request.FILES.getlist('product_image')
            print('get_product_image====',get_product_image)
            print('get file list image',request.FILES.getlist)
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()     
                get_product_id = serializer.data.get('id')
                if get_product_image:
                    for image in get_product_image:
                        create_image_obj = ProductImage.objects.create(product_id=get_product_id, image=image,type='uploded')
                else:
                    create_image_obj = ProductImage.objects.create(product_id=get_product_id, image='product_image/default_product_image.jpg',type='default')

                return get_serializer_context("Product Created Successfully!")
                
            else:
                return get_exception_context(serializer.errors)
            
        except Exception as exception:
            return get_exception_context(str(exception))
        

class GetProductListAPI(APIView):

    def get(self,request,*args,**kwargs):
        try:
            get_product = Product.objects.all().select_related('warehouse','created_by')
            serializer = ProductListSerializer(get_product,many=True)
            return get_serializer_context(serializer.data)
        except Exception as exception:
            return get_exception_context(str(exception))


        
class ProductDeleteApi(APIView):

    def delete(self,request,uid,*args,**kwargs):
        try:
            try:
                get_product = Product.objects.get(uid=uid)
                get_product.delete()
                return get_serializer_context("Product Delete Successfully!")
            except Exception as exception:
                return get_exception_context('Product does not exist!')
        except Exception as exception:
            return get_exception_context(str(exception))
    
class ProductUpdateApi(APIView):
    def put(self,request,uid,*args,**kwargs):

        try:
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
                        # get_obj.type == 'default'
                        get_obj.delete()
 
                return get_serializer_context("Product Updated Succesfully!")
            else:
                return get_exception_context(serializer.errors)
            
        except Exception as exception:
            return get_exception_context(str(exception))
        
class ProductDetailApi(APIView):
    def get(self,request,uid,*args,**kwargs):
        try:
            get_product = Product.objects.select_related('warehouse','created_by').get(uid=uid)
            serializer = ProductdetailSerializer(get_product)
            return get_serializer_context(serializer.data) 
        except Exception as exception:
            return get_exception_context(str(exception))

        
class ProductImageDeleteApi(APIView):
    def delete(self,request,uid,*args,**kwargs):
        try:
            try:
                get_obj = ProductImage.objects.get(uid=uid)
                get_obj.delete()
                return get_serializer_context("Product Image Deleted!")
            except Exception as exception:
                return get_exception_context("Image Not Found")
        except Exception as exception:
            return get_exception_context(str(exception))


class WipingQuestionsPostApi(APIView):
    def post(self,request,*args,**kwargs):
        try:
            get_product = request.data.get('product_uid',None)
            print('get_product====',get_product)
            if get_product is None or get_product == '':
                return get_exception_context({'product_uid':['product_uid is required']})
            request.data._mutable = True
            get_product = Product.objects.get(uid=request.data['product_uid'])
            request.data['product'] = get_product.id
            request.data._mutable = False
            serializer = WipingQuestionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return get_serializer_context(serializer.data)
            else:
                return get_exception_context(serializer.errors)
            
        except Exception as exception:
            return get_exception_context(str(exception))
        

class WipingQuestionsUpdateApi(APIView):
    def put(self,request,uid,*args,**kwargs):
        try:
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
        except Exception as exception:
            return get_exception_context(str(exception))
            
            
class WipingQuestionsGetApi(APIView):
    def get(self,request,uid,*args,**kwargs):
        try:
            try:
                get_wiped = WipingQuestionnaire.objects.select_related('product').get(uid=uid)
                serializer = WipingQuestionGetSerializer(get_wiped)
                return get_serializer_context(serializer.data)
            except Exception as exception:
                return get_exception_context(serializer.errors)      
        except Exception as exception:
            return get_exception_context(str(exception))
        
class WipingQuestionsDeleteApi(APIView):
    def delete(self,request,uid,*args,**kwargs):
        try:
            try:
                get_wiped = WipingQuestionnaire.objects.get(uid=uid)
                get_wiped.delete()
                return get_serializer_context('Device Data Wiping Deleted Successfully')
            except Exception as exception:
                return get_exception_context('Device Data Wiping Does Not Exist')
        except Exception as exception:
            return get_exception_context(str(exception))
        
class WipingQuestionListApi(APIView):
    def get(self,request,*args,**kwargs):
        try:
            try:           
                get_wiped = WipingQuestionnaire.objects.all().select_related('product')
                serializer = WipingQuestionGetSerializer(get_wiped,many=True)
                return get_serializer_context(serializer.data)
            except Exception as exception:
                return get_exception_context(serializer.errors)        
        except Exception as exception:
            return get_exception_context(str(exception))
            
            


        
