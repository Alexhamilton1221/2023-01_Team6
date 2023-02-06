# TEMP, DO NOT COMMIT
class Program:
    def __init__(self, name):
        self.name = name

        self.stored_courses = []

    def add_course(self, stored_course):
        self.stored_courses.append(stored_course)
