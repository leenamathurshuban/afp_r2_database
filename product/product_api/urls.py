from django.urls import path
from product.product_api.views import (
    generate_barcode
)

urlpatterns = [

    path('bar-code/',generate_barcode.as_view()),
    
]
