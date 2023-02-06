
class Program:
    def __init__(self, name):
        self.name = name

        self.stored_courses = []

    def add_course(self, stored_course):
        self.stored_courses.append(stored_course)

    def get_hours(self, specification=lambda course: True):
        # Gets the hours of a single term
        hours = 0
        for course in self.stored_courses:
            if specification(course):
                hours += course.total_hours

        return hours

