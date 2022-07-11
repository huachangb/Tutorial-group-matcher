"""
TODO:
- add location for later checking (SP, REC are not compatible if they're right after the other)
- properly handle edge case new year when adding all duplicating events to create a 'schedule'
- properly handle cases where events don't last whole hours
- think about whether we want that subgroups are handled as one group (e.g. A1, A2 fall both under A)
"""

from .calendar_event import CalendarEvent
from .course import Course
from .constants import CEventTypes, DEFAULT_LECTURE_TYPES_CAL, DEFAULT_PRACTICAL_SEMINAR_TYPES_CAL
from .convert import to_datetime
from datetime import timedelta

import pandas as pd

class CCalendar():
    def __init__(self, lecture_types: list = None, prac_sem_types: list = None) -> None:
        self.courses = {} # list of Course objects
        self.events = [] # list of CalendarEvent objects
        self.misc = [] # list of CalendarEventCollection objects
        self.config = {
            "lecture types": lecture_types if lecture_types != None else DEFAULT_LECTURE_TYPES_CAL,
            "practical seminar types": prac_sem_types if prac_sem_types != None else DEFAULT_PRACTICAL_SEMINAR_TYPES_CAL
        }
    

    def __str__(self) -> str:
        """ Returns description of current instance """
        return f"Calendar contains {', '.join(self.courses.keys())} and {len(self.events) + len(self.misc)} others events"

    
    def load_course_from_excel(self, path: str, title: str, ignore_type: list = None, ignore_description: list = None) -> None:
        """ Loads course from Excel file and is added to self """
        assert title not in self.courses, f"This calendar already contains a course with the name '{title}'"

        # set default values
        if ignore_type == None:
            ignore_type = list()
        if ignore_description == None:
            ignore_description = list()

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

            class_type_in_ignore = any(x in class_type for x in ignore_type)
            description_in_ignore = any(x in description for x in ignore_description)
            
            if class_type_in_ignore or description_in_ignore:
                continue

            # location = row["Locations"]
            weeks = list(map(int, row["Weeks"].split(",")))
            duration = row["Duration"]

            # parse time from hours, should also account for floats
            start_time = row["StartTime"]
            hour = int(start_time)
            minutes = int((start_time - hour) * 60)
            start_date = row["StartDate"].replace(hour=hour, minute=minutes)

            # determine event type
            event_type = CEventTypes.OTHER
            if class_type in self.config["lecture types"]:
                event_type = CEventTypes.LECTURE
            elif class_type in self.config["practical seminar types"]:
                event_type = CEventTypes.PRACTICAL_SEMINAR


            # get first week
            first_week_num = min(weeks)

            for week_number in weeks:
                cal_event = CalendarEvent(
                    title="",
                    # TODO: edge case: new year?
                    begin_date=start_date + timedelta(days=7 * (week_number - first_week_num)),
                    hours=duration,
                    minutes=0, # is this correct?
                    event_type=event_type
                )

                # add to associated collections
                if event_type == CEventTypes.PRACTICAL_SEMINAR:
                    group = row["Groups"].replace("Group ", "")

                    # fixes case where group is split into subgroups
                    if len(group) == 2:
                        group = group[0]
                    course.add_practical_seminar_event(cal_event=cal_event, group=group)
                elif event_type == CEventTypes.LECTURE:
                    course.add_lecture(cal_event)
                else:
                    course.add_misc_event(cal_event)
                
        
        self.courses[title] = course
