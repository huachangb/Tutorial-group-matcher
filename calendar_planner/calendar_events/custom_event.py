from ..calendar_events.calendar_event import CalendarEvent

class CustomCalendarEvent(CalendarEvent):
    def __init__(self, title: str, schedule: list, description: str, low_priority: bool) -> None:
        super().__init__(title, schedule, description=description)
        self.type = "Custom event"
        self.low_priority = low_priority

    
    def overlaps(self, cal_event) -> bool:
        if self.low_priority:
            return False
        return super().overlaps(cal_event)