# config/settings/base.py

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

from config.settings.security.secret_key import SECRET_KEY

from config.settings.apps.installed import INSTALLED_APPS

from config.settings.middleware.settings import MIDDLEWARE

ROOT_URLCONF = 'config.settings.application.urls'

WSGI_APPLICATION = 'config.settings.application.wsgi.application'
ASGI_APPLICATION = 'config.settings.application.asgi.application'


from config.settings.restframework.settings import REST_FRAMEWORK
from config.settings.celery.settings import *
# from config.settings.authentication.jwt import SIMPLE_JWT
from config.settings.templates.settings import *
from config.settings.authentication.settings import *    
# from config.settings.authentication.password_validators import AUTH_PASSWORD_VALIDATORS
from config.settings.localization.settings import (
    LANGUAGE_CODE,
    TIME_ZONE,
    USE_I18N,
    USE_TZ,
)
from config.settings.assets.storage import STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT
# from config.settings.authentication.user_model import *
# from config.settings.global_settings.settings import Response, status