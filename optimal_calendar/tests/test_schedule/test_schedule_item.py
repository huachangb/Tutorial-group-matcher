import pytest

from datetime import datetime
from ...schedule.datetimerange import Datetimerange
from ...schedule.schedule_item import ScheduleItem

class TestScheduleItem():
    @pytest.mark.parametrize("start,hours,minutes,end,location,description", [
        (
            datetime(2020, 5, 17, 0, 0), 
            1, 
            34, 
            datetime(2020, 5, 17, 1, 34),
            "locat1",
            "descr"
        ),
        (
            datetime(2002, 5, 17, 0, 0), 
            1, 
            34, 
            datetime(2002, 5, 17, 1, 34),
            "locat2",
            "descr"
        )
    ])
    def test_init(self, start: datetime, hours: int, minutes: int, end: datetime, 
                    location: str, description: str):
        """ 
        TEST: should init similarly to Datetimerange
        """
        schedule_item = ScheduleItem(
            description=description,
            location=location,
            begin_date=start,
            hours=hours,
            minutes=minutes
        )
        assert schedule_item.end == end


    @pytest.mark.parametrize("schedule_item_1,schedule_item_2,result", [
        # starts immediately after the other
        (
            ScheduleItem("", "", datetime(2020, 5, 17, 1, 0), 1, 0), 
            ScheduleItem("", "", datetime(2020, 5, 17, 2, 0), 2, 0), 
            False
        ),
        # no overlap
        (
            ScheduleItem("", "", datetime(2020, 5, 17, 1, 0), 0, 5), 
            ScheduleItem("", "", datetime(2020, 5, 17, 2, 0), 2, 0), 
            False
        ),
        # overlap exists
        (
            ScheduleItem("", "", datetime(2020, 5, 17, 1, 0), 2, 0), 
            ScheduleItem("", "", datetime(2020, 5, 17, 2, 0), 2, 0), 
            True
        )
    ])
    def test_overlaps(self, schedule_item_1: ScheduleItem, schedule_item_2: ScheduleItem, result: bool):
        """
        TEST: overlap between two schedule items
        """
        assert schedule_item_1.overlaps(schedule_item_2) == result
        assert schedule_item_2.overlaps(schedule_item_1) == result

    
    @pytest.mark.parametrize("schedule_item,dtrange,result", [
        (
            ScheduleItem("", "", datetime(2020, 5, 17, 1, 0), 1, 0),
            Datetimerange(datetime(2020, 5, 17, 2, 0), 2, 0),
            False
        )
    ])
    def test_compatible_with_dtrange(self, schedule_item: ScheduleItem, dtrange: Datetimerange, result: bool):
        assert schedule_item.overlaps(dtrange) == result
        assert dtrange.overlaps(schedule_item) == result

    @pytest.mark.parametrize("schedule_item_1,schedule_item_2,result", [
        (
            ScheduleItem("l1", "a2", datetime(2020, 5, 17, 1, 0), 0, 5), 
            ScheduleItem("l1", "a2", datetime(2020, 5, 17, 1, 0), 0, 5), 
            True
        ),
        (
            ScheduleItem("l1", "a2", datetime(2020, 5, 17, 1, 0), 0, 5), 
            ScheduleItem("l", "a2", datetime(2020, 5, 17, 1, 0), 0, 5), 
            False
        ),
        (
            ScheduleItem("l1", "a2", datetime(2020, 5, 17, 1, 0), 0, 5), 
            ScheduleItem("l1", "a2", datetime(2020, 5, 17, 1, 0), 0, 6), 
            False
        )
    ])
    def test_eqauality(self, schedule_item_1: ScheduleItem, schedule_item_2: ScheduleItem, result: bool):
        assert (schedule_item_1 == schedule_item_2) == result
        assert (schedule_item_2 == schedule_item_1) == result
