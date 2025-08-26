
import os
import sys
from dotenv import load_dotenv

load_dotenv() 

def main():
    """Run administrative tasks."""
    try:
        DJANGO_MODE = os.getenv("DJANGO_MODE", "development").lower()

        if DJANGO_MODE == "development" or DJANGO_MODE == "dev":
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
        elif DJANGO_MODE == "prod" or DJANGO_MODE == "production":
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")
        else:
            raise ValueError(f"Invalid DJANGO_MODE value: {DJANGO_MODE}")
        
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
