import pytest

from ...calendar.practical_seminar import PracticalSeminar
from datetime import datetime

def create_mock_practical_seminar():
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
    cal_event = PracticalSeminar(
        title="TEST",
        group="TEST1",
        schedule=schedule_list,
        description="TEST_DESCR"
    )
    return cal_event, schedule_list


class TestPracticalSeminar():
    def test_add_lectures(self):
        ps, _ = create_mock_practical_seminar()
        length = len(ps)

        ps.add_lectures(ps)
        assert len(ps) == 2 * length
