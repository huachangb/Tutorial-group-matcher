""" Contains code for course class """

from .constants import CCollectionTypes, CEventTypes
from .calendar_event_collection import CalendarEventCollection
from .calendar_event import CalendarEvent
import copy


class Course():
    """ Structure to handle lectures, practical seminar groups and misc. events
    
    Methods:
        __init__
        __str__
        lectures
        misc
        practical_seminars
        add_lecture
        add_misc_event
        add_practical_seminar_event
        overlaps_practical_seminar_group
    """
    def __init__(self, title: str) -> None:
        self.title = title
        self.__lectures = CalendarEventCollection(title="Lectures", collection_type=CCollectionTypes.LECTURES)
        self.__misc = CalendarEventCollection(title="Misc", collection_type=CCollectionTypes.OTHER)
        self.__practical_seminars = {}
    
    
    def __str__(self) -> str:
        """ Returns description of instance """
        return f"{self.title}, with {len(self.lectures)} lecture(s), {len(self.groups)} group(s) and {len(self.misc)} misc. events"


    @property
    def lectures(self):
        """ Returns list of lectures """
        return self.__lectures.copy()


    @property
    def misc(self):
        """ Returns misc. events """
        return self.__misc.copy()


    @property
    def practical_seminars(self):
        """ Returns all practical seminar groups and their events """
        return copy.deepcopy(self.__practical_seminars)


    def add_lecture(self, cal_event: CalendarEvent) -> None:
        """ Adds lecture """
        assert cal_event.type == CEventTypes.LECTURE
        self.__lectures.add_event(cal_event)


    def add_misc_event(self, cal_event: CalendarEvent) -> None:
        """ Adds misc event """
        assert cal_event.type == CEventTypes.OTHER
        self.__misc.add_event(cal_event)
    

    def add_practical_seminar_event(self, cal_event: CalendarEvent, group: str) -> None:
        """ Adds event to practical seminar group. If group does not exist yet, create entry """
        assert cal_event.type == CEventTypes.PRACTICAL_SEMINAR
        
        if group not in self.__practical_seminars:
            self.__practical_seminars[group] = CalendarEventCollection(
                title=f"Group {group}",
                collection_type=CCollectionTypes.PRACTICAL_SEMINAR_GROUP,
                collection_id=group
            )

        self.__practical_seminars[group].add_event(cal_event)


    def overlaps_practical_seminar_group(self, group: str, cal_event: CalendarEvent) -> bool:
        """
        Returns True if <cal_event> overlaps with the schedule of <group>. Else, returns False.
        Compatability with a practical seminar group is checked. However, we are not interested
        in <group> if <cal_event> is not compatible with the lectures or misc events. 
        """
        overlap_lectures = any(
            cal_event.overlaps(lecture) 
            for lecture in self.__lectures
        )
        overlap_practical_group =  self.__practical_seminars[group].overlaps(cal_event)
        overlap_misc = any(
            cal_event.overlaps(misc_event)
            for misc_event in self.__misc
        )
        return overlap_lectures or overlap_practical_group or overlap_misc
