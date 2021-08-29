from datetime import datetime
from calendar_planner.schedule.datetime_range import DateTimeRange

class ScheduleItem():
    def __init__(self, description: str, datetime_start: datetime, location: str, duration_hours: int, duration_minutes: int = 0) -> None:
        self.description = description
        self.datetime_range = DateTimeRange(datetime_start, duration_hours, duration_minutes)
        self.location = location
    
    def overlaps(self, schedule_item) -> bool:
        return self.datetime_range.overlaps(schedule_item.datetime_range)