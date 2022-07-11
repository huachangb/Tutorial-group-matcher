from datetime import datetime
from .constants import MONTHS


def dutch_month_to_num(month: str) -> str:
    """ Converts shorthand notation for month to its numeric equivalent """
    return MONTHS[month]


def to_datetime(date_: str) -> str:
    """ Converts dutch datetime str to datetime object 
    Such as, '10 sep 2021'
    """
    x = date_.split()
    return datetime(int(x[2]), dutch_month_to_num(x[1]), int(x[0]))


def parse_time_string(time_str: str) -> datetime:
    """ Parses time from string """
    return datetime.strptime(time_str, "%H:%M")


def list_to_lower(arr) -> list:
    """ Returns list where are elements are in lowercase. 
    Assumes that <arr> only contains strings
    """
    return [x.lower() for x in arr]