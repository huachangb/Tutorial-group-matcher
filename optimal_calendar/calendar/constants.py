from enum import Enum, auto

class CEventTypes(Enum):
    """
    Act likes an enum
    Types: LECTURE, PRACTICAL_SEMINAR, OTHER
    """
    LECTURE = auto()
    PRACTICAL_SEMINAR = auto()
    CUSTOM = auto()
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
