# Planner for finding the optimal schedule
To-do:
- Add support for exams
- Add custom events (probably, a wrapper class would be the best option)
- Support for preferences, additional constraints for finding a schedule

## Format of dates 
```json
[
    {
        "description": "", // must be a string
        "start_date": "", // must be a datetime object
        "duration_hours": 0, // must be an int
        "duration_minutes": 0, // must be an int 
        "location": "" // must be a string
    }
]
```

# Usage
```python
# path to files
course_paths = {
    "course name": "path to file"
}

# configuration
lecture_types = ["hoorcollege"] # hoorcolleges etc
practical_types = ["laptopcollege", "werkcollege", "presentatie"] # variabele colleges, zoals werkcolleges
ignore = [] # type college om te negeren 
ignore_description = ["optional", "reistijd"] # negeer college als deze in beschrijving voorkomen

# create calendar 
cal = Calendar(
    lecture_types=lecture_types, 
    practical_types=practical_types,
    ignore=ignore,
    ignore_description=ignore_description
)
cal.read_courses_from_excel(course_paths)

# get all possible combinations
cal.find_all_schedules()
```
