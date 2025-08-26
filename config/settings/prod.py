# config/settings/prod.py
from .base import *
from .database.postgres import DATABASES
from .logging.logging_config import LOGGING
from .security.csrf import *
from .security.cors import *
from .security.ssl import *
from .authentication.jwt import *
DEBUG = False

ALLOWED_HOSTS = ["*"]