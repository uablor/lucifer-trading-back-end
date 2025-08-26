from config.settings.apps.django_apps import DJANGO_APPS
from config.settings.apps.third_party_apps import THIRD_PARTY_APPS
from config.settings.apps.local_apps import LOCAL_APPS

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
