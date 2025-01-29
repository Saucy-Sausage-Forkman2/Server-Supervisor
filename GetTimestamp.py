import datetime
def time():
    current_time = datetime.datetime.now()
    hour = current_time.hour
    minute = current_time.minute
    pm = ' AM'
    if hour >= 12:
        pm = " PM"
    if hour >= 13:
        hour -= 12
    if hour == 0:
    	hour = 12
    if minute < 10:
        minute = "0" + str(minute)

    return f"{hour}" + ":" + f"{minute}"  + f"{pm}" + "  PST"
