""" Class definition for ScheduleItem """

from __future__ import annotations
from typing import Union
from datetime import datetime
from .datetimerange import Datetimerange

class ScheduleItem(Datetimerange):
    """
    Wraps Datetimerange

    Overrides methods [Datetimerange]:
        __eq__
        __str__
        overlaps
    """
    def __init__(self, description: str, location: str,
                    begin_date: datetime, hours: int,
                    minutes: int = 0) -> None:
        """ Inits class """
        super().__init__(begin_date, hours, minutes)
        self.description = description
        self.location = location

    
    def __eq__(self, __o: ScheduleItem) -> bool:
        same_attr = self.description == __o.description and self.location == __o.location
        return Datetimerange.__eq__(self, __o) and same_attr


    def __str__(self) -> str:
        """ Returns detailed description of current instance """
        description_txt = self.description if self.description else "N/A description"
        return f"{description_txt} at {self.location} on " + Datetimerange.__str__(self)


    def overlaps(self, schedule_item: Union[ScheduleItem, Datetimerange]) -> bool:
        """
        Returns True if current instance overlaps with argument,
        otherwise returns False
        """
        return Datetimerange.overlaps(self, schedule_item)
    