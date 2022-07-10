from .constants import CEventTypes
from .calendar_event import CalendarEvent

class Lecture(CalendarEvent):
    """
    wraps calendar event
    """
    def __init__(self, title: str, schedule: list, description: str) -> None:
        super().__init__(title, schedule, description=description)
        self.type = CEventTypes.LECTURE
        