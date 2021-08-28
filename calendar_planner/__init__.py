import pandas as pd
from datetime import timedelta
from calendar_planner.custom_datetime import to_datetime
from calendar_planner.courses.lecture import Lecture
from calendar_planner.courses.practical_lecture import PracticalLecture
from calendar_planner.courses.course import Course

class Calendar():
    def __init__(self):
        self.courses = {}
        self.non_group_lectures = ["Hoorcollege", "Vragenuur", "overig"]
        self.optional = ["reistijd", "optional", "nan"]
        self.exams = ["Tentamen", "Deeltoets", "Hertentamen"]
        
    def __str__(self):
        return "Calendar contains: " + ", ".join(self.courses.keys())

    
    def __len__(self):
        return len(self.courses.keys())


    def list_courses(self):
        return list(self.courses.keys())
        
        
    def add_course(self, course):
        """ Add course to calendar """
        assert isinstance(course, Course)
        assert course.title not in self.courses
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
        
        for _, row in cal.iterrows():
            class_type = row["Type"]
            if class_type in self.exams: continue
                
            location = row["Locations"]
            weeks = row["Weeks"].split(",")
            duration = row["Duration"]
            start_date = row["StartDate"].replace(hour=row["StartTime"])
            description = row["Description"]
            description = description.lower() if isinstance(description, str) else ""
            schedule = [
                {
                    "description": description,
                    "start_date": start_date + timedelta(days=7 * i),
                    "duration": duration,
                    "location": location
                } for i, _ in enumerate(weeks)
            ]
            
            if class_type not in self.non_group_lectures and not any(x.lower() in description for x in self.optional):
                group = row["Groups"].replace("Group ", "")
                practical = PracticalLecture(title, schedule, group)
                course.add_practical_lecture(group, practical)
            else:
                lecture = Lecture(title, schedule)
                course.add_lecture(lecture)
                
        
        self.courses[title] = course   
        
    
    def add_courses_from_excel(self, filenames: dict) -> None:
        """ Add multiple courses from a given dict. Dict must have the path as key 
        and the course title as value. If value is None, then its key will be used as
        course name"""
        for key, value in filenames.items():
            title = value if isinstance(value, str) else key 
            self.add_course_from_excel(path=key, title=title)
            