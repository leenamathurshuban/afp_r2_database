from django.db import models

from account.managers  import UserManager
from django.contrib.auth.models import AbstractUser
import uuid,os,shutil

from django.conf import settings

# Create your models here.


class Role(models.Model):
    status_choice = (
        ('Active' ,'Active'),
        ('Inactive','Inactive')
    )

    role_uid = models.UUIDField(editable=False,default=uuid.uuid4,unique=True,blank=True)
    role_name = models.CharField(max_length=100,blank=True, null=True,unique=True)
    status = models.CharField(max_length=20,choices=status_choice,blank=True,null=True,default='Active')
    image = models.ImageField(upload_to='role_image/',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.role_name

    class Meta:
        verbose_name_plural = 'Role'


def get_unique_code(first_name, last_name):
    number = str(uuid.uuid4().int)[:4]
    code = 'AFP' + first_name[0].upper() + last_name[0].upper() + number
    return code

class User(AbstractUser):
    # USER_STATUS = (
    #     ("Pending" , "Pending"),
    #     ("Approved" , "Approved"),
    #     ("Rejected" , "Rejected")
    # )

    user_uid = models.UUIDField(editable=False,default=uuid.uuid4,unique=True,blank=True)
    email = models.EmailField(blank=True, null=True)
    user_role = models.ForeignKey(Role,related_name='reverse_user_role',blank=True, null=True, on_delete=models.CASCADE)
    phone_number = models.IntegerField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='user_profile/',blank=True, null=True)
    employee_number = models.CharField(max_length=50, blank=True, null=True)
    afp_code = models.CharField(max_length=200, unique=True, blank=True, null=True)
    # status = models.CharField(max_length=30,default="Pending",choices=USER_STATUS)
    # is_user_active = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    objects = UserManager()

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name_plural = "User"

    # def save(self, *args, **kwargs):
    #     super(User, self).save(*args, **kwargs)

