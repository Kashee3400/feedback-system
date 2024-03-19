from django.apps import apps
from django.contrib.auth.models import Permission, ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_model_permissions(sender, **kwargs):
    if sender.name == 'invent_app':
        for model in apps.get_models():
            content_type = ContentType.objects.get_for_model(model)
            permission_name = f'Can view {model._meta.verbose_name_plural}'
            codename = f'view_{model._meta.model_name}'
            permission, created = Permission.objects.get_or_create(
                codename=codename,
                content_type=content_type,
                defaults={'name': permission_name}
            )

            if created:
                print(f'Created permission: {permission_name} ({codename})')
