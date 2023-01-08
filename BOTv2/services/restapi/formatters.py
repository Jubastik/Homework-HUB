

"""
f = fetch, достать данные
"""
def f_days_from_schedules(schedules):
    days = set()
    for schedule in schedules:
        days.add(schedule['day']['name'])
    return list(days)