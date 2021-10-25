from .schedule.datetime_range import DateTimeRange
from .calendar_events.course import Course
from .calendar_events.lecture import Lecture
from .calendar_events.custom_event import CustomCalendarEvent
from .calendar_events.practical_lecture import PracticalLecture
from .schedule.convert import parse_time_string, to_datetime
from .search_algorithms import search_by_cliques
from datetime import timedelta

import pandas as pd

class Calendar():
    def __init__(self, lecture_types: list, practical_types: list, ignore: list = None, ignore_description: list = None) -> None:
        self.courses = {}
        self.events = []
        
        ignore = [] if ignore == None else ignore
        ignore_description = [] if ignore_description == None else ignore_description

        self.config = {
            "lecture_types": lecture_types,
            "practical_types": practical_types,
            "ignore": ignore,
            "ignore_description": ignore_description
        }

    
    def __str__(self) -> str:
        return "Calendar contains: " + ", ".join(self.courses.keys()) + f" and {len(self.events)} other event(s)"


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

    
    def read_course_from_excel(self, path: str, title: str) -> None:
        """ Loads course from Excel file and is added to self
        
        Parameters:
            path: path to file
            title: title of course
        
        """
        assert title not in self.courses

        df = pd.read_excel(path)
        df = df.loc[:,["Type", "Description", "Groups", "Locations", "Weeks", "StartTime", "Duration", "StartDate"]]\
                    .assign(Groups=df["Groups"].str.split(", "))\
                    .explode("Groups")
        df["StartDate"] = df["StartDate"].map(to_datetime)
        
        course = Course(title)
        
        for _, row in df.iterrows():
            # parse data from row
            class_type = row["Type"].lower()
            description = row["Description"]
            description = description.lower() if isinstance(description, str) else ""

            class_type_in_ignore = any(x in class_type for x in self.config["ignore"])
            description_in_ignore = any(x in description for x in self.config["ignore_description"])
            
            if class_type_in_ignore or description_in_ignore:
                continue
                
            location = row["Locations"]
            weeks = list(map(int, row["Weeks"].split(",")))
            duration = row["Duration"]

            # parse time from hours, should also account for floats
            start_time = row["StartTime"]
            hour = int(start_time)
            minutes = int((start_time - hour) * 60)
            start_date = row["StartDate"].replace(hour=hour, minute=minutes)

            # create schedule
            first_week_num = min(weeks)
            schedule = [
                {
                    "description": description,
                    "start_date": start_date + timedelta(days=7 * (week_number - first_week_num)),
                    "duration_hours": duration,
                    "duration_minutes": 0,
                    "location": location
                } for week_number in weeks
            ]

            if class_type in self.config["lecture_types"]:
                lecture  = Lecture(
                    title=title,
                    description=description,
                    schedule=schedule
                )
                course.add_lecture(lecture)
            elif class_type in self.config["practical_types"]:
                group = row["Groups"].replace("Group ", "")

                # fix for when group is split into subgroups
                if len(group) == 2:
                    group = group[0]

                group_lecture = PracticalLecture(
                    title=title,
                    group=group,
                    description=description,
                    schedule=schedule
                )
                course.add_practical_lecture(
                    group=group,
                    practical_lecture=group_lecture
                )
            else:
                misc = CustomCalendarEvent(
                    title=class_type,
                    description=description,
                    schedule=schedule,
                    low_priority=False
                )
                course.add_misc(misc)
                
        
        self.courses[title] = course   


    def read_courses_from_excel(self, filenames: dict) -> None:
        """ Add multiple courses from a given dict. Dict must have the path as key 
        and the course title as value.
        """
        skipped = []

        for key, value in filenames.items():
            if key in self.courses:
                skipped.append(key)
                continue
            self.read_course_from_excel(path=value, title=key)

        if skipped:
            print(f"Calendar already contains: {skipped}")


    def find_all_schedules(self, format_groups: bool = False, start_time: str = None, end_time: str = None) -> pd.DataFrame:
        """ Finds all possible combinations using clique-based approach """
        df = search_by_cliques(self)

        # get all schedules between time range
        if isinstance(start_time, str) and isinstance(end_time, str):
            # create time range
            time_start = parse_time_string(start_time)
            time_end = parse_time_string(end_time)
            time_range = DateTimeRange(time_start, time_end.hour - time_start.hour)

            within_time_range = []

            # for every combination, check if within time range
            for index, row in df.iterrows():
                groups_within_range = []

                for value in row:
                    course, group = value.split("---")
                    groups_within_range.append(all(
                        schedule_item.within_range(time_range) 
                        for schedule_item in self.courses[course].groups[group].schedule
                    ))

                if all(groups_within_range):
                    within_time_range.append(index)

            df = df.loc[within_time_range,:]
            df.index = pd.RangeIndex(len(df.index))


        # removes all text except the group 
        if format_groups:
            for col in df.columns:
                df[col] = df[col].map(lambda x: x.split("---")[1])
        
        return df
