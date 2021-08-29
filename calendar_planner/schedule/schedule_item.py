from datetime import datetime
from ..schedule.datetime_range import DateTimeRange

class ScheduleItem():
    def __init__(self, description: str, datetime_start: datetime, location: str, duration_hours: int, duration_minutes: int = 0) -> None:
        self.description = description
        self.datetime_range = DateTimeRange(datetime_start, duration_hours, duration_minutes)
        self.location = location


    def __str__(self) -> str:
        description_txt = self.description if self.description else "N/A description"
        return f"{description_txt} at {self.location} on " + self.datetime_range.__str__()

    
    def overlaps(self, schedule_item) -> bool:
        return self.datetime_range.overlaps(schedule_item.datetime_range)