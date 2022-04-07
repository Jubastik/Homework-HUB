def time_is_correct(time):
    try:
        hours, minutes = map(int, time.split(":"))
        if hours < 0 or minutes < 0 or hours > 24 or minutes > 60:
            return False
        if hours != hours or minutes != minutes:
            return False
        return [str(hours), str(minutes)]
    except:
        return False
