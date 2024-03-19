from django.contrib import admin
from django.utils.translation import gettext_lazy
from .models import *
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'first_name','last_name','email','is_superuser', 'role']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

# Register the CustomUserAdmin class with the CustomUser model
admin.site.register(CustomUser, CustomUserAdmin)

class RoleAdmin(admin.ModelAdmin):
    list_display = ['id','role']
    
admin.site.register(Role,RoleAdmin)