from calendar_planner.calendar_events.calendar_event import CalendarEvent

class PracticalLecture(CalendarEvent):
    def __init__(self, title: str, group: str, schedule: list, description: str) -> None:
        super().__init__(title, schedule, description=description)
        self.group = group
        self.type = "Werkcollege"


    def add_lectures(self, practical_lecture) -> None:
        """ Adds lectures from another instance of practical lecture """
        for lecture in practical_lecture.schedule:
            self.add_schedule_item(lecture)