import pytest

from datetime import datetime
from ...calendar.custom_event import CustomCalendarEvent

def create_mock_cust_cal_event(prio: bool):
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
    cal_event = CustomCalendarEvent(
        title="TEST",
        schedule=schedule_list,
        description="TEST_DESCR",
        low_priority=prio
    )
    return cal_event, schedule_list


class TestCustomCalendarEvent():
    def test_low_prio(self):
        c1, _ = create_mock_cust_cal_event(True)
        c2, _ = create_mock_cust_cal_event(False)
        assert not c1.overlaps(c2)
        assert not c2.overlaps(c1)

    def test_high_prio(self):
        c1, _ = create_mock_cust_cal_event(False)
        assert c1.overlaps(c1)
        
