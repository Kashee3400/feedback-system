default_app_config = 'invent_app.apps.InventAppConfig'

def ready():
    # Import signals here to ensure they are loaded after the application is ready
    from invent_app import signals

# Import celery_app from .celery module
from .celery import celery_app
    
# Define __all__ to export celery_app when using `from invent_app import *`
__all__ = ('celery_app',)
