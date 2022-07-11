# Planner for finding the optimal schedule
Python module to find schedules with a minimal number of overlapping lectures. 

## This branch contains the previous version of this project. Most code has been rewritten, which is now included in the main branch. It is recommended to use the code in the main branch, although both versions should produce the same output. 

## Features
- Search for a schedule to limit the number of overlapping lectures 
- Search within a given range of time
- Adding custom events

# How to use this?
A demo in a Jupyter Notebook is included in the repository (demo excel files will be added in the future). Firstly, we need to load the timetables for each course. This can be done by reading the corresponding Excel files.

```python
# paths to files
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
```

Now, we can search for every possible schedule. This can be done by calling ```cal```'s method ```find_all_schedules```. This method takes 3 **optional** parameters and returns a Pandas DataFrame. 
- format_groups: simplifies output
- start_time = lower time limit
- end_time = upper time limit
Note that ```start_time``` and ```end_time``` should be in 24-hour notation, e.g. ```11:00```. This controls the possible schedules, such that no lecture is before <start_time> and no lecture is after <end_time>

```python
cal.find_all_schedules(
    format_groups=True, 
    start_time="10:00", 
    end_time="17:00"
)
```

## To-do
- add an option to search for a schedule that minimizes overlap (generalizing the current algorithm)
