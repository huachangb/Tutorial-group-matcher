from datetime import datetime
from calendar_planner.constants import MONTHS

def parse_time(datetime_str: datetime) -> str:
    """ Returns time in HH:MM format """
    return datetime.strftime(datetime_str, "%H:%M")


def parse_date(datetime_str: datetime) -> str:
    """ Returns date in yyyy-mm-dd format """
    return datetime.strftime(datetime_str, "%Y-%m-%d")


def parse_datetime(datetime_str: str) -> str:
    return f"{parse_date(datetime_str)} {parse_time(datetime_str)}"


def dutch_month_to_num(month: str) -> str:
    """ Converts shorthand notation for month to its numeric equivalent """
    return MONTHS[month]


def to_datetime(date_: str) -> str:
    """ Converts dutch datetime str to datetime object 
    Such as, '10 sep 2021'
    """
    x = date_.split()
    return datetime(int(x[2]), dutch_month_to_num(x[1]), int(x[0]))