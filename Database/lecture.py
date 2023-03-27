
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

    def time_collison_compare(self, start_time, end_time):
        # Purpose: This function checks if the time, but not the date of another lecture is in collision with tihs
        startLessThanStart = self.start_time <= start_time
        endLessThanEnd = self.end_time <= end_time
        startLessThanEnd = self.start_time < end_time
        endGreaterThanStart = self.end_time > start_time

        if self.start_time == start_time and self.end_time == end_time:
            return True
        elif startLessThanStart and endLessThanEnd and startLessThanEnd and endGreaterThanStart:
            return True
        elif not startLessThanStart and not endLessThanEnd and startLessThanEnd and endGreaterThanStart:
            return True
        elif startLessThanStart and not endLessThanEnd and startLessThanEnd and endGreaterThanStart:
            return True
        elif not startLessThanStart and endLessThanEnd and startLessThanEnd and endGreaterThanStart:
            return True

        return False


    def length(self):
        return self.end_time - self.start_time
