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
    start_time = datetime.combine(datetime.today(), start_time)
    time_tables = []
    for i in range(1, 9):
        end_time = start_time + timedelta(minutes=45)
        les = {
            "lesson_number": i,
            "begin_time": start_time.strftime("%H:%M"),
            "end_time": end_time.strftime("%H:%M"),
        }
        time_tables.append(les)
        start_time = start_time + timedelta(minutes=60)
    return time_tables
