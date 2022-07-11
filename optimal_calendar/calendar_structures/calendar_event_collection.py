""" Contains class definition for CalendarEventCollection 

TODO:
- add method: remove event
- add way to check if certain event has been added
"""

from __future__ import annotations
from typing import Union
from .constants import CCollectionTypes
from .calendar_event import CalendarEvent

class CalendarEventCollection():
    """ Collection of CalendarEvents

    Methods:
        __init__
        __iter__
        __next__
        __contains__
        __len__
        events
        add_event
        overlaps
        in_range
    """
    def __init__(
            self, 
            title: str = "", 
            description: str = "", 
            collection_type: CCollectionTypes = CCollectionTypes.OTHER,
            collection_id: str = None
        ) -> None:
        """ Initializes class """
        self.title = title
        self.description = description
        self.type = collection_type
        self.collection_id = collection_id
        self.__events = [] # a.k.a. schedule

        # declarations for __iter__
        self.__n = 0
        self.__max = 0
    

    def __iter__(self):
        """ Allows iterating over class """
        self.__n = 0
        self.__max = len(self.__events)
        return self

    
    def __next__(self):
        """ Returns n-th event """
        if self.__n < self.__max:
            self.__n += 1
            return self.__events[self.__n - 1]
        else:
            raise StopIteration

    
    def __contains__(self, __o: object) -> bool:
        """ Returns True if <__o> is an element of <events> """
        return __o in self.__events

    
    def __len__(self) -> int:
        """ Returns number of events in current instance """
        return len(self.__events)


    @property
    def events(self) -> list:
        """ Returns list of events """
        return self.__events.copy()


    def add_event(self, cal_event: CalendarEvent) -> None:
        """ Adds event to list of events """
        assert isinstance(cal_event, CalendarEvent), "Argument should be of type CalendarEvent"
        self.__events.append(cal_event)


    def overlaps(self, cal_event: Union[CalendarEvent, CalendarEventCollection]) -> bool:
        """ 
        Returns True if <cal_event> has overlap with any of the events of the current instance.
        Else, returns False 
        """
        return any(cal_event.overlaps(event) for event in self.__events)


    def in_range(self, dtrange: CalendarEvent) -> bool:
        """
        Returns True if <self> is in <dtrange>, only considers hours
        """
        return all(event.in_range(dtrange) for event in self.__events)
