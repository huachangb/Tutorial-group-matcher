from datetime import datetime
from ..constants import NO_GROUP
from ..custom_datetime import DateTimeRange, parse_date, parse_time

class ClassBase():
    def __init__(self, course_title: str, schedule: list, group: str = None) -> None:
        """ Initializes abstract class 
        
        Parameters:
            course_title: title of course,
            schedule: list of lectures (see README.md for format),
            group: group, if none NO_GROUP will be used
        """
        self.course_title = course_title
        self.group = group if group else NO_GROUP
        self.schedule = [
            {
                "description": lecture["description"],
                "time_range": DateTimeRange(lecture["start_date"], lecture["duration"]),
                "location": lecture["location"]
            } for lecture in schedule
        ]
        self.type = "General"


    def __iter__(self):
        """ Allows iterating over class """
        self.__n = 0
        self.__max = len(self.schedule)
        return self


    def __next__(self):
        """ Returns n-th element of schedules attribute """
        if self.__n < self.__max:
            self.__n += 1
            return self.schedule[self.__n - 1]
        else:
            raise StopIteration


    def add_lecture(self, description: str, start_time: datetime, duration: int, location: str) -> None:
        """ Adds a lecture to the list of lectures """
        self.schedule.append({
            "description": description,
            "time_range": DateTimeRange(start_time, duration),
            "location": location
        })


    def add_lecture_fixed(self, lecture: dict):
        """ Add an already formatted lecture to the list of lectures """
        self.schedule.append(lecture)

    
    def overlaps_with_time_range(self, time_range) -> bool:
        return any(lecture["time_range"].overlaps(time_range) 
                    for lecture in self.schedule)
