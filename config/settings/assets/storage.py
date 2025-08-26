from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"
