
class Lecture:
    def __init__(self, classroom, start_time, end_time):

        # The Classroom that the lecture is in
        self.classroom = classroom
        # The Starting time of the lecture
        self.start_time = start_time
        # The ending Time of the lecture
        self.end_time = end_time


    def same_classroom(self, classroom):
        return self.classroom == classroom

    def same_start_time(self, start_time):
        return self.start_time == start_time

    def same_end_time(self, end_time):
        return self.end_time == end_time

    def is_within(self, lecture):
        # Check if another lecture interferes with this timeslot
        if lecture.start_time < self.end_time and lecture.end_time > self.start_time:
            return True
        return False

    def length(self):
        return self.end_time - self.start_time
