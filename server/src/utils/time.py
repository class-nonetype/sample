from src.utils.environments import TIME_ZONE

from pytz import timezone
from datetime import datetime






def get_time_zone():
    return timezone(zone=TIME_ZONE)

def get_datetime() -> datetime:
    return datetime.now(tz=get_time_zone())

