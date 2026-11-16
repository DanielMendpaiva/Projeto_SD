import os

IS_PRODUCTION = os.getenv("IS_PRODUCTION", 'False').lower() in ('1', 'true', 't', 'yes', 'y')

if IS_PRODUCTION:
    from .conf.production.settings import *
else:
    from .conf.development.settings import *

# Application definition
INSTALLED_APPS = [
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # required by all-auth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # providers all-auth
        # https://django-allauth.readthedocs.io/en/latest/installation.html
        'allauth.socialaccount.providers.google',
        #'allauth.socialaccount.providers.instagram',
        #'allauth.socialaccount.providers.apple',
        #'allauth.socialaccount.providers.facebook',
        #'allauth.socialaccount.providers.linkedin',
        #'allauth.socialaccount.providers.twitter',
    
    # https://pypi.org/project/django-widget-tweaks/
    # Tweak the form field rendering in templates, 
    # not in python-level form definitions. Altering CSS classes and HTML attributes is supported.
    'widget_tweaks',

    # Enable the inner home (home)   
    'apps.enquetes',  

]

# configurações servem apenas para send_common (SMTP using DJango)
EMAIL_HOST = 'smtp.xxxxxxxxx.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'no-reply@projetosd.com.br'
EMAIL_HOST_PASSWORD = 'xxxxxxxxxx' 
DEFAULT_FROM_EMAIL = 'no-reply@projetosd.com.br'
DEFAULT_REPLY_TO = 'falecom@projetosd.com.br'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'pt-br'

USE_I18N = True
USE_L10N = True

USE_TZ = True
TIME_ZONE = 'America/Recife'