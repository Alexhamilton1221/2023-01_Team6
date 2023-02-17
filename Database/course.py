class Course:
    # This is the single instance of a course
    def __init__(self, name, total_hours, prerequisites, delivery = "Class"):
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
        # Whether the course has finished all lectures (boolean)
        self.finished = False

    def add_lecture(self, lecture):
        # Adds a new lecture to lectures
        self.hours_remaining -= lecture.length()
        self.lectures.append(lecture)
        if self.hours_remaining <= 0:
            self.finished = True
    def is_lab(self):
        return self.delivery == "Lab"

