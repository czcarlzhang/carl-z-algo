from datetime import date, datetime
from dateutil import tz

def utc_to_local(hour, min, sec):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    # in consideration of daylight saving time
    today_date = date.today().strftime('%Y-%m-%d')

    # make datetime object utc timezone
    utc = datetime.strptime(today_date + ' ' + hour + ':' + min + ':' + sec, '%Y-%m-%d %H:%M:%S')
    utc = utc.replace(tzinfo=from_zone)

    # convert utc timezone to local timezone
    local_datetime = utc.astimezone(to_zone).strftime('%Y-%m-%d %H:%M:%SS')
    return local_datetime[11:16]