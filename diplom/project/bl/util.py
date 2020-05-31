from datetime import datetime


def generateAllDayForDate(to):
    form = "%Y-%m-%d"
    to_date = datetime.strptime(to, form).replace(hour=23, minute=59, second=59)
    return to_date