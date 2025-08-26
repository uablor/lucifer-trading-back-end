# config/settings/dev.py
import os
from .base import *
from .database.sqlite import DATABASES
from .logging.logging_config import LOGGING
from .security.csrf import *
from .security.cors import *
from .authentication.jwt import *

DEBUG = True
ALLOWED_HOSTS = ['*']


