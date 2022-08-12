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
