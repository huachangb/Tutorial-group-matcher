from ..calendar_events.calendar_event import CalendarEvent

class Lecture(CalendarEvent):
    def __init__(self, title: str, schedule: list, description: str) -> None:
        super().__init__(title, schedule, description=description)
        self.type = "Hoorcollege"