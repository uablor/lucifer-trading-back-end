import os

env = os.getenv('DJANGO_ENV', 'dev')

if env == 'prod':
    from .prod import application
else:
    from .dev import application
