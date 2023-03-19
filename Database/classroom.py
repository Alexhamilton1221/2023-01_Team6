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
            if self.is_lab:
                for course in cohort.courses:
                    if course.delivery == "Lab":
                        start_lecture = course.lectures[0]
                        end_lecture = course.lectures[len(course.lectures) - 1]
                        for day in range(start_day, end_day + 1, 2):
                            comp_lecture = Lecture(day, start_time, end_time)
                            if comp_lecture.is_within(start_lecture) or comp_lecture.is_within(end_lecture):
                                return False

            else:
                for course in cohort.courses:
                    if course.delivery == "Class":
                        start_lecture = course.lectures[0]
                        end_lecture = course.lectures[len(course.lectures) - 1]
                        for day in range(start_day, end_day + 1, 2):
                            comp_lecture = Lecture(day, start_time, end_time)
                            if comp_lecture.is_within(start_lecture) or comp_lecture.is_within(end_lecture):
                                return False

        return True

    def check_for_conflict(self):
        for cohort in self.cohorts:
            for course in cohort.courses:
                for lecture in course.lectures:
                    for cohort2 in self.cohorts:
                        if cohort != cohort2:
                            for course2 in cohort2.courses:
                                if course.delivery == course2.delivery:
                                    for lecture2 in course2.lectures:
                                        if lecture.day == lecture2.day and lecture.start_time == lecture2.start_time and lecture.end_time == lecture2.end_time:
                                            return (course, course2)

        return None
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



