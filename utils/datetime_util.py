from datetime import datetime

import pytz
from dateutil import tz

from config import TIME_ZONE
from utils.number import suffixes_for_positional_number


def get_now():
    return datetime.utcnow().replace(tzinfo=pytz.UTC)


def convert_to_my_tz(time: datetime):
    if time is None:
        return None
    if time.tzinfo is None:
        time.replace(tzinfo=tz.gettz('UTC'))
    client_tz = tz.gettz(TIME_ZONE)
    time.astimezone(client_tz)
    return time


def convert_to_dict(time: datetime):
    if time is None:
        return None
    return {
        'd': time.strftime('%d'),
        'sd': suffixes_for_positional_number(time.day),
        'm': time.strftime('%B'),
        'y': time.strftime('%Y'),
    }
