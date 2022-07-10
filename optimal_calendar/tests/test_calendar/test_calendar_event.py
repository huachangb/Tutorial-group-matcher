import pytest

from ...calendar.calendar_event import CalendarEvent
from datetime import datetime


class TestCalendarEvent():
    @pytest.mark.parametrize("start,hours,minutes,end", [
        (
            datetime(2020, 5, 17, 0, 0), 
            1, 
            34, 
            datetime(2020, 5, 17, 1, 34)
        ),
        (
            datetime(2002, 5, 17, 0, 0), 
            1, 
            34, 
            datetime(2002, 5, 17, 1, 34)
        )
    ])
    def test_init(self, start: datetime, hours: int, minutes: int, end: datetime):
        """ 
        TEST: init
        """
        schedule_item = CalendarEvent(
            title="test",
            description="",
            begin_date=start,
            hours=hours,
            minutes=minutes
        )
        assert schedule_item.end == end

    @pytest.mark.parametrize("schedule_item_1,schedule_item_2,result", [
        # starts immediately after the other
        (
            CalendarEvent(title="", begin_date=datetime(2020, 5, 17, 1, 0), hours=1, minutes=0), 
            CalendarEvent(title="", begin_date=datetime(2020, 5, 17, 2, 0), hours=2, minutes=0), 
            False
        ),
        # no overlap
        (
            CalendarEvent(title="", begin_date=datetime(2020, 5, 17, 1, 0), hours=0, minutes=5), 
            CalendarEvent(title="", begin_date=datetime(2020, 5, 17, 2, 0), hours=2, minutes=0), 
            False
        ),
        # overlap exists
        (
            CalendarEvent(title="", begin_date=datetime(2020, 5, 17, 1, 0), hours=2, minutes=0), 
            CalendarEvent(title="", begin_date=datetime(2020, 5, 17, 2, 0), hours=2, minutes=0), 
            True
        )
    ])
    def test_overlaps(self, schedule_item_1: CalendarEvent, schedule_item_2: CalendarEvent, result: bool):
        """
        TEST: overlap between two schedule items
        """
        assert schedule_item_1.overlaps(schedule_item_2) == result
        assert schedule_item_2.overlaps(schedule_item_1) == result


    @pytest.mark.parametrize("cal_event,result", [
        (datetime(2020, 5, 17, 0, 0), "2020-05-17 00:00"),
        (datetime(2022, 1, 12, 23, 59), "2022-01-12 23:59")
    ])
    def test_parse_datetime(self, cal_event: CalendarEvent, result: str):
        """
        TEST: parsing yyyy-mm-dd from datetime object
        """
        assert CalendarEvent.parse_datetime(cal_event) == result

    
    @pytest.mark.parametrize("dtimerange1,dtimerange2,result", [
        # fully within timerange
        (
            CalendarEvent(title="", begin_date=datetime(2020, 5, 17, 1, 0), hours=1, minutes=0), 
            CalendarEvent(title="", begin_date=datetime(2020, 5, 17, 1, 0), hours=2, minutes=0), 
            True
        ),
        # partially within timerange
        (
            CalendarEvent(title="", begin_date=datetime(2020, 5, 17, 1, 0), hours=1, minutes=0), 
            CalendarEvent(title="", begin_date=datetime(2020, 5, 17, 1, 30),hours= 2,minutes= 0), 
            False
        ),
        # not within timerange
        (
            CalendarEvent(title="", begin_date=datetime(2020, 5, 17, 1, 0), hours=1, minutes=0), 
            CalendarEvent(title="", begin_date=datetime(2020, 5, 17, 4, 0), hours=2, minutes=0), 
            False
        )
    ])
    def test_within_range(self, dtimerange1, dtimerange2, result):
        """
        TEST: check if Datimerange is between [start] and [end] CalendarEvent
        with only being concerned with hours
        """
        assert dtimerange1.in_range(dtimerange2) == result
