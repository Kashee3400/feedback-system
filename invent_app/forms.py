# forms.py
from django import forms
from django.apps import apps

def generate_dynamic_model_forms():
    dynamic_forms = {}
    models = apps.get_models()
    for model in models:
        Meta = type('Meta', (object,), {'model': model, 'fields': '__all__'})
        form_class = type(f'{model.__name__}Form', (forms.ModelForm,), {'Meta': Meta})
        dynamic_forms[model.__name__] = form_class
    return dynamic_forms
