from calendar_planner.calendar_events.lecture import Lecture
from calendar_planner.calendar_events.practical_lecture import PracticalLecture

class Course():
    def __init__(self, title: str) -> None:
        self.title = title
        self.lectures = []
        self.groups = {}
        self.misc = []
        
    
    def __str__(self) -> str:
        return f"{self.title}, with {len(self.lectures)} lecture(s), {len(self.groups)} group(s) and {len(self.misc)} misc"

    
    def number_of_groups(self) -> int:
        return len(self.groups)

    
    def add_lecture(self, lecture: Lecture) -> None:
        """ Adds lecture to lectures """
        assert isinstance(lecture, Lecture)
        self.lectures.append(lecture)


    def add_misc(self, misc) -> None:
        self.misc.append(misc)

    
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
            lecture.overlaps(cal_event) 
            for lecture in self.lectures
        )
        overlap_practicals = self.groups[group].overlaps(cal_event)
        overlap_misc = any(
            misc.overlaps(cal_event)
            for misc in self.misc
        )
        return overlap_lectures or overlap_practicals or overlap_misc
