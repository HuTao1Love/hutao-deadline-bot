from datetime import datetime, date


def get_date(deadline: datetime, time: str = None) -> str:
    date_format = "%d.%m.%Y" if deadline.year != date.today().year else (
        "%d.%m"
        if deadline.month != date.today().month or deadline.day != date.today().day
        else None
    )
    if time is None:
        return "Today" if not date_format else deadline.strftime(date_format)
    else:
        return "Today" if not date_format else deadline.strftime(date_format) + " " + time
