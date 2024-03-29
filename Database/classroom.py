from Database.lecture import Lecture


class Classroom:
    def __init__(self, name, size, is_lab=False):
        # Name/# of Class (String)
        self.name = name
        # Student Max Capacity (Integer)
        self.size = size
        # whether the classroom is a lab (Boolean)
        self.is_lab = is_lab
        # Cohorts assigned to the Room (array of Cohorts)
        self.cohorts = []

    def __repr__(self):
        return self.name

    def check_if_lecture_fits(self, start_day, end_day, start_time, end_time):
        # This checks if a lecture fits within the classroom if it has the allotted times
        for cohort in self.cohorts:
            if cohort.courses[0].lectures[0].day % 2 != start_day % 2 or cohort.courses[0].lectures[0].day == 0:
                continue
            if self.is_lab:
                for course in cohort.courses:
                    if course.delivery == "Lab":
                        l_start = course.lectures[0].start_time
                        l_end = course.lectures[0].end_time
                        l_fDay = course.lectures[0].day
                        l_lDay = course.lectures[len(course.lectures) - 1].day

                        if Classroom.check_time_conflict(start_time, l_start, end_time, l_end):
                            if (end_day >= l_fDay >= start_day) or (start_day <= l_lDay <= end_day) or (start_day <= l_fDay and end_day >= l_lDay) or (start_day >= l_fDay and end_day <= l_lDay):
                                return False


            else:
                for course in cohort.courses:
                    if course.delivery == "Class":
                        l_start = course.lectures[0].start_time
                        l_end = course.lectures[0].end_time
                        l_fDay = course.lectures[0].day
                        l_lDay = course.lectures[len(course.lectures) - 1].day
                        if Classroom.check_time_conflict(start_time, l_start, end_time, l_end):
                            if (end_day >= l_fDay >= start_day) or (start_day <= l_lDay <= end_day) or (start_day <= l_fDay and end_day >= l_lDay) or (start_day >= l_fDay and end_day <= l_lDay):
                                return False

        return True
    @staticmethod
    def check_time_conflict(aStartTime, bStartTime, aEndTime, bEndTime):
        aGoesOverB = (aEndTime > bStartTime > aStartTime)
        bGoesOverA = (aStartTime < bEndTime < aEndTime)
        bWithinA = (aStartTime <= bStartTime and aEndTime >= bEndTime)
        aWithinB = (aStartTime >= bStartTime and aEndTime <= bEndTime)
        return aGoesOverB or bGoesOverA or bWithinA or aWithinB or (aEndTime == bEndTime and bStartTime == aStartTime)


    def add_cohort(self, cohort):
        self.cohorts.append(cohort)

    def same_name(self, name):
        return self.name == name

    def same_size(self, size):
        return self.size == size

    def has_lab(self):
        return self.is_lab

    def is_equal(self, other):
        if type(other) != Classroom:
            return False
        return self.same_name(other.name) and self.same_size(other.size) and self.is_lab == other.is_lab
