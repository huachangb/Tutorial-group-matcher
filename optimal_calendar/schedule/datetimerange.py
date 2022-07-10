""" Class definition for Datetimerange """

from __future__ import annotations
from datetime import datetime, timedelta


class Datetimerange():
    """
    Class for managing time ranges, with a precision up to a minute
    """
    def __init__(self, begin_date: datetime, hours: int, minutes: int = 0) -> None:
        """ Initializes class by setting the start and end of the time range"""
        self.begin = begin_date
        self.end = begin_date + timedelta(hours=hours, minutes=minutes)


    def __eq__(self, __o: Datetimerange) -> bool:
        return self.begin == __o.begin and self.end == __o.end


    def __str__(self) -> str:
        return f"{self.parse_datetime(self.begin)} to {self.parse_datetime(self.end)}"


    @staticmethod
    def parse_datetime(dtime: datetime) -> str:
        """ Parses datetime from string, format = yyyy-mm-dd hh:mm """
        return datetime.strftime(dtime, "%Y-%m-%d %H:%M")


    def overlaps(self, dtimerange: Datetimerange) -> bool:
        """ Checks if two time ranges overlap """
        s_1 = self.begin <= dtimerange.begin < self.end
        s_2 = dtimerange.begin <= self.begin < dtimerange.end
        return s_1 or s_2


    def within_range(self, dtimerange: Datetimerange) -> bool:
        """ Checks if current instance is between begin and end of the given
        dtrange"""
        within_lower_limit = self.begin.time() >= dtimerange.begin.time()
        within_upper_limit = self.end.time() <= dtimerange.end.time()
        return within_lower_limit and within_upper_limit
