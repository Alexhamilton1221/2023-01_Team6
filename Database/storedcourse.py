from Database.course import Course
class StoredCourse:
    # This is the long term stored info about the course
    def __init__(self, name, total_hours, term, prerequisites, delivery = "Class"):
        # The name of the course
        self.name = name

        # How many hours are in the course
        self.total_hours = total_hours

        # The term of the course
        self.term = term

        # The prerequsits of the course
        self.prerequisites = prerequisites

        # The delivery of the course
        self.delivery = delivery
    def generate_course(self):
        return Course(self.name, self.total_hours, self.prerequisites, self.delivery)
