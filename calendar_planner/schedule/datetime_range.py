from datetime import datetime, time, timedelta
from ..schedule.convert import parse_datetime

class DateTimeRange():
    """ Class for managing time ranges """
    def __init__(self, begin_date: datetime, hours: int, minutes: int = 0) -> None:
        """ Initializes class by setting the start and end
        of the time range"""
        self.begin = begin_date
        self.end = begin_date + timedelta(hours=hours, minutes=minutes)


    def __str__(self) -> str:
        return f"{parse_datetime(self.begin)} to {parse_datetime(self.end)}"
        
    
    def overlaps(self, timerange) -> bool:
        """ Checks if two time ranges overlap """
        s1 = self.begin <= timerange.begin < self.end
        s2 = timerange.begin <= self.begin < timerange.end        
        return s1 or s2

    def within_range(self, timerange) -> bool:
        """ Checks if time range is between begin and end """
        within_lower_limit = self.begin.time() >= timerange.begin.time()
        within_upper_limit = self.end.time() <= timerange.end.time()
        return within_lower_limit and within_upper_limit