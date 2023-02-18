import math

from Database.classrooms import Classrooms
from Database.cohort import Cohort
from calc_space import get_hours
from calc_space import get_FullStack_hours


class Cohorts:

    def __init__(self, cohorts=[]):
        # The cohorts of the database (array of cohort)
        self.cohorts = cohorts

    @staticmethod
    def __read_students__(students):
        # Turns a array of students with the format [("PCOM 1", 54) -> ["PCOM", 1, 54] and sorts it
        # format is [program, term, students]
        termed_students = []
        for groups in students:
            group = groups[0].split()
            termed_students.append([group[0], int(group[1]), groups[2]])

        termed_students.sort(key=lambda program_count: program_count[2], reverse=True)
        return termed_students

    def create_cohorts(self, classrooms, programs, students):
        # Given an amount of classrooms in the classrooms object
        # programs from the programs object
        # students: a list of students in the format [("PROGRAM-NAME TERM", COUNT)]
        # Ex: [("PCOM 1", 54),("PCOM 2", 45), ("PCOM 3", 81), ("PC 2", 32)]

        # This is sorting the list of students from largest to smallest amount of students
        termed_students = self.__read_students__(students)
        # These are the sorted lists of classrooms by their size from largest to smallest
        classes_by_size, labs_by_size = Classrooms.rooms_by_size(classrooms)

        # These are lists of all the classrooms sizes by themselves, Ex [40, 36, 30, 24]
        class_sizes = []
        lab_sizes = []
        # These are list all the classrooms by the hours stored within
        classroom_hours = []
        lab_hours = []

        # This creates a separate list containing the classrooms hours for core (left) and program (right)
        # As cohorts are assigned the amount of spare hours will be decreased
        for room in classes_by_size:
            # FORMAT [ROOM, CORE HOURS, PROGRAM HOURS]
            classroom_hours.append([room, get_hours(), get_hours()])
            if room.size not in class_sizes:
                class_sizes.append(room.size)

        # This creates a separate list containing the lab hours for core (left) and program (right), with extra hours
        # that full stack classes get on the far right.
        # As cohorts are assigned the amount of spare hours will be decreased
        for room in labs_by_size:
            # FORMAT [ROOM, CORE HOURS, PROGRAM HOURS, FULL STACK ONLY HOURS]
            lab_hours.append([room, get_hours(), get_hours(), get_FullStack_hours()])
            if room.size not in class_sizes:
                lab_sizes.append(room.size)

        # This goes through all grouping of students
        for unsorted_students in termed_students:
            # loops while the students have not been split into cohorts
            split = False
            while not split:
                # Goes for all sizes of classrooms in class_sizes
                for size in class_sizes:
                    # Multiplies by 0.9 to leave extra room inside cohorts
                    cohort_count = math.ceil((unsorted_students[2] / (size * 0.9)))

                    # This gets how many hours of coursework will be needed by the course, and gets them for only
                    # classes in classrooms
                    class_hours = programs.get_program(lambda program: program.name == unsorted_students[0]).get_hours(
                        lambda course: not course.is_lab())



    def add_cohort(self, cohort):
        # Adds a new cohort to the list
        self.cohorts.append(cohort)

    def get_cohort(self, specification):
        # Finds a cohort with the following specification
        for a_cohort in self.cohorts:
            if specification(a_cohort):
                return a_cohort
        return None

    def get_cohorts(self, specification):
        # Finds rooms with the following specification
        cohorts = []
        for a_cohort in self.cohorts:
            if specification(a_cohort):
                cohorts.append(a_cohort)
        return cohorts

    def show_cohorts(self):
        # Shows hours separated by information
        for a_cohort in self.cohorts:
            print(a_cohort.name)
