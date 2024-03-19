from django.apps import AppConfig


class InventAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'invent_app'
    def ready(self):
        import invent_app.signals.group_permission
