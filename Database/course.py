class Course:
    # This is the single instance of a course
    def __init__(self, name, total_hours, prerequisites, delivery = "Class"):
        # The name of the course
        self.name = name
        # The total number of hours for this course
        self.total_hours = total_hours
        # how many hours are left in the course
        self.hours_remaining = total_hours
        # The prequisites of this course
        self.prerequisites = prerequisites
        # How the course is delivered (Class, Lab, Online, Or Virtual) (online is synchronous, Virtual is async)
        self.delivery = delivery
        # Lectures the course has taken
        self.lectures = []
        # Wether the course has finished all lectures
        self.finished = False

    def add_lecture(self, lecture):
        # Adds a new lecture to lectures
        self.hours_remaining -= lecture.length()
        self.lectures.append(lecture)
        if self.hours_remaining <= 0:
            self.finished = True
    def is_lab(self):
        return self.delivery == "Lab"

