import pytest

###################################################
# datetime_range.py
###################################################

from ../calendar_planner/schedule import schedule
from datetime import datetime

class DateTimeRangeTest():
    @pytest.mark.parametrize("start,hours,minutes,end", [
                (datetime(2020, 5, 17, 0,0 ), 1, 34, datetime(2020, 5, 17, 1, 34)),
                (datetime(2020, 5, 17, 0,0 ), 1, 34, datetime(2020, 5, 17, 1, 34))])
    def correctInit(self, start, hours, minutes, end):
        ...
