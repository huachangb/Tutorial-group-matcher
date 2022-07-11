import pytest

from ...calendar_structures.constants import CCollectionTypes, CEventTypes
from ...calendar_structures.course import Course
from ...calendar_structures.calendar_event import CalendarEvent
from datetime import datetime


def add_helper(func, obj1, obj2):
    # retrns True if func throws an assertion error
    try:
        func(obj1, obj2)
    except AssertionError:
        return True
    return False


class TestCourse():
    def test_init(self):
        course = Course("Test")
        assert course.lectures.type == CCollectionTypes.LECTURES
        assert course.misc.type == CCollectionTypes.OTHER
        
        for _, coll in course.practical_seminars:
            assert coll.type == CCollectionTypes.PRACTICAL_SEMINAR_GROUP


    @pytest.mark.parametrize("cal_event,should_fail", [
        (CalendarEvent(event_type=CEventTypes.PRACTICAL_SEMINAR, title="", begin_date=datetime(2020, 5, 17, 1, 0), hours=1, minutes=0), True),
        (CalendarEvent(event_type=CEventTypes.OTHER, title="", begin_date=datetime(2020, 5, 17, 1, 0), hours=1, minutes=0), True),
        (CalendarEvent(event_type=CEventTypes.LECTURE, title="", begin_date=datetime(2020, 5, 17, 1, 0), hours=1, minutes=0), False)
    ])
    def test_add_lecture(self, cal_event: CalendarEvent, should_fail: bool) -> None:
        course = Course("Test")
        assert add_helper(Course.add_lecture, course, cal_event) == should_fail

    
    @pytest.mark.parametrize("cal_event,should_fail", [
        (CalendarEvent(event_type=CEventTypes.PRACTICAL_SEMINAR, title="", begin_date=datetime(2020, 5, 17, 1, 0), hours=1, minutes=0), True),
        (CalendarEvent(event_type=CEventTypes.OTHER, title="", begin_date=datetime(2020, 5, 17, 1, 0), hours=1, minutes=0), False),
        (CalendarEvent(event_type=CEventTypes.LECTURE, title="", begin_date=datetime(2020, 5, 17, 1, 0), hours=1, minutes=0), True)
    ])
    def test_add_misc(self, cal_event: CalendarEvent, should_fail: bool) -> None:
        course = Course("Test")
        assert add_helper(Course.add_misc_event, course, cal_event) == should_fail


    @pytest.mark.parametrize("cal_event,should_fail,group", [
        (CalendarEvent(event_type=CEventTypes.PRACTICAL_SEMINAR, title="", begin_date=datetime(2020, 5, 17, 1, 0), hours=1, minutes=0), False, "A"),
        (CalendarEvent(event_type=CEventTypes.OTHER, title="", begin_date=datetime(2020, 5, 17, 1, 0), hours=1, minutes=0), True, "B"),
        (CalendarEvent(event_type=CEventTypes.LECTURE, title="", begin_date=datetime(2020, 5, 17, 1, 0), hours=1, minutes=0), True, "C")
    ])
    def test_add_practical(self, cal_event: CalendarEvent, should_fail: bool, group: str) -> None:
        course = Course("Test")
        def add_prac(obj1, obj2):
            """ wrap function, because add_practical_event requires more args than the other add methods """
            Course.add_practical_seminar_event(obj1, obj2, group)
        assert add_helper(add_prac, course, cal_event) == should_fail

    
    @pytest.mark.parametrize("cal_event,result", [
        (
            # overlaps with lecture
            CalendarEvent(event_type=CEventTypes.OTHER, title="", begin_date=datetime(2020, 5, 17, 14, 0), hours=0, minutes=20), 
            True
        ),
        (
            # overlaps with practical seminar
            CalendarEvent(event_type=CEventTypes.OTHER, title="", begin_date=datetime(2020, 5, 17, 1, 10), hours=0, minutes=5), 
            True
        ),
        (
            # overlaps with misc events
            CalendarEvent(event_type=CEventTypes.OTHER, title="", begin_date=datetime(2021, 5, 17, 14, 0), hours=0, minutes=20), 
            True
        ),
        (
            # does not overlap
            CalendarEvent(event_type=CEventTypes.OTHER, title="", begin_date=datetime(2023, 5, 17, 1, 0), hours=1, minutes=0), 
            False
        )
    ])
    def test_overlaps(self, cal_event: CalendarEvent, result: bool) -> None:
        course = Course("TEst")

        # add practical seminar
        prac_sem = CalendarEvent(
            event_type=CEventTypes.PRACTICAL_SEMINAR, 
            title="", 
            begin_date=datetime(2020, 5, 17, 1, 0), 
            hours=1, 
            minutes=0
        )
        course.add_practical_seminar_event(prac_sem, "A")

        # add some lectures and misc. events
        for i in range(5):
            lecture = CalendarEvent(
                title="",
                begin_date=datetime(2020, 5, 17 + i, 14, 0), 
                hours=1, 
                minutes=0,
                event_type=CEventTypes.LECTURE
            )
            course.add_lecture(lecture)

            misc = CalendarEvent(
                title="",
                begin_date=datetime(2021, 5, 17 + i, 14, 0), 
                hours=1, 
                minutes=0,
                event_type=CEventTypes.OTHER
            )
            course.add_misc_event(misc)

        assert course.overlaps_practical_seminar_group("A", cal_event) == result

