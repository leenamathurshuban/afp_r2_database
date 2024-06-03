from django.db import models
import uuid,os,shutil

# Create your models here.

class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, blank=True)
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


    def __str__(self):
        return self.device_type
    
    class Meta:
        verbose_name_plural = 'Product'


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, related_name='product_image', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_image/',blank=True, null=True)

    def __str__(self):
        return self.product.device_type
    
    class Meta:
        verbose_name_plural = 'Product Image'
    



