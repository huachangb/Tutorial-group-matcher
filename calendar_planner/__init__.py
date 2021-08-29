from calendar_planner.calendar_events.course import Course
from calendar_planner.calendar_events.lecture import Lecture
from calendar_planner.calendar_events.practical_lecture import PracticalLecture
from calendar_planner.schedule.convert import to_datetime
from datetime import timedelta
import pandas as pd

class Calendar():
    def __init__(self, lecture_types: list = [], optional: list = [], ignore: list = [], ignore_description: list = []) -> None:
        self.courses = {}
        self.events = []
        self.config = {
            "lecture_types": lecture_types,
            "optional": optional,
            "ignore": ignore,
            "ignore_description": ignore_description
        }

    
    def __str__(self) -> str:
        return "Calendar contains: " + ", ".join(self.courses.keys())


    def list_courses(self) -> list:
        """ Returns list of courses """
        return list(self.courses.keys())

    
    def number_of_courses(self) -> int:
        """ Returns number of courses """
        return len(self.courses)


    def number_of_events(self) -> int:
        """ Returns number of events, exluding courses """
        return len(self.events)


    def add_course(self, course) -> None:
        """ Adds course to calendar """
        assert isinstance(course, Course)
        assert course.title not in self.courses
        self.courses[course.title] = course

    
    def add_course_from_excel(self, path: str, title: str) -> None:
        """ Loads course from Excel file and is added to self
        
        Parameters:
            path: path to file
            title: title of course
        
        """
        df = pd.read_excel(path)
        df = df.loc[:,["Type", "Description", "Groups", "Locations", "Weeks", "StartTime", "Duration", "StartDate"]]\
                    .assign(Groups=df["Groups"].str.split(", "))\
                    .explode("Groups")
        df["StartDate"] = df["StartDate"].map(to_datetime)
        
        course = Course(title)
        
        for _, row in df.iterrows():
            class_type = row["Type"]
            if class_type in self.config["ignore"]: continue
                
            location = row["Locations"]
            weeks = row["Weeks"].split(",")
            duration = row["Duration"]
            start_date = row["StartDate"].replace(hour=row["StartTime"])
            description = row["Description"]
            description = description.lower() if isinstance(description, str) else ""

            if description in self.config["ignore_description"]:
                continue

            schedule = [
                {
                    "description": description,
                    "start_date": start_date + timedelta(days=7 * int(week_number)),
                    "duration_hours": duration,
                    "duration_minutes": 0,
                    "location": location
                } for week_number in weeks
            ]

            # leftover
            
            if class_type not in self.non_group_lectures and not any(x.lower() in description for x in self.optional):
                group = row["Groups"].replace("Group ", "")
                practical = PracticalLecture(title, schedule, group)
                course.add_practical_lecture(group, practical)
            else:
                lecture = Lecture(title, schedule)
                course.add_lecture(lecture)
                
        
        self.courses[title] = course   
