from calendar_planner.calendar_events.lecture import Lecture
from calendar_planner.calendar_events.practical_lecture import PracticalLecture

class Course():
    def __init__(self, title: str) -> None:
        self.title = title
        self.lectures = []
        self.groups = {}
        
    
    def __str__(self) -> str:
        return f"{self.title}, with {len(self.lectures)} lecture(s) and {len(self.groups)} group(s)"

    
    def add_lecture(self, lecture: Lecture) -> None:
        """ Adds lecture to lectures """
        assert isinstance(lecture, Lecture)
        self.lectures.append(lecture)

    
    def add_practical_lecture(self, group: str, practical_lecture: PracticalLecture) -> None:
        """ Adds practical lecture. If there is already a record of a group, 
        <practical_lecture> will be merged with this instance """
        assert isinstance(practical_lecture, PracticalLecture)
        if group not in self.groups:
            self.groups[group] = practical_lecture
            return
        self.groups[group].add_lectures(practical_lecture)


    def overlaps(self, cal_event, group: str) -> bool:
        """ Checks if schedule overlaps with the schedule of self """
        overlap_lectures = any(
            lecture.overlaps(cal_event) for lecture in self.lectures
        )
        overlap_practicals = self.groups[group].overlaps(cal_event)
        return overlap_lectures or overlap_practicals
