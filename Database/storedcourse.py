from Database.course import Course
import re

class StoredCourse:
    # This is the long term stored info about the course
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
        return Course(self.name, self.total_hours, prerequisites, self.delivery)

    #returns value for lecture length from extra_req value from storedcourse object
    def lecture_length(self):
        length_of_lecture = self.extra_req
        #Brian: not all stored lectures have a lecture length, not sure what to do when that happens
        if length_of_lecture[0] == "H":
            #checking if extra req has H
            length = re.search('=(.+?)h',length_of_lecture)
            return float(length.group(1))
        else:
            return None
    def number_of_lectures(self):
        number_of_lectures = self.total_hours / self.lecture_length()
        return number_of_lectures
