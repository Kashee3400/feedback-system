from django.apps import apps


def get_app_models(app_name):
    app_config = apps.get_app_config(app_name)
    return app_config.get_models()
