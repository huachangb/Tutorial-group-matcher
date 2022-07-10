import pytest

from ...schedule.datetimerange import Datetimerange
from ...schedule.schedule import Schedule
from ...schedule.schedule_item import ScheduleItem
from ...calendar.calendar_event import CalendarEvent
from datetime import datetime

def create_mock_cal_event():
    schedule_list = [
        {
            "description": "",
            "start_date": datetime(2020, 5, 17, 1, 0),
            "location": "",
            "duration_hours": 2,
            "duration_minutes": 15
        },
        {
            "description": "",
            "start_date": datetime(2020, 5, 18, 13, 0),
            "location": "",
            "duration_hours": 1,
            "duration_minutes": 0
        },
        {
            "description": "",
            "start_date": datetime(2020, 5, 18, 22, 0),
            "location": "",
            "duration_hours": 1,
            "duration_minutes": 45
        }
    ]
    cal_event = CalendarEvent(
        title="TEST",
        schedule=schedule_list,
        description="TEST_DESCR"
    )
    return cal_event, schedule_list


class TestCalendarEvent():
    def test_iter(self):
        cal_event, schedule_list = create_mock_cal_event()

        schedule_items = []

        for schedule_item in schedule_list:
            schedule_items.append(ScheduleItem(
                description=schedule_item["description"],
                begin_date=schedule_item["start_date"],
                location=schedule_item["location"],
                hours=schedule_item["duration_hours"],
                minutes=schedule_item["duration_minutes"]
            ))

        assert all(item in schedule_items for item in cal_event)

    
    def test_add(self):
        cal_event, _ = create_mock_cal_event()
        items = [
            ScheduleItem("", "", datetime(2020, 5, 17, 1, 0), 1, 0), 
            ScheduleItem("", "", datetime(2020, 5, 17, 2, 0), 2, 0)
        ]

        for item in items:
            cal_event.add_to_schedule(item)
        
        all_items = cal_event.schedule.items

        for item in items:
            assert item in all_items


    def test_add_throw(self):
        cal_event, _ = create_mock_cal_event()
        passed = True

        for item in [1, "a", cal_event]:
            try:
                cal_event.add_to_schedule(item)
                passed = False
            except AssertionError:
                continue
        
        assert passed

    def test_overlaps_dtrange(self):
        cal_event, _ = create_mock_cal_event()

        # overlap
        dtrange1 = Datetimerange(datetime(2020, 5, 17, 2, 0), 1, 0)
        assert cal_event.overlaps(dtrange1)


        # no overlap
        dtrange2 = Datetimerange(datetime(2020, 5, 19, 1, 0), 1, 0)
        assert not cal_event.overlaps(dtrange2)

    
    def test_overlaps_sched_item(self):
        cal_event, _ = create_mock_cal_event()

        # overlap
        s1 = ScheduleItem("", "", datetime(2020, 5, 17, 2, 0), 1, 0)
        assert cal_event.overlaps(s1)

        # no overlap
        s2 = ScheduleItem("", "", datetime(2020, 5, 19, 1, 0), 1, 0)
        assert not cal_event.overlaps(s2)

    def test_overlaps_sched(self):
        cal_event, items = create_mock_cal_event()

        # overlaps
        s1 = Schedule()
        for schedule_item in items[:2]: 
            s1.add_item(ScheduleItem(
                description=schedule_item["description"],
                begin_date=schedule_item["start_date"],
                location=schedule_item["location"],
                hours=schedule_item["duration_hours"],
                minutes=schedule_item["duration_minutes"]
            ))
        assert cal_event.overlaps(s1)

        # no overlap with empty schedule
        s2 = Schedule()
        assert not cal_event.overlaps(s2)

        # no overlap
        s3 = Schedule()
        s3.add_item(ScheduleItem("", "", datetime(2024, 5, 17, 2, 0), 1, 0))
        assert not cal_event.overlaps(s3)

    
    def test_overlaps_cal_event(self):
        cal_event, items = create_mock_cal_event()

        # overlaps with itself
        assert cal_event.overlaps(cal_event)

        # overlaps
        c1 = CalendarEvent("", items[:1])
        assert cal_event.overlaps(c1)
        assert c1.overlaps(cal_event)

        # no overlap: empty
        c2 = CalendarEvent("", [])
        assert not cal_event.overlaps(c2)
        assert not c2.overlaps(cal_event)

        # no overlap
        c3 = CalendarEvent("", [
            {
                "description": "",
                "start_date": datetime(2220, 5, 17, 1, 0),
                "location": "",
                "duration_hours": 2,
                "duration_minutes": 15
            }
        ])
        assert not cal_event.overlaps(c3)
        assert not c3.overlaps(cal_event)
