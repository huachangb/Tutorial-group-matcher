from __future__ import annotations
from .constants import CEventTypes


from .calendar_event import CalendarEvent

class PracticalSeminar(CalendarEvent):
    def __init__(self, title: str, group: str, schedule: list, description: str) -> None:
        super().__init__(title, schedule, description=description)
        self.group = group
        self.type = CEventTypes.PRACTICAL_SEMINAR


    def add_lectures(self, practical_lecture: PracticalSeminar) -> None:
        """ Adds lectures from another instance of practical lecture """
        for lecture in practical_lecture:
            self.add_to_schedule(lecture)

    
    def overlaps_with_course(self, calendar, course_title: str, group: str) -> bool:
        """ Check if there is overlap with a couse """
        course = calendar.courses[course_title]
        return course.overlaps(self, group)
