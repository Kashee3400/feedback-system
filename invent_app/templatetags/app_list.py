from django import template
from django.urls import reverse
from invent_app.utility import app_models
register = template.Library()

@register.simple_tag
def myapp_navigation(app_name):
    models = app_models.get_app_models(app_name)
    navigation_html = ''
    for model in models:
        model_name = model.__name__
        model_url = reverse('model_create', kwargs={'model_name': model_name.lower()})
        another_url = reverse('another_url_name')  # Replace 'another_url_name' with your actual URL name
        navigation_html += f'<li><a href="{model_url}">{model_name}</a> (<a href="{another_url}">Another URL</a>)</li>'
    return navigation_html