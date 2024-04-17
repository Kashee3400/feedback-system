from django.contrib.admin.sites import AdminSite
from django.urls import path
from django.apps import apps
from . import views
from invent_app.utility import app_models

class MyAdminSite():
    app_name = "invent_app"
    
    def __init__(self, name="myadmin"):
        self.name = name

    @property
    def urls(self):
        return self.get_urls(), "myadmin", self.name

    def get_urls(self):
        urls = [
            path(f'', views.index, name='index'),
        ]
        
        models = app_models.get_app_models(app_name=self.app_name)
        for model in models:
            model_name = model.__name__.lower()
            urlpatterns = [
                path(f'{model_name}/', views.model_list, name=f'{model_name}_list'),
                path(f'{model_name}/create/', views.model_create, name=f'{model_name}_create'),
            ]
            urls += urlpatterns
        return urls
    

    
