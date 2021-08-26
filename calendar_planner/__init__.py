import pandas as pd
from datetime import datetime
from .custom_datetime import DateTimeRange, parse_date, parse_time, to_datetime

class ClassEvent():
    def __init__(self, course: str, location: str, start_time: int, duration: int, date:datetime, weeks:list) -> None:
        self.course = course
        self.location = location
        self.duration = duration
        self.weeks = weeks
        self.datetime = date.replace(hour=start_time)
        self.datetime_range = DateTimeRange(self.datetime, duration)
        self.type = "General"
        
    def __str__(self):
        return f"{self.course} - {self.type}, from {parse_time(self.datetime_range.start)} to {parse_time(self.datetime_range.end)} on {parse_date(self.datetime)}"
        
class Werkcollege(ClassEvent):
    def __init__(self, group, course, location: str, start_time: int, duration: int, date:datetime, weeks:list) -> None:
        super(Werkcollege, self).__init__(course, location, start_time, duration, date, weeks)
        self.group = group
        self.type = "Werkcollege"

class Hoorcollege(ClassEvent):
    def __init__(self, course:str, location: str, start_time: int, duration: int, date:datetime, weeks:list) -> None:
        super(Hoorcollege, self).__init__(course, location, start_time, duration, date, weeks)
        self.type = "Hoorcollege"

class Course():
    def __init__(self, title):
        self.title = title
        self.hoorcolleges = []
        self.werkcolleges = []
        self.examens = [] # maybe in the future
        
    def add_hoorcollege(self, hoorcollege):
        assert isinstance(hoorcollege, Hoorcollege)
        self.hoorcolleges.append(hoorcollege)
        
        
    def add_werkcollege(self, werkcollege):
        assert isinstance(werkcollege, Werkcollege)
        self.werkcolleges.append(werkcollege)

class Calendar():
    def __init__(self):
        self.courses = {}
        self.non_group_lectures = ["Hoorcollege", "Vragenuur", "overig"]
        self.optional = ["reistijd", "optional", "nan"]
        self.exams = ["Tentamen", "Deeltoets", "Hertentamen"]
        
    def __str__(self):
        return "Calendar contains: " + ", ".join(self.courses.keys())
        
        
    def add_course(self, course):
        """ Add course to calendar """
        assert isinstance(course, Course)
        self.courses[course.title] = course
        
    
    def add_course_from_excel(self, path: str, title: str = None) -> None:
        """ Loads course from Excel file and is added to self
        
        Parameters:
            path: path to file
            title: title of course, if none path name will be used
        
        """
        cal = pd.read_excel(path)
        cal = cal.loc[:,["Type", "Description", "Groups", "Locations", "Weeks", "StartTime", "Duration", "StartDate"]]\
            .assign(Groups=cal["Groups"].str.split(", "))\
            .explode("Groups")
        cal["StartDate"] = cal["StartDate"].map(to_datetime)
        
        course = Course(title if isinstance(title, str) else path)
        
        for index, row in cal.iterrows():
            class_type = row["Type"]
            if class_type in self.exams: continue
                
            location = row["Locations"]
            weeks = row["Weeks"].split(",")
            start_time = row["StartTime"]
            duration = row["Duration"]
            start_date = row["StartDate"]
            description = row["Description"]
            description = description.lower() if isinstance(description, str) else ""
            
            
            if class_type not in self.non_group_lectures and not any(x in description for x in self.optional):
                group = row["Groups"].replace("Group ", "")
                werkcollege = Werkcollege(group, title, location, start_time, duration, start_date, weeks)
                course.add_werkcollege(werkcollege)
            else:
                hoorcollege = Hoorcollege(title, location, start_time, duration, start_date, weeks)
                course.add_hoorcollege(hoorcollege)
                
        
        self.courses[title] = course   
        
    
    def add_courses_from_excel(self, filenames: dict) -> None:
        """ Add multiple courses from a given dict. Dict must have the path as key 
        and the course title as value. If value is None, then its key will be used as
        course name"""
        for key, value in filenames.items():
            title = value if isinstance(value, str) else key 
            self.add_course_from_excel(path=key, title=title)
            
            
    
    def optimal_planning(self):
        ...
