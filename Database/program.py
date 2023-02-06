
class Program:
    def __init__(self, name):
        self.name = name

        self.stored_courses = []

    def add_course(self, stored_course):
        self.stored_courses.append(stored_course)

    def get_term_hours(self, term):
        # Gets the hours of a single term
        hours = 0
        for course in self.stored_courses:
            if course.term == term:
                hours += course.total_hours

        return hours

    def get_total_hours(self):
        # Gets the total hours of all three terms
        hours = 0
        for course in self.stored_courses:
            hours += course.total_hours

        return hours
