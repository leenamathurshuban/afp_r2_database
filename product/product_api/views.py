from django.shortcuts import render
from account.helpers import (
    get_exception_context,
    get_serializer_context,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from product.models import (
    WareHouse
)
from product.product_api.serializers import (
    WareHouseSerializer
)


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
                serializer_error = [serializer.errors[error][0] for error in serializer.errors]
                return get_exception_context(serializer_error)

        except Exception as exception:
            return get_exception_context(str(exception))

    
 
class UpdateWareHouse(APIView):    
    def put(self, request,uid,*args,**kwargs):
        uuid = kwargs.get('uid',None)
        if uuid:       
            try:
                get_warehouse = WareHouse.objects.get(warehouse_uid=uuid)
                serializer = WareHouseSerializer(get_warehouse,data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return get_serializer_context(serializer.data)
                else:
                    serializer_error = [serializer.errors[error][0] for error in serializer.errors]
                    return get_exception_context(serializer_error)
            except Exception as exception:
                return get_exception_context(str(exception))
            


class GetWareHouseList(APIView):   
    def get(self,request,*args,**kwargs):
        try:
            get_warehouse = WareHouse.objects.all()
            serializer =WareHouseSerializer(get_warehouse,many=True)
            if serializer:
                return get_serializer_context(serializer.data)
            else:  
                serializer_error = [serializer.errors[error][0] for error in serializer.errors]
                return get_exception_context(serializer_error)
        except Exception as exception:
            return get_exception_context(str(exception))
        
 
class DeleteWareHouse(APIView):  
    def delete(self,request,uid,*args,**kwargs):
        try:
            try:
                get_warehouse = WareHouse.objects.get(warehouse_uid=uid)
                get_warehouse.delete()
                return get_serializer_context('Ware House Deleted Successfully !')
            except Exception as exception:
                return get_exception_context('Ware House matching query does not exist !')           
        except Exception as exception:
            return get_exception_context(str(exception))
        

class DetailWareHouse(APIView):  
    def get(self,request,uid,*args,**kwargs):
        try:
            get_warehouse = WareHouse.objects.get(warehouse_uid=uid)
            serializer = WareHouseSerializer(get_warehouse)
            if get_warehouse:
                return get_serializer_context(serializer.data)
            else:  
                serializer_error = [serializer.errors[error][0] for error in serializer.errors]
                return get_exception_context(serializer_error)
        except Exception as exception:
             return get_exception_context(str(exception))

# Worked on above code 27/05/2024 By Tasmiya