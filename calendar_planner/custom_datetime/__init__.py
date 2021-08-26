from datetime import datetime, timedelta

class DateTimeRange():
    """ Class for managing time ranges """
    def __init__(self, start: datetime, hours: int) -> None:
        """ Initializes class by setting the start and end
        of the time range"""
        self.start = start
        self.end = start + timedelta(hours=hours)
    
    def overlaps(self, timerange) -> bool:
        """ Checks if two time ranges overlap """
        # check if courses start at the same time
        start_same = self.start == timerange.start
        
        # check if courses start while the other course is going
        s1 = self.start <= timerange.start < self.end
        s2 = timerange.start <= self.start < timerange.end        
        
        return start_same or s1 or s2


def parse_time(datetime_str: str) -> str:
    """ Returns time in HH:MM format """
    return datetime.strftime(datetime_str, "%H:%M")


def parse_date(datetime_str: str) -> str:
    """ Returns date in yyyy-mm-dd format """
    return datetime.strftime(datetime_str, "%Y-%m-%d")


def dutch_month_to_num(month: str) -> str:
    """ Converts shorthand notation for month to its numeric equivalent """
    return {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "mei": 5, "jun": 6, "jul": 7, "aug": 8, "sep": 9, "okt": 10, "nov": 11, "dec": 12}[month]


def to_datetime(date_: str) -> str:
    """ Converts dutch datetime str to datetime object 
    Such as, '10 sep 2021'
    """
    x = date_.split()
    return datetime(int(x[2]), dutch_month_to_num(x[1]), int(x[0]))

