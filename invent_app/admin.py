from django.contrib import admin
from django.utils.translation import gettext_lazy
from .models import *
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.apps import apps

# Get all models from the app 'invent_app'

app_name = 'invent_app'
app_models = apps.get_app_config(app_name).get_models()


for model in app_models:
    # Exclude CustomUser model
    if model.__name__ == 'CustomUser':
        continue
    
    # Determine searchable fields
    search_fields = [field.name for field in model._meta.fields if isinstance(field, (models.CharField, models.TextField))]

    # Create admin class attributes
    admin_class_attrs = {
        '__module__': model.__module__,
        'list_display': [field.name for field in model._meta.fields],
        'search_fields': search_fields,
    }
    
    # Create admin class dynamically
    admin_class = type(f'{model.__name__}Admin', (admin.ModelAdmin,), admin_class_attrs)
    
    # Register admin class
    admin.site.register(model, admin_class)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'first_name','last_name','email','is_superuser', 'role']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role','department')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role','department')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
