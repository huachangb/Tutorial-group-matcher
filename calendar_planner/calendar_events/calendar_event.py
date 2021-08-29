from calendar_planner.schedule.schedule import Schedule
from calendar_planner.schedule.schedule_item import ScheduleItem
from calendar_planner.constants import NO_GROUP
from datetime import datetime

class CalendarEvent():
    def __init__(self, title: str, schedule: list, description: str = "") -> None:
        self.title = title
        self.description = description
        self.schedule = Schedule()

        for schedule_item in schedule:
            self.add_to_schedule(
                description=schedule_item["description"],
                datetime_begin=schedule_item["start_date"],
                location=schedule_item["location"],
                duration_hours=schedule_item["duration_hours"],
                duration_minutes=schedule_item["duration_minutes"]
            )

        self.type = "General"
        self.group = NO_GROUP


    def __str__(self) -> str:
        """ print """
        return f"{self.title}, {self.type} with {len(self.schedule)} item(s)"


    def __iter__(self):
        """ Allows iterating over class """
        self.__n = 0
        self.__max = len(self.schedule)
        return self


    def __next__(self):
        """ Returns n-th element of schedule items """
        if self.__n < self.__max:
            self.__n += 1
            return self.schedule.get_item(self.__n - 1)
        else:
            raise StopIteration

    
    def add_to_schedule(self, description: str, datetime_begin: datetime, location: str, duration_hours: int, duration_minutes: int = 0) -> None:
        """ adds items to schedule """
        schedule_item = ScheduleItem(
            description=description,
            datetime_start=datetime_begin,
            location=location,
            duration_hours=duration_hours,
            duration_minutes=duration_minutes
        )
        self.schedule.add_item(schedule_item)


    def add_schedule_item(self, schedule_item: ScheduleItem) -> None:
        """ adds item to schedule """
        self.schedule.add_item(schedule_item)


    def overlaps(self, cal_event) -> bool:
        for schedule_item_self in self.schedule:
            for schedule_item_other in cal_event.schedule:
                if schedule_item_self.overlaps(schedule_item_other):
                    return True
        return False
