import datetime
import pytz


def timestamp_to_datetime(t: int):
    return datetime.datetime.fromtimestamp(t)


def timestamp_to_timezone(t: int, zone: str = 'Asia/Tehran'):
    local_tz = pytz.timezone(zone)
    utc_dt = datetime.datetime.utcfromtimestamp(t).replace(tzinfo=pytz.utc)
    return local_tz.normalize(utc_dt.astimezone(local_tz))


def safe_get_user_from_context(context):
    user = None
    request = context.get("request")
    if request and hasattr(request, "user"):
        user = request.user
    return user
