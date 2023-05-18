from datetime import datetime


def readable_date(date):
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%B %dth, %Y")
    return formatted_date
