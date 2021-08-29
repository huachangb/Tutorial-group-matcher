from calendar_planner3.courses.lecture import Lecture
from calendar_planner3.courses.practical_lecture import PracticalLecture

class Course():
    def __init__(self, title: str) -> None:
        self.title = title
        self.lectures = []
        self.practical_lectures = {}
        self.examens = [] # maybe in the future

    
    def __len__(self):
        return len(self.practical_lectures)

        
    def add_lecture(self, lecture: Lecture) -> None:
        """ Adds lecture to lectures """
        assert isinstance(lecture, Lecture)
        self.lectures.append(lecture)
        
        
    def add_practical_lecture(self, group: str, practical_lecture: PracticalLecture) -> None:
        """ Adds practical lecture. If there is already a record of a group, 
        <practical_lecture> will be merged with this instance """
        assert isinstance(practical_lecture, PracticalLecture)
        if group not in self.practical_lectures:
            self.practical_lectures[group] = practical_lecture
            return
        self.practical_lectures[group].add_lectures(practical_lecture.schedule)

    
    def overlaps(self, time_range, group) -> bool:
        """ Checks if schedule of group overlaps with the lectures of self """
        overlap_lectures = any(lecture.overlaps_with_time_range(time_range) 
                                for lecture in self.lectures)
        overlap_practical_lectures = self.practical_lectures[group]\
                                        .overlaps_with_time_range(time_range)
        return overlap_lectures or overlap_practical_lectures
