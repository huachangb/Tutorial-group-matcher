# Planner for finding the optimal schedule for courses at the UvA [deprecated]
Python module to find schedules with a minimal number of overlapping lectures.

## Features
- Search for a schedule to limit the number of overlapping lectures 
- Search within a given range of time

# How to use this?
A demo in a Jupyter Notebook is included in the repository (demo excel files will be added in the future). Firstly, we need to load the timetables for each course. This can be done by reading the corresponding Excel files. A simple example is included here, however, more advanced usage is shown in the demo.

```python
from optimal_calendar import CCalendar

cal = CCalendar()
cal.load_course_from_excel(path="path to file", title="course 1")
cal.load_course_from_excel(path="path to another file", title="course 2")

results = cal.find_all_schedules() # results is an instance of a Pandas DataFrame
results.head(10)
```
