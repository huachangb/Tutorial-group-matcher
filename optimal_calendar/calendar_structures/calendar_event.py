""" Contains class definition for CalendarEvent """

from __future__ import annotations
from datetime import datetime, timedelta
from .constants import CEventTypes


class CalendarEvent():
    """
    A calendar event. This may be any activity. 

    Methods
        __init__
        __str__
        __eq__
        parse_datetime
        get_time
        overlaps
        in_range
    """
    def __init__(
            self, 
            title: str,
            begin_date: datetime,
            hours: int,
            description: str = "", 
            location: str = "",
            minutes: int = 0,
            event_type: int = CEventTypes.OTHER,
            compulsory: bool = True
        ) -> None:
        """ Initialize class
        """
        self.title = title
        self.description = description
        self.location = location
        self.type = event_type
        self.compulsory = compulsory
        self.begin = begin_date
        self.end = begin_date + timedelta(hours=hours, minutes=minutes)

    
    def __str__(self) -> str:
        """ Returns global description of current instance """
        description_txt = self.description if self.description else "N/A description"
        return f"{description_txt} at {self.location} on " + str(self.begin)

    
    def __eq__(self, __o: CalendarEvent) -> bool:
        """ Only equal if all fields match, assumes only used in combination with another
        CalendarEvent instance """
        return self.title == __o.title and self.description == __o.description and \
            self.location == __o.location and self.type == __o.type and \
            self.compulsory == __o.compulsory and self.begin == __o.begin and \
            self.end == __o.end


    @staticmethod
    def parse_datetime(dtime: datetime) -> str:
        """ Parses datetime from string, format = yyyy-mm-dd hh:mm """
        return datetime.strftime(dtime, "%Y-%m-%d %H:%M")


    def get_time(self) -> str:
        """ Returns datetime as string"""
        return f"{self.parse_datetime(self.begin)} to {self.parse_datetime(self.end)}"

    
    def overlaps(self, dtimerange: CalendarEvent) -> bool:
        """ Checks if two time ranges overlap """
        s_1 = self.begin <= dtimerange.begin < self.end
        s_2 = dtimerange.begin <= self.begin < dtimerange.end
        return s_1 or s_2


    def in_range(self, dtimerange: CalendarEvent) -> bool:
        """ Checks if current instance is between begin and end of the given
        dtrange"""
        within_lower_limit = self.begin.time() >= dtimerange.begin.time()
        within_upper_limit = self.end.time() <= dtimerange.end.time()
        return within_lower_limit and within_upper_limit
