import pytest

from datetime import datetime
from ...schedule.datetimerange import Datetimerange
from ...schedule.schedule_item import ScheduleItem
from ...schedule.schedule import Schedule


def create_mock_schedule() -> Schedule:
    schedule = Schedule()
    items = [
        ScheduleItem("", "", datetime(2020, 5, 17, 1, 0), 1, 0), 
        ScheduleItem("", "", datetime(2020, 5, 17, 2, 0), 2, 0), 
        ScheduleItem("", "", datetime(2020, 5, 19, 20, 0), 2, 30), 
    ]
    
    for item in items:
        schedule.add_item(item)
    
    return schedule, items


class TestSchedule():
    def test_add_items(self):
        """
        TEST: add items to schedule
        """
        schedule = Schedule()

        def test_correct_add():
            item = ScheduleItem("", "", datetime(2020, 5, 17, 1, 0), 1, 0)
            schedule.add_item(item)
            assert schedule.get_item(0) == item
        
        def test_incorrect_add():
            """
            Handles incorrect adds correctly
            """
            passed = True
            
            for item in [1, 'e', Schedule()]:
                try:
                    schedule.add_item(item)
                    passed = False
                except AssertionError:
                    continue
            
            assert passed

            
        test_correct_add()
        test_incorrect_add()
        
    
    def test_get_item(self):
        schedule, correct_items = create_mock_schedule()

        def correct(schedule, correct_items):
            """ Should be able to get all items back """
            for i in range(len(schedule)):
                assert schedule.get_item(i) in correct_items


        def incorrect(schedule):
            """ Should not be able to go out of index """
            passed = False

            try:
                schedule.get_item(9)
            except IndexError:
                passed = True
            
            assert passed

        correct(schedule, correct_items)
        incorrect(schedule)


    def test_items(self):
        """
        TEST: items prop
        """
        schedule, correct_items = create_mock_schedule()
        assert schedule.items == correct_items


    def test_len(self):
        """
        TEST: len()
        """
        schedule, _ = create_mock_schedule()
        assert len(schedule) == 3

    
    def test_iter(self):
        """
        TEST: itering over schedule
        """
        schedule, items = create_mock_schedule()
        assert all(item in items for item in schedule)


    def test_overlaps(self):
        """
        TEST overlap, with another schedule and scheduleitem
        """
        schedule, _ = create_mock_schedule()

        def other_schedule(schedule):
            # no overlap with empty schedule
            s_2 = Schedule()
            assert not schedule.overlaps(s_2)
            assert not s_2.overlaps(schedule)

            # no overlap with schedule that has no overlapping events
            s_3 = Schedule()
            items = [
                ScheduleItem("", "", datetime(2020, 6, 17, 1, 0), 1, 0), 
                ScheduleItem("", "", datetime(2020, 2, 17, 2, 0), 2, 0), 
                ScheduleItem("", "", datetime(2020, 1, 19, 20, 0), 2, 30), 
            ]
            for item in items: s_3.add_item(item)

            assert not schedule.overlaps(s_3)
            assert not s_3.overlaps(schedule)

            # overlap
            s_4 = Schedule()
            s_4.add_item(ScheduleItem("", "", datetime(2020, 5, 17, 1, 0), 1, 0))
            assert s_4.overlaps(schedule)
            assert schedule.overlaps(s_4)


        def sched_item(schedule):
            # overlap
            sched_item_1 = ScheduleItem("", "", datetime(2020, 5, 17, 1, 0), 1, 0)
            assert schedule.overlaps(sched_item_1)

            # no overlap
            sched_item_1 = ScheduleItem("", "", datetime(2020, 6, 17, 1, 0), 1, 0)
            assert not schedule.overlaps(sched_item_1)

        
        def dtrange(schedule):
            # overlap
            sched_item_1 = Datetimerange(datetime(2020, 5, 17, 1, 0), 1, 0)
            assert schedule.overlaps(sched_item_1)

            # no overlap
            sched_item_1 = Datetimerange(datetime(2020, 6, 17, 1, 0), 1, 0)
            assert not schedule.overlaps(sched_item_1)

        
        other_schedule(schedule)
        sched_item(schedule)
        dtrange(schedule)

