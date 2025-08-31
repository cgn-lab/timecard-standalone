from datetime import datetime, timedelta, timezone


class TimeZone:
    UTC = timezone.utc
    JST = timezone(timedelta(hours=9))


__all__ = [
    'TimeZone',
]
