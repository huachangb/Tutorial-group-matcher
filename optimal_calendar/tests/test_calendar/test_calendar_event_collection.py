import pytest

from ...calendar_structures.calendar_event import CalendarEvent
from ...calendar_structures.calendar_event_collection import CalendarEventCollection
from ...calendar_structures.constants import CCollectionTypes
from datetime import datetime


def create_mock_collection(offset: int) -> CalendarEventCollection:
    events = [
        CalendarEvent(title="", begin_date=datetime(2020, 5, 17 + offset, 1, 0), hours=1, minutes=0), 
        CalendarEvent(title="", begin_date=datetime(2020, 5, 17 + offset, 2, 0), hours=2, minutes=0), 
        CalendarEvent(title="", begin_date=datetime(2020, 5, 17 + offset, 1, 0), hours=0, minutes=5), 
        CalendarEvent(title="", begin_date=datetime(2020, 5, 18 + offset, 2, 0), hours=2, minutes=0), 
        CalendarEvent(title="", begin_date=datetime(2020, 5, 19 + offset, 1, 0), hours=2, minutes=0), 
        CalendarEvent(title="", begin_date=datetime(2020, 5, 20 + offset, 2, 0), hours=2, minutes=0)
    ]
    coll = CalendarEventCollection()

    for event in events:
        coll.add_event(event)
    
    return coll


class TestCalendarEventCollection():
    def test__init__(self) -> None:
        title = "test"
        coll = CalendarEventCollection(
            title=title
        )
        assert coll.title == title
        assert coll.type == CCollectionTypes.OTHER
        assert len(coll.events) == 0
        
    
    @pytest.mark.parametrize("cal_events", [
        [
            CalendarEvent(title="", begin_date=datetime(2020, 5, 17, 1, 0), hours=1, minutes=0), 
            CalendarEvent(title="", begin_date=datetime(2020, 5, 17, 2, 0), hours=2, minutes=0), 
            CalendarEvent(title="", begin_date=datetime(2020, 5, 17, 1, 0), hours=0, minutes=5), 
            CalendarEvent(title="", begin_date=datetime(2020, 5, 17, 2, 0), hours=2, minutes=0), 
            CalendarEvent(title="", begin_date=datetime(2020, 5, 17, 1, 0), hours=2, minutes=0), 
            CalendarEvent(title="", begin_date=datetime(2020, 5, 17, 2, 0), hours=2, minutes=0)
        ]
    ])
    def test_add_event(self, cal_events: list) -> None:
        coll = CalendarEventCollection(title="Test")

        for index, cal_event in enumerate(cal_events):
            coll.add_event(cal_event)
            assert len(coll.events) == index + 1
            assert cal_event in coll
        

    def test_overlaps(self) -> None:
        coll = create_mock_collection(0)
        
        # overlap
        overlap1 = CalendarEvent(title="", begin_date=datetime(2020, 5, 17, 1, 0), hours=0, minutes=20)
        overlap2 = CalendarEvent(title="", begin_date=datetime(2020, 5, 17, 2, 0), hours=1, minutes=30)
        assert coll.overlaps(overlap1)
        assert coll.overlaps(overlap2)

        # no overlap
        no_overlap1 = CalendarEvent(title="", begin_date=datetime(2021, 5, 17, 1, 0), hours=0, minutes=20)
        no_overlap2 = CalendarEvent(title="", begin_date=datetime(2022, 5, 17, 2, 0), hours=1, minutes=30)
        assert not coll.overlaps(no_overlap1)
        assert not coll.overlaps(no_overlap2)

    
    def test_overlaps_2(self) -> None:
        coll1 = create_mock_collection(0)
        coll2 = create_mock_collection(2)
        coll3 = create_mock_collection(10)
        assert coll1.overlaps(coll2)
        assert not coll1.overlaps(coll3)
        assert coll2.overlaps(coll1)
        assert not coll2.overlaps(coll3)
        assert not coll3.overlaps(coll1)
        assert not coll3.overlaps(coll2)

    
    @pytest.mark.parametrize("dtrange,result", [
        (
            CalendarEvent(title="", begin_date=datetime(1900, 1, 1, 1, 0), hours=5, minutes=0),
            True
        ),
        (
            CalendarEvent(title="", begin_date=datetime(1900, 1, 1, 2, 0), hours=5, minutes=0),
            False
        )
    ])
    def test_in_range(self, dtrange: CalendarEvent, result: bool) -> None:
        coll = create_mock_collection(0)
        assert coll.in_range(dtrange) == result
