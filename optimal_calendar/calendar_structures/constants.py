from enum import Enum, auto


class CEventTypes(Enum):
    """ Calendar event type
    Act likes an enum. Exists in order to reduce
    the amount of inheritance used. 

    Types: LECTURE, PRACTICAL_SEMINAR, OTHER
    """
    LECTURE = auto()
    PRACTICAL_SEMINAR = auto()
    OTHER = auto()


class CCollectionTypes(Enum):
    """ Collection of events types
    
    Types: LECTURES, PRACTICAL_SEMINAR_GROUP, OTHER
    """
    LECTURES = auto()
    PRACTICAL_SEMINAR_GROUP = auto()
    OTHER = auto()


NO_GROUP = "NOGROUP"
MONTHS = {
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

DEFAULT_LECTURE_TYPES_CAL = ["hoorcollege"]
DEFAULT_PRACTICAL_SEMINAR_TYPES_CAL = ["laptopcollege", "werkcollege", "presentatie"]
