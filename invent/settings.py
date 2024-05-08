import os
from pathlib import Path
from dotenv import load_dotenv
import logging

load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# SECURITY WARNING: keep the secret key used in production secret!
KEY = os.getenv('SECRET_KEY', None)
if KEY:
    SECRET_KEY = KEY
else:
    SECRET_KEY = 'django-insecure-vz7340h_a-udjw9@o7d5g3-duv$g9w!em*22tdp4$)15#45)07'


DEBUG = False

# DEBUG = True
if DEBUG:
    ALLOWED_HOSTS = ['localhost', '*']
else:
    ALLOWED_HOSTS = ["tech.kasheemilk.com","1.22.197.176"]


# Application definition

INSTALLED_APPS = [
    'invent_app',
    'awareness',
    'vcg',
    'veterinary',
    'channels',
    'webpush',
    'daphne',
    'rest_framework.authtoken',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'invent_app.login_check_middleware.LoginRequiredMiddleware',
]

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'invent.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

LOGIN_URL = 'login_user'

WSGI_APPLICATION = 'invent.wsgi.application'
ASGI_APPLICATION = 'invent.asgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DB_ENGINE = os.getenv('DB_ENGINE', None)
DB_USERNAME = os.getenv('DB_USER', None)
DB_PASS = os.getenv('DB_PASSWORD', None)
DB_HOST = os.getenv('DB_HOST', None)
DB_PORT = os.getenv('DB_PORT', None)
DB_NAME = os.getenv('DB_NAME', None)
DB_NAME_TEST = os.getenv('DB_NAME', None)

if DB_ENGINE and DB_NAME and DB_USERNAME:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.' + DB_ENGINE,
            'NAME': DB_NAME,
            'USER': DB_USERNAME,
            'PASSWORD': DB_PASS,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
        },
        'vcg': {
            'ENGINE': 'django.db.backends.' + DB_ENGINE,
            'NAME': DB_NAME_TEST,
            'USER': DB_USERNAME,
            'PASSWORD': DB_PASS,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
        'test': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:', 
        }
    }


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

# LANGUAGE_CODE = 'en-US'
LANGUAGE_CODE = 'hi'

# LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', 'en-US')

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

from django.utils.translation import gettext_lazy as _
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),  # Replace 'locale' with the path to your locale directory
]

LANGUAGES = [
    ('en', _('English')),
    ('hi', _('Hindi')),
    ("de", _("German")),
    
]


if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(BASE_DIR, 'error.log'),  # Path to your error log file
                'maxBytes': 1024 * 1024 * 10,  # 10 MB
                'backupCount': 5,  # Keep up to 5 previous log files
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'ERROR',
                'propagate': True,
            },
        },
    }


AUTH_USER_MODEL = 'invent_app.CustomUser'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

MEDIA_URL="/media/"
MEDIA_ROOT=os.path.join(BASE_DIR,"media/")

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATIC_URL="staticfiles/"
STATIC_ROOT="staticfiles/"
STATICFILES_DIRS=[STATIC_DIR]


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp3.netcore.co.in'
EMAIL_PORT = 587  # Port for SMTP (typically 587 for TLS)
EMAIL_USE_TLS = True  # Enable TLS (Transport Layer Security)
EMAIL_HOST_USER = 'gro@kasheemilk.com'  # Your email address
EMAIL_HOST_PASSWORD = '#GEmilk@02*'  # Your email password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # Default sender email address

from django.core.cache.backends.redis import RedisCache

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',  # Adjust host and port if needed
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

from celery.beat import crontab

CELERY_BEAT_SCHEDULE = {
    'backup-database': {
        'task': 'invent_app.tasks.backup_only_data',
        'schedule': crontab(minute=1, hour=0, day_of_month='*', month_of_year='*', day_of_week='*'),
    },
    'backup-data': {
        'task': 'invent_app.tasks.backup_only_data',
        'schedule': crontab(minute=5, hour=0, day_of_month='*', month_of_year='*', day_of_week='*'),
    },
}

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'


# settings.py

CHANNEL_LAYERS = {
    "default": {
        # "BACKEND": "channels.layers.InMemoryChannelLayer",  #Use InMemoryChannelLayer for development
        "BACKEND": "channels_redis.core.RedisChannelLayer",  #Use this for production with Redis
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

SECURE_REFERRER_POLICY = "same-origin"

WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": "BHn29znsBkzIn9-ibaBBZzqbw95prLs9SrghESViOZp11Vlq-ponue91PfIZ_BnKPKdqCahQWB648aspDub-JvQ",
    "VAPID_PRIVATE_KEY":"bmB5JWAM0E7tLjghdW-ZpJqTOOiHY_Ki064VmwOOVcg",
    "VAPID_ADMIN_EMAIL": "divyanshu.kumar@kasheemilk.com"
}
