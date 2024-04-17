from django import template

register = template.Library()

@register.filter(name='has_permission')
def has_permission(user, permission):
    return user.has_perm(permission)
