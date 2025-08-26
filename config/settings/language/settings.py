from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', 'English'),
    ('lo', 'Lao'),
]

USE_I18N = True

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
