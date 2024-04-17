from django import template

register = template.Library()

@register.simple_tag()
def get_object_fields(instance):
    return instance._meta.get_fields()
