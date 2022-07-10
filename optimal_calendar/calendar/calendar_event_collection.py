""" Contains class definition for CalendarEventCollection 

TODO:
- add method: remove event
"""

from .constants import CCollectionTypes
from .calendar_event import CalendarEvent

class CalendarEventCollection():
    """ Collection of CalendarEvents. 
    Examples: courses or practical seminar groups (see other files)
    Abstract strucuture
    """
    def __init__(
            self, 
            title: str, 
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


    @property
    def events(self) -> list:
        """ Returns list of events """
        return self.__events.copy()


    def add_event(self, cal_event: CalendarEvent) -> None:
        """ Adds event to list of events """
        assert isinstance(cal_event, CalendarEvent), "Argument should be of type CalendarEvent"
        self.__events.append(cal_event)
