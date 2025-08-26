from django.apps import AppConfig

class UserConfigConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.user.config'
    label = 'user_config'
