
class Lecture:
    def __init__(self, day, start_time, end_time):
        # The day of the lecture (in relation to the start of the term)
        self.day = day
        # The Starting time of the lecture (double)
        self.start_time = start_time
        # The ending Time of the lecture (double)
        self.end_time = end_time


    def same_start_time(self, start_time):
        return self.start_time == start_time

    def same_end_time(self, end_time):
        return self.end_time == end_time

    def is_within(self, lecture):
        # Check if another lecture interferes with this timeslot
        if (lecture.start_time < self.end_time and lecture.end_time > self.start_time) or (lecture.start_time == self.start_time and lecture.end_time == self.end_time):
            if self.day == lecture.day:
                return True
        return False


    def length(self):
        return self.end_time - self.start_time
