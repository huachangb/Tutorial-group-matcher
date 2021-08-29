from calendar_planner.schedule.schedule_item import ScheduleItem

class Schedule():
    def __init__(self) -> None:
        self.items = []


    def __len__(self) -> int:
        return len(self.items)

    
    def __iter__(self):
        """ Allows iterating over class """
        self.__n = 0
        self.__max = len(self.items)
        return self


    def __next__(self):
        """ Returns n-th element of schedule items """
        if self.__n < self.__max:
            self.__n += 1
            return self.items[self.__n - 1]
        else:
            raise StopIteration

    
    def get_item(self, index: int) -> ScheduleItem:
        return self.items[index]


    def add_item(self, item: ScheduleItem) -> None:
        assert isinstance(item, ScheduleItem)
        self.items.append(item)


    def overlaps(self, schedule_item: ScheduleItem) -> bool:
        for schedule_item_ in self.items:
            if schedule_item.overlaps(schedule_item_):
                return True
        return False
