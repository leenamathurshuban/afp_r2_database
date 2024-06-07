from django.db import models
import uuid,os,shutil
import barcode
from account.models import (
    User
)

# Create your models here.

class BaseModel(models.Model):
    uid = models.UUIDField(editable=False,default=uuid.uuid4,unique=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class WareHouse(BaseModel):
    warehouse_name = models.CharField(max_length=150,null=True,blank=True)

    def __str__(self):
        return self.warehouse_name
    
    class Meta:
        verbose_name_plural = "WareHouse"

class Product(BaseModel):
    PRODUCT_STATUS = (
        ('CHECKED-IN','CHECKED-IN'),
        ('CHECKED-OUT','CHECKED-OUT'),
    )
    warehouse  = models.ForeignKey(WareHouse, related_name='product_warehouse', on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=255,blank=True, null=True)
    year = models.CharField(max_length=255,blank=True, null=True)
    product_size = models.CharField(max_length=255,blank=True, null=True)
    device_type = models.CharField(max_length=255,blank=True, null=True)
    product_status = models.CharField(max_length=255,choices=PRODUCT_STATUS,blank=True, null=True)
    model_number = models.CharField(max_length=255,blank=True, null=True)
    emc_number = models.CharField(max_length=255,blank=True, null=True)
    model_family = models.CharField(max_length=255,blank=True, null=True)
    memory = models.CharField(max_length=255,blank=True, null=True)
    storage_type = models.CharField(max_length=255,blank=True, null=True)
    storage_size = models.CharField(max_length=255,blank=True, null=True)
    battery_capacity = models.CharField(max_length=255,blank=True, null=True)
    battery_cycles = models.CharField(max_length=255,blank=True, null=True)
    grade = models.CharField(max_length=50,blank=True, null=True)
    grade_notes = models.TextField(blank=True,null=True)
    technical_notes = models.TextField(blank=True,null=True)
    track_pad = models.BooleanField(default=False,null=True)
    keyboard = models.BooleanField(default=False,null=True)
    lcd_ghost_peel = models.BooleanField(default=False,null=True)
    headphone_jack = models.BooleanField(default=False,null=True)
    microphone = models.BooleanField(default=False,null=True)
    usb_port = models.BooleanField(default=False,null=True)
    bluetooth_wifi = models.BooleanField(default=False,null=True)
    face_time_camera = models.BooleanField(default=False,null=True)
    find_my_mac = models.BooleanField(default=False,null=True)
    mdm = models.BooleanField(default=False,null=True)
    created_by = models.ForeignKey(User, related_name="created_by_user", on_delete=models.CASCADE, blank=True, null=True) # Added on 05/06/2024

    bar_code  = models.FileField(upload_to='bar_code/',blank=True, null=True)


    def __str__(self):
        return self.device_type
    
    class Meta:
        verbose_name_plural = 'Product'

    
    # def save(self, *args, **kwargs):

    #     if self.id:
    #         number = f"AFP000{self.id}"
        
    #     else:
    #         number = "AFP0001"

    #     ean = barcode.codex.Code39(number, add_checksum=False)
    #     unique_filename = uuid.uuid4()
    #     filename = ean.save(unique_filename)
    #     if not self.bar_code:
    #         self.bar_code = filename

    #     return super(Product, self).save(*args, **kwargs)


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, related_name='product_image', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_image/',blank=True, null=True)

    def __str__(self):
        return self.product.device_type
    
    class Meta:
        verbose_name_plural = 'Product Image'
    



