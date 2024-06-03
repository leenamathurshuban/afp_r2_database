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