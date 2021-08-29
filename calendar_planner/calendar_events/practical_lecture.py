from calendar_planner.calendar_events.calendar_event import CalendarEvent

class PracticalLecture(CalendarEvent):
    def __init__(self, title: str, group: str, schedule: list, description: str) -> None:
        super().__init__(title, schedule, description=description)
        self.group = group
        self.type = "Werkcollege"

    
    def __len__(self) -> int:
        return len(self.schedule)


    def add_lectures(self, practical_lecture) -> None:
        """ Adds lectures from another instance of practical lecture """
        for lecture in practical_lecture.schedule:
            self.add_schedule_item(lecture)

    
    def overlaps_with_course(self, calendar, course_title, group) -> bool:
        """ Check if there is overlap with a couse """
        course = calendar.courses[course_title]
        return course.overlaps(self, group)
        # for lecture in self.schedule:
        #     if course.overlaps(lecture, group):
        #         return True
        
        # return False
