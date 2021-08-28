# Planner for finding the optimal schedule
To-do:
- Add support for exams
- Add custom events (probably, a wrapper class would be the best option)
- Support for preferences, additional constraints for finding a schedule

## Format of dates 
```json
[
    {
        "description": str,
        "start_date": datetime,
        "duration": int,
        "location": str
    }
]
```

# Usage
```python
from calendar_planner import Calendar

# dictionary of courses and path to file
course_paths = {
    "course name": "path-to-excel-file"
}

# create calendar
cal = Calendar()
cal.add_courses_from_excel(course_paths)

# get all possible combinations
cal.find_all_schedules()
```
