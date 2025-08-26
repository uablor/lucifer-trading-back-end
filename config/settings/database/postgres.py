# config/settings/database/postgres.py

import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'prod_db'),
        'USER': os.getenv('DB_USER', 'prod_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'prod_password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
