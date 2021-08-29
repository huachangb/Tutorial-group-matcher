from datetime import datetime, timedelta
from calendar_planner.schedule.convert import parse_datetime

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