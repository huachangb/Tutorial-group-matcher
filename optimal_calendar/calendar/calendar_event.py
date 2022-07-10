""" Contains class definition for CalendarEvent """

from __future__ import annotations
from typing import Union
from .constants import CEventTypes, NO_GROUP
from ..schedule.schedule import Schedule
from ..schedule.schedule_item import ScheduleItem
from ..schedule.datetimerange import Datetimerange


class CalendarEvent():
    """ Any activity, whether it be a lecture or doctors appointment """
    def __init__(self, title: str, schedule: list, description: str = "") -> None:
        self.title = title
        self.description = description
        self.type = CEventTypes.OTHER
        self.group = NO_GROUP
        self.__n = 0
        self.__max = 0
        self.__schedule = Schedule()

        for schedule_item in schedule:
            self.add_to_schedule(ScheduleItem(
                description=schedule_item["description"],
                begin_date=schedule_item["start_date"],
                location=schedule_item["location"],
                hours=schedule_item["duration_hours"],
                minutes=schedule_item["duration_minutes"]
            ))

    def __len__(self) -> int:
        return len(self.__schedule)

    def __str__(self) -> str:
        """ TODO """
        return f"{self.title}, {self.type} with {len(self.__schedule)} schedule item(s)"


    def __iter__(self) -> CalendarEvent:
        """ Allows iterating over class """
        self.__n = 0
        self.__max = len(self.__schedule)
        return self


    def __next__(self) -> ScheduleItem:
        """ Returns n-th element of objects schedule """
        if self.__n < self.__max:
            self.__n += 1
            return self.__schedule.get_item(self.__n - 1)
        else:
            raise StopIteration


    @property
    def schedule(self):
        return self.__schedule

    
    def add_to_schedule(self, schedule_item: ScheduleItem) -> None:
        """ adds item to schedule """
        assert isinstance(schedule_item, ScheduleItem)
        self.__schedule.add_item(schedule_item)


    def overlaps(self, c_event: Union[CalendarEvent, Datetimerange, Schedule, ScheduleItem]) -> bool:
        """
        Checks whether there is overlap between c_event and itself
        Returns True is there is overlap, else returns False
        """
        if isinstance(c_event, (Datetimerange, ScheduleItem, Schedule)):
            return self.__schedule.overlaps(c_event)

        return any(self.overlaps(schedule_item) for schedule_item in c_event)
