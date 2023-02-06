class Course:
    # This is the single instance of a course
    def __init__(self, name, total_hours, prerequisites, delivery = "Class"):
        self.name = name

        self.total_hours = total_hours

        self.hours_remaining = total_hours

        self.prerequisites = prerequisites

        self.delivery = delivery

        self.lectures = []

        self.finished = False
    def add_lecture(self, lecture):
        # Adds a new lecture to lectures
        self.hours_remaining -= lecture.length()
        self.lectures.append(lecture)
        if self.hours_remaining <= 0:
            self.finished = True

