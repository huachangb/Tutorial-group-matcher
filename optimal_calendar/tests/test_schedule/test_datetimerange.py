import pytest

from datetime import datetime
from ...schedule.datetimerange import Datetimerange

class TestDatetimerange():
    @pytest.mark.parametrize("start,hours,minutes,end", [
        (datetime(2020, 5, 17, 0, 0), 1, 34, datetime(2020, 5, 17, 1, 34)),
        (datetime(2022, 5, 12, 23, 59), 0, 2, datetime(2022, 5, 13, 0, 1))
    ])
    def test_correctInit(self, start: datetime, hours: int, minutes: int, end: datetime):
        """
        TEST: initialization of Datetimerange
        """
        dtrange = Datetimerange(
            begin_date=start,
            hours=hours,
            minutes=minutes
        )
        assert dtrange.end == end


    @pytest.mark.parametrize("dtime,result", [
        (datetime(2020, 5, 17, 0, 0), "2020-05-17 00:00"),
        (datetime(2022, 1, 12, 23, 59), "2022-01-12 23:59")
    ])
    def test_parse_datetime(self, dtime: datetime, result: str):
        """
        TEST: parsing yyyy-mm-dd from datetime object
        """
        assert Datetimerange.parse_datetime(dtime) == result


    @pytest.mark.parametrize("dtrange1,dtrange2,result", [
        # starts immediately after the other
        (
            Datetimerange(datetime(2020, 5, 17, 1, 0), 1, 0), 
            Datetimerange(datetime(2020, 5, 17, 2, 0), 2, 0), 
            False
        ),
        # no overlap
        (
            Datetimerange(datetime(2020, 5, 17, 1, 0), 0, 5), 
            Datetimerange(datetime(2020, 5, 17, 2, 0), 2, 0), 
            False
        ),
        # overlap exists
        (
            Datetimerange(datetime(2020, 5, 17, 1, 0), 2, 0), 
            Datetimerange(datetime(2020, 5, 17, 2, 0), 2, 0), 
            True
        )
    ])
    def test_overlaps(self, dtrange1: Datetimerange, dtrange2: Datetimerange, result: bool):
        """
        TEST: check if overlap exists given two Datetimeranges
        """
        assert dtrange1.overlaps(dtrange2) == result
        assert dtrange2.overlaps(dtrange1) == result


    @pytest.mark.parametrize("dtimerange1,dtimerange2,result", [
        # fully within timerange
        (
            Datetimerange(datetime(2020, 5, 17, 1, 0), 1, 0), 
            Datetimerange(datetime(2020, 5, 17, 1, 0), 2, 0), 
            True
        ),
        # partially within timerange
        (
            Datetimerange(datetime(2020, 5, 17, 1, 0), 1, 0), 
            Datetimerange(datetime(2020, 5, 17, 1, 30), 2, 0), 
            False
        ),
        # not within timerange
        (
            Datetimerange(datetime(2020, 5, 17, 1, 0), 1, 0), 
            Datetimerange(datetime(2020, 5, 17, 4, 0), 2, 0), 
            False
        )
    ])
    def test_within_range(self, dtimerange1, dtimerange2, result):
        """
        TEST: check if Datimerange is between [start] and [end] Datetimerange
        with only being concerned with hours
        """
        assert dtimerange1.within_range(dtimerange2) == result


    @pytest.mark.parametrize("dtrange1,dtrange2,result", [
        (
            Datetimerange(datetime(2020, 5, 17, 1, 0), 1, 0),
            Datetimerange(datetime(2020, 5, 17, 1, 0), 1, 0),
            True
        ),
        (
            Datetimerange(datetime(2020, 5, 17, 1, 0), 1, 0),
            Datetimerange(datetime(2020, 5, 17, 1, 0), 1, 1), 
            False
        )
    ])
    def test_equality(self, dtrange1: Datetimerange, dtrange2: Datetimerange, result: bool):
        assert (dtrange1 == dtrange2) == result
        assert (dtrange2 == dtrange1) == result