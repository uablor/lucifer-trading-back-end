from babel.dates import format_datetime
from datetime import datetime
from typing import Optional

def format_date_to_lao(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None
    return format_datetime(dt, locale='lo')

def format_date_to_english(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None
    return format_datetime(dt, locale='en')