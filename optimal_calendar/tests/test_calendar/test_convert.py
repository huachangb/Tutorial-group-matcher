import pytest

from ...calendar_structures.convert import dutch_month_to_num, list_to_lower, parse_time_string, to_datetime
from datetime import datetime


def test_list_to_lower():
    l = ["A", "b", "DvD"]
    l_lower = ["a", "b", "dvd"]
    assert list_to_lower(l) == l_lower

def test_dutch_month_to_num():
    months = {
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "mei": 5,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "okt": 10,
        "nov": 11,
        "dec": 12
    }

    for month, num in months.items():
        assert dutch_month_to_num(month) == num


def test_to_dt():
    dts = [
        ("10 sep 2021", datetime(2021, 9, 10)),
        ("12 mar 2022", datetime(2022, 3, 12))
    ]

    for dt, answer in dts:
        assert to_datetime(dt) == answer

def test_parse_tstring():
    tstrings = [
        ("12:05", 12, 5),
        ("18:34", 18, 34)
    ]

    for timestr, hours, minutes in tstrings:
        dt = parse_time_string(timestr)
        assert dt.hour == hours
        assert dt.minute == minutes