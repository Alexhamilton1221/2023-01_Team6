class Course:
    # This is the single instance of a course
    def __init__(self, name, total_hours, prerequisites, delivery = "Class", extra_req = ""):
        # The name of the course (String)
        self.name = name
        # The total number of hours for this course (double)
        self.total_hours = total_hours
        # how many hours are left in the course (double)
        self.hours_remaining = total_hours
        # The prequisites of this course (array of courses)
        self.prerequisites = prerequisites
        # How the course is delivered (Class, Lab, Online, Virtual) (online is synchronous, Virtual is async) (String)
        self.delivery = delivery
        # Lectures the course has taken (array of lecture object)
        self.lectures = []
        # extra requirements for this course
        self.extra_req = extra_req
        # Whether the course has finished all lectures (boolean)
        self.finished = False

    def add_lecture(self, lecture):
        # Adds a new lecture to lectures
        self.hours_remaining -= lecture.length()
        self.lectures.append(lecture)
        if self.hours_remaining <= 0:
            self.finished = True

    def set_lecture_time(self, start_time, end_time):
        # This function sets the times all lectures for this course
        for lecture in self.lectures:
            lecture.start_time = start_time
            lecture.end_time = end_time

    def is_lab(self):
        return self.delivery == "Lab"

    def is_equal(self, other):
        if type(other) != Course:
            return False
        if len(self.prerequisites) != len(other.prerequisites):
            return False
        prereqs = zip(self.prerequisites, other.prerequisites)
        for prereq in prereqs:
            if not prereq[0].is_equal(prereq[1]):
                return False

        return self.name == other.name and self.total_hours == other.total_hours and self.hours_remaining == other.hours_remaining and self.delivery == other.delivery

    def __repr__(self):
        return self.name