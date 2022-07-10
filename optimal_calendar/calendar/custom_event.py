from .calendar_event import CalendarEvent
from .constants import CEventTypes

class CustomCalendarEvent(CalendarEvent):
    """
    Overrides:
        overlaps()
    """
    def __init__(self, title: str, schedule: list, description: str, low_priority: bool) -> None:
        super().__init__(title, schedule, description=description)
        self.type = CEventTypes.CUSTOM
        self.low_priority = low_priority

    
    def overlaps(self, cal_event: CalendarEvent) -> bool:
        """
        Ignore overlap if low priority
        """
        low_prio = self.low_priority
        if isinstance(cal_event, CustomCalendarEvent):
            low_prio = low_prio or cal_event.low_priority
        return not low_prio and super().overlaps(cal_event)
