from calendar_planner.courses.classBase import ClassBase

class PracticalLecture(ClassBase):
    def __init__(self, course_title: str, schedule: list, group: str) -> None:
        super().__init__(course_title, schedule, group=group)
        self.type = "Werkcollege"


    def add_lectures(self, schedule: list) -> None:
        """ Merges list of lectures """
        for lecture in schedule:
            self.add_lecture_fixed(lecture)

    
    def overlaps_with_course(self, calendar, course_title, group) -> bool:
        """ Checks if there is overlap between schedules """
        course = calendar.courses[course_title]
        for lecture in self.schedule:
            if course.overlaps(lecture["time_range"], group):
                return False
        return True

