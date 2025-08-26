import os
import os
from dotenv import load_dotenv

load_dotenv()

env = os.getenv('DJANGO_ENV', 'dev').lower()
if env == 'prod':
    from .prod import *
elif env == 'test':
    from .test import *
else:
    from .dev import *


