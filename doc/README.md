# Documentation
The sole purpose of this document is to quickly 'relearn' the strucuture of this project for when I want to work on this project. That is, it is not meant to actually be any kind of serious documentation.

## Classes
### CalendarEvent
Any event that may appear on a calendar. It is a wrapper for a datetime range. 

Methods:
- \_\_init\_\_(title: str, begin_date: datetime, hours: int, description: str = "",  location: str = "", minutes: int = 0, event_type: int = CEventTypes.OTHER, compulsory: bool = True)
- \_\_str\_\_: allows to```print``` the event to the console
- \_\_eq\_\_: checks for equality
- parse_datetime: 
- get_time
- overlaps
- in_range


### CalendarEventCollection
A collection of CalendarEvent instances. E.g. practical seminar groups or a set of lectures.

### Course
A collection of all relevant events related to an academic course. Contains lectures, misc. events and a set of practical seminar groups with their schedules. 

### CCalendar
A collection of calendar events, courses and calendareventcollections

### Helper functions

## Search algorithms
### Clique search
The algorithm is defined in ```find_cliques_cal(cal) -> pd.DataFrame```. Edges are left out if a practical seminar group has any overlap with any calendar event of the other group.

### Generalized clique search
