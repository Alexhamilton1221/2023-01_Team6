from Database.course import Course
class StoredCourse:
    # This is the long term stored info about the course
    # !!! This is NOT the object within the cohort !!!
    # This is the object within the program that is used to create each course!
    # THis object is effectively a template for the actual course and should never appear within a cohort object
    def __init__(self, name, total_hours, term, prerequisites, delivery = "Class", extra_req = ""):
        # The name of the course (String)
        self.name = name

        # How many hours are in the course (Double)
        self.total_hours = total_hours

        # The term of the course (integer)
        self.term = term

        # The prerequsits of the course (array of StoredCourse)
        self.prerequisites = prerequisites

        # The delivery of the course (string)
        self.delivery = delivery

        # Extra Non-standard requirements for a course (string)
        self.extra_req = extra_req
    def generate_course(self):
        prerequisites = []
        for course in self.prerequisites:
            prerequisites.append(course.generate_course())
        return Course(self.name, self.total_hours, prerequisites, self.delivery, self.extra_req)
