from calendar_planner.calendar_events.calendar_event import CalendarEvent
from calendar_planner.constants import NO_GROUP

class Lecture(CalendarEvent):
    def __init__(self, title: str, schedule: list, description: str) -> None:
        super().__init__(title, schedule, description=description)
        self.type = "Hoorcollege"