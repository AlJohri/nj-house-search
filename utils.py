import datetime

def find_nearest_weekday(now=datetime.datetime.now()):
    MONDAY = 0
    FRIDAY = 5
    current = now
    while current.weekday() > FRIDAY:
        current += datetime.timedelta(days=1)
    return current
