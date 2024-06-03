
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
# from barcode import EAN13 ,Code39, Code128
import barcode
from barcode.writer import ImageWriter
import uuid



class generate_barcode(APIView):

    def get(self, request, *args, **kwargs):
        # Make sure to pass the number as string 
        number = "AFP0001"
        ary = {}
        # barcode_writer = ImageWriter()

        ean = barcode.codex.Code39(ary, add_checksum=False)

        unique_filename = uuid.uuid4()

        filename = ean.save(f'{number}')
        
        # Now, let's create an object of EAN13 
        # class and pass the number 
        # my_code = Code128(number)
        
        # Our barcode is ready. Let's save it. 
        # file = my_code.save("new")

        return Response(filename)

