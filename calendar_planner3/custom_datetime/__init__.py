from datetime import datetime, timedelta
from calendar_planner3.constants import MONTHS

class DateTimeRange():
    """ Class for managing time ranges """
    def __init__(self, start: datetime, hours: int) -> None:
        """ Initializes class by setting the start and end
        of the time range"""
        self.start = start
        self.end = start + timedelta(hours=hours)
    
    def overlaps(self, timerange) -> bool:
        """ Checks if two time ranges overlap """
        if self.start.date() != timerange.start.date():
            return False
        s1 = self.start <= timerange.start < self.end
        s2 = timerange.start <= self.start < timerange.end        
        return s1 or s2


def parse_time(datetime_str: str) -> str:
    """ Returns time in HH:MM format """
    return datetime.strftime(datetime_str, "%H:%M")


def parse_date(datetime_str: str) -> str:
    """ Returns date in yyyy-mm-dd format """
    return datetime.strftime(datetime_str, "%Y-%m-%d")


def dutch_month_to_num(month: str) -> str:
    """ Converts shorthand notation for month to its numeric equivalent """
    return MONTHS[month]


def to_datetime(date_: str) -> str:
    """ Converts dutch datetime str to datetime object 
    Such as, '10 sep 2021'
    """
    x = date_.split()
    return datetime(int(x[2]), dutch_month_to_num(x[1]), int(x[0]))

