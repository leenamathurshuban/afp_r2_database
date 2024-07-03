from django.contrib import admin
from account.models import (
    Role,
    User,
    UserRolePermission,
   
)

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['user_uid','username','user_role','first_name','last_name','afp_code']

    search_fields = ['username','user_role__role_name','first_name','last_name']

class RoleAdmin(admin.ModelAdmin):
    list_display = ['role_uid','role_name','status']

class UserRolePermissionAdmin(admin.ModelAdmin):
    list_display = ['uid','role','permission_module','can_add','can_update','can_list','can_delete','can_do_all']

    search_fields = ['user_role__role_name','permission_module']
    

from django.contrib.admin.models import LogEntry
admin.site.register(LogEntry)

admin.site.register(User,UserAdmin)
admin.site.register(Role,RoleAdmin)
admin.site.register(UserRolePermission,UserRolePermissionAdmin)
