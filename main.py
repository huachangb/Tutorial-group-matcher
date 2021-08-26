from calendar_planner import Calendar

def main():
    course_paths = {
        "databases.xlsx": "Databases INF/IK",
        "inleiding_ki.xlsx": "Inleiding kunstmatige intelligentie",
        "nwo.xlsx": "Netwerkorganisaties",
        "psas.xlsx": "Problem solving and search"
    }
    calendar = Calendar()
    calendar.add_courses_from_excel(course_paths)
    print(calendar)

if __name__ == "__main__":
    main()