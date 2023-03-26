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
        # Checks if a lecuture fits in the classroom
        # for cohort in self.cohorts:
        #     if self.is_lab:
        #         for course in cohort.courses:
        #             for l_lecture in course.lectures:
        #                 if course.delivery == "Lab" and l_lecture.is_within(lecture):
        #                     return False
        #
        #     else:
        #         for course in cohort.courses:
        #             for l_lecture in course.lectures:
        #                 if course.delivery == "Class" and l_lecture.is_within(lecture):
        #                     return False
        #
        # return True

        # Checks if a lecture fits in a period of time
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

                        if (end_time > l_start > start_time) or (start_time < l_end < end_time) or (start_time < l_start and end_time > l_end) or (start_time > start_time and end_time < l_end) or(end_time == l_end and l_start == start_time):
                            if (end_day >= l_fDay >= start_day) or (start_day <= l_lDay <= end_day) or (start_day <= l_fDay and end_day >= l_lDay) or (start_day >= l_fDay and end_day <= l_lDay):
                                return False


            else:
                for course in cohort.courses:
                    if course.delivery == "Class":
                        l_start = course.lectures[0].start_time
                        l_end = course.lectures[0].end_time
                        l_fDay = course.lectures[0].day
                        l_lDay = course.lectures[len(course.lectures) - 1].day
                        if (end_time > l_start > start_time) or (start_time < l_end < end_time) or (start_time < l_start and end_time > l_end) or (start_time > start_time and end_time < l_end) or (end_time == l_end and l_start == start_time):
                            if (end_day >= l_fDay >= start_day) or (start_day <= l_lDay <= end_day) or (start_day <= l_fDay and end_day >= l_lDay) or (start_day >= l_fDay and end_day <= l_lDay):
                                return False

        return True

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
