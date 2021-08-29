from calendar_planner.schedule.datetime_range import DateTimeRange
from calendar_planner.schedule.schedule_item import ScheduleItem
from calendar_planner.schedule.schedule import Schedule
from calendar_planner.calendar_events.calendar_event import CalendarEvent
from calendar_planner.schedule.convert import dutch_month_to_num, parse_date, parse_datetime, parse_time, to_datetime
from calendar_planner.constants import MONTHS
from datetime import datetime

#
# TEST
# 
# convert.py
#
datetime_1 = datetime(year=2021, month=9, day=8, hour=14)
assert parse_time(datetime_1) == "14:00"
assert parse_date(datetime_1) == "2021-09-08"
assert parse_datetime(datetime_1) == "2021-09-08 14:00"
assert all(dutch_month_to_num(key) == value 
            for key, value in MONTHS.items())
assert to_datetime("8 sep 2021").date() == datetime_1.date()


#
# TEST
# 
# DateTimeRange
#
date_1 = DateTimeRange(datetime(year=2021, month=9, day=8, hour=14), 2)
date_2 = DateTimeRange(datetime(year=2021, month=9, day=8, hour=13), 2)
assert date_1.overlaps(date_2), "should overlap"
assert date_2.overlaps(date_1), "should overlap"

date_1 = DateTimeRange(datetime(year=2021, month=9, day=8, hour=14), 2)
date_2 = DateTimeRange(datetime(year=2021, month=9, day=8, hour=16), 2)
assert not date_1.overlaps(date_2), "should not overlap"
assert not date_2.overlaps(date_1), "should not overlap"

date_1 = DateTimeRange(datetime(year=2021, month=8, day=8, hour=14), 2)
date_2 = DateTimeRange(datetime(year=2021, month=8, day=9, hour=4), 2)
assert not date_1.overlaps(date_2), "should not overlap"
assert not date_2.overlaps(date_1), "should not overlap"


#
# TEST
#
# ScheduleItem 
#
schedule_item_1 = ScheduleItem(
    description="TEST",
    datetime_start=datetime(year=2021, month=8, day=8, hour=14),
    location="TEST LOC",
    duration_hours=1,
    duration_minutes=0
)
schedule_item_2 = ScheduleItem(
    description="TEST",
    datetime_start=datetime(year=2021, month=8, day=8, hour=13),
    location="TEST LOC",
    duration_hours=2,
    duration_minutes=0
)
schedule_item_3 = ScheduleItem(
    description="TEST",
    datetime_start=datetime(year=2021, month=8, day=8, hour=11),
    location="TEST LOC",
    duration_hours=2,
    duration_minutes=0
)
assert schedule_item_2.overlaps(schedule_item_1)
assert schedule_item_1.overlaps(schedule_item_2)
assert not (schedule_item_1.overlaps(schedule_item_3) and 
            schedule_item_2.overlaps(schedule_item_3))


#
# TEST
#
# Schedule 
#
schedule = Schedule()
schedule.add_item(schedule_item_1)
schedule.add_item(schedule_item_2)
schedule.add_item(schedule_item_3)
assert len(schedule) == 3

for item in schedule:
    continue

for i in range(len(schedule)):
    assert schedule.get_item(i) == schedule.items[i]

schedule_item_test_1 = ScheduleItem(
    description="TEST",
    datetime_start=datetime(year=2021, month=8, day=8, hour=10),
    location="TEST LOC",
    duration_hours=2,
    duration_minutes=0
)
schedule_item_test_2 = ScheduleItem(
    description="TEST",
    datetime_start=datetime(year=2021, month=8, day=8, hour=12),
    location="TEST LOC",
    duration_hours=2,
    duration_minutes=0
)
schedule_item_test_3 = ScheduleItem(
    description="TEST",
    datetime_start=datetime(year=2021, month=8, day=8, hour=15),
    location="TEST LOC",
    duration_hours=2,
    duration_minutes=0
)
assert schedule.overlaps(schedule_item_test_1)
assert schedule.overlaps(schedule_item_test_2)
assert not schedule.overlaps(schedule_item_test_3)

#
# TEST
#
# CalendarEvent
#

schedule_1 = [
    {
        "description": "TEST",
        "start_date": schedule_item_1.datetime_range.begin,
        "duration_hours": 1,
        "duration_minutes": 0,
        "location": "TEST"
    },
    {
        "description": "TEST",
        "start_date": schedule_item_2.datetime_range.begin,
        "duration_hours": 2,
        "duration_minutes": 0,
        "location": "TEST"
    }
]
schedule_2 = [
    {
        "description": "TEST",
        "start_date": schedule_item_3.datetime_range.begin,
        "duration_hours": 2,
        "duration_minutes": 0,
        "location": "TEST"
    }
]
schedule_3 = [
    {
        "description": "TEST",
        "start_date": schedule_item_2.datetime_range.begin,
        "duration_hours": 2,
        "duration_minutes": 0,
        "location": "TEST"
    }
]

calendar_event_1 = CalendarEvent(
    title="TEST",
    description="TEST",
    schedule=schedule_1
)
calendar_event_2 = CalendarEvent(
    title="TEST",
    description="TEST",
    schedule=schedule_2
)   
calendar_event_3 = CalendarEvent(
    title="TEST",
    description="TEST",
    schedule=schedule_3
)
assert not calendar_event_1.overlaps(calendar_event_2)
assert not calendar_event_2.overlaps(calendar_event_1)
assert calendar_event_1.overlaps(calendar_event_3)

print("All tests finished succesfully")
