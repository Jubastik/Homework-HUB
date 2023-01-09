"""
f = fetch, достать данные
"""
from datetime import datetime, timedelta, time


def f_days_from_schedules(schedules):
    days = set()
    for schedule in schedules:
        days.add(schedule["day"]["name"])
    return list(days)


def create_time_tables(start_time: datetime.time):
    time_tables = []
    for i in range(1, 9):
        les = {
            "lesson_number": i,
            "begin_time": start_time.strftime("%H:%M"),
            "end_time": time(start_time.hour, start_time.minute + 45).strftime("%H:%M"),
        }
        time_tables.append(les)
        start_time = time(start_time.hour + 1, start_time.minute)
    return time_tables
