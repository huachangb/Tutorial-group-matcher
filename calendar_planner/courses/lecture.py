from calendar_planner.courses.classBase import ClassBase

class Lecture(ClassBase):
    def __init__(self, course_title: str, schedule: list) -> None:
        super().__init__(course_title, schedule)
        self.type = "Hoorcollege"