import datetime

def find_nearest_weekday(now=datetime.datetime.now()):
    MONDAY = 0
    FRIDAY = 5
    current = now
    # departure_time MUST be in the future so adding 1 day to start
    current += datetime.timedelta(days=1)
    while current.weekday() > FRIDAY:
        current += datetime.timedelta(days=1)
    return current
