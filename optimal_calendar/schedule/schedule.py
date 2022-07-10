""" Contains the definition for the Schedule class """

from __future__ import annotations
from typing import Union
from itertools import product
from .schedule_item import ScheduleItem
from .datetimerange import Datetimerange

class Schedule():
    """ Defines a schedule """
    def __init__(self) -> None:
        """ Initializes instance """
        self.__items = []
        self.__n = 0
        self.__max = 0


    def __len__(self) -> int:
        """ Number of items """
        return len(self.__items)


    def __iter__(self) -> Schedule:
        """ Allows iterating over class """
        self.__n = 0
        self.__max = len(self.__items)
        return self


    def __next__(self) -> ScheduleItem:
        """ Returns n-th element of schedule items """
        if self.__n < self.__max:
            self.__n += 1
            return self.__items[self.__n - 1]
        raise StopIteration


    @property
    def items(self) -> list:
        """ Returns all schedule items """
        return self.__items


    def get_item(self, index: int) -> ScheduleItem:
        """ Get schedule item by index """
        return self.__items[index]


    def add_item(self, item: ScheduleItem) -> None:
        """ Adds schedule item """
        assert isinstance(item, ScheduleItem)
        self.__items.append(item)


    def overlaps(self, value: Union[Datetimerange, ScheduleItem, Schedule]) -> bool:
        """
        Returns true if there exists a schedule item of [self] and
        a schedule item of [schedule] or [value], such that there is overlap.
        Else, return False
        """
        items = [value] if isinstance(value, (Datetimerange, ScheduleItem)) else value.items
        return any(map(
            lambda pair: ScheduleItem.overlaps(*pair),
            product(items, self.__items)
        ))
