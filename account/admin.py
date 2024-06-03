from django.contrib import admin
from account.models import (
    Role,
    User,
   
)

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['user_uid','username','user_role','first_name','last_name','afp_code']

    search_fields = ['username','user_role__role_name','first_name','last_name']

class RoleAdmin(admin.ModelAdmin):
    list_display = ['role_uid','role_name','status']



admin.site.register(User,UserAdmin)
admin.site.register(Role,RoleAdmin)