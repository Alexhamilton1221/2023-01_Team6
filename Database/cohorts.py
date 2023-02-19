import math

from Database.classrooms import Classrooms
from Database.cohort import Cohort
from calc_space import get_hours
from calc_space import get_FullStack_hours


class NearLimit(Exception):
    # def __init__(self):

    # "Raises if the amount of students is near the abosoltue limit of courses
    pass

class OverLimit(Exception):
    # def __init__(self):

    # "Raises if there are too many students for the program to handle
    pass
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
            termed_students.append([group[0], int(group[1]), groups[1], 0])

        termed_students.sort(key=lambda program_count: program_count[2], reverse=True)
        return termed_students

    @staticmethod
    def __students_by_priority__(students):
        priority_levels = []
        # goes through each group and adds it priority level to the group
        for group in students:
            if group[3] not in priority_levels:
                priority_levels.append(group[3])
        priority_levels.sort(reverse=True)

        p_sorted_students = []
        for level in priority_levels:
            p_students = []
            for group in students:
                if group[3] == level:
                    p_students.append(group)
            p_students.sort(key=lambda student: student[2])
            p_sorted_students.append(p_students)

        return p_sorted_students

    @staticmethod
    def __check_if_fits__(capacities, group, programs, classroom_hours, lab_hours):
        fits = False
        for capacity in capacities:
            # This stores the hours that are to be removed if the capacity is correct
            hours_removal = []
            room_num = 0
            # Hours per cohort is the amount of hours this cohort will need for the program
            # total hours is the total number of hours needed for all cohorts
            hours_per_cohort = programs.get_program(group[0]).get_hours(lambda course: not course.is_lab())
            total_hours = hours_per_cohort * capacities[2]
            if programs.get_program(group[0]).is_core():

                # Goes through every classroom
                while room_num < len(classroom_hours) and total_hours > 0:
                    # Checks if room is not too small
                    if classroom_hours[room_num][1] >= capacity[1]:
                        # Removes all possibles hours from the classroom
                        total_hours -= math.floor(classroom_hours[room_num][1] / hours_per_cohort)
                    room_num += 1

                    # If the classrooms was able to handle hours
                if room_num == len(classroom_hours):
                    # This means that the current capacity cannot hold the students
                    # Changes the way that the students are stored
                    continue

                room_num = 0
                # Hours per cohort is the amount of hours this cohort will need for the program
                # total hours is the total number of hours needed for all cohorts
                hours_per_cohort = programs.get_program(group[0]).get_hours(lambda course: course.is_lab())
                total_hours = hours_per_cohort * capacities[2]
                while room_num < len(lab_hours) and total_hours > 0:
                    # Checks if room is not too small
                    if lab_hours[room_num][1] >= capacity[1]:
                        # Removes all possibles hours from the classroom
                        total_hours -= math.floor(lab_hours[room_num][1] / hours_per_cohort)
                    room_num += 1

                if room_num == len(lab_hours):
                    # This means that the current capacity cannot hold the students
                    # Changes the way that the students are stored
                    continue

                return True, capacity
        return False, None

    @staticmethod
    def __remove_hours_from_room_core__(capacity, group, programs, classroom_hours, lab_hours):

        room_num = 0
        # Hours per cohort is the amount of hours this cohort will need for the program
        # total hours is the total number of hours needed for all cohorts
        hours_per_cohort = programs.get_program(group[0]).get_hours(lambda course: not course.is_lab())
        total_hours = hours_per_cohort * capacity[2]
        # Goes through every classroom
        while room_num < len(classroom_hours) and total_hours > 0:
            # Checks if room is not too small
            if classroom_hours[room_num][1] >= capacity[1]:
                # Removes all possibles hours from the classroom and removes them from the classroom
                total_hours -= math.floor(classroom_hours[room_num][1] / hours_per_cohort)
                classroom_hours[room_num][1] -= math.floor(classroom_hours[room_num][1] / hours_per_cohort)
            room_num += 1

        room_num = 0
        # Hours per cohort is the amount of hours this cohort will need for the program
        # total hours is the total number of hours needed for all cohorts
        hours_per_cohort = programs.get_program(group[0]).get_hours(lambda course: course.is_lab())
        total_hours = hours_per_cohort * capacity[2]
        while room_num < len(lab_hours) and total_hours > 0:
            # Checks if room is not too small
            if lab_hours[room_num][1] >= capacity[1]:
                # Removes all possibles hours from the classroom
                total_hours -= math.floor(lab_hours[room_num][1] / hours_per_cohort)
                lab_hours[room_num][1] -= math.floor(classroom_hours[room_num][1] / hours_per_cohort)
            room_num += 1

    @staticmethod
    def __student_assignment__(students, class_by_size, labs_by_size, programs, safety_net=1.1):

        # These are lists of all the classrooms sizes by themselves, Ex [40, 36, 30, 24]
        class_sizes = []
        lab_sizes = []
        # These are list all the classrooms by the hours stored within
        classroom_hours = []
        lab_hours = []

        # This creates a separate list containing the classrooms hours for core (left) and program (right)
        # As cohorts are assigned the amount of spare hours will be decreased
        for room in class_by_size:
            # FORMAT [ROOM, ROOM SIZE, CORE HOURS, PROGRAM HOURS]
            classroom_hours.append([room, room.size, get_hours(), get_hours()])
            if room.size not in class_sizes:
                class_sizes.append(room.size)
        classroom_hours.sort(key=lambda room: room.size)

        # This creates a separate list containing the lab hours for core (left) and program (right), with extra hours
        # that full stack classes get on the far right.
        # As cohorts are assigned the amount of spare hours will be decreased
        for room in labs_by_size:
            # FORMAT [ROOM, ROOM SIZE,CORE HOURS, PROGRAM HOURS, FULL STACK ONLY HOURS]
            lab_hours.append([room, room.size, get_hours(), get_hours(), get_FullStack_hours()])
            if room.size not in class_sizes:
                lab_sizes.append(room.size)
        lab_sizes.sort(key=lambda room: room.size)

        # This pruduces a matrix with the outer array being the sorted priority
        sorted_priority_students = Cohorts.__students_by_priority__(students)

        for p_students in sorted_priority_students:
            # Go through all groups of students
            for group in p_students:
                # goes through all class sizes, and find the cohorts that leave around 10% extra room
                # capacities format is [Spare Space, cohort Size, cohort count]
                capacities = []
                for size in class_sizes:
                    # gets the size of the cohort with the safety net making the class bigger
                    cohort_count = math.ceil((group[2] * safety_net / size))
                    cohort_size = math.ceil((group[2] / cohort_count))
                    # Extra space is the size of the cohort times the size of the cohort minus the amount of student
                    extra_space = (cohort_count * size) - group[2]
                    capacities.append([extra_space, cohort_size, cohort_count])

                # Sorts the cohorts from the largest amount of extra space
                capacities.sort(key=lambda capacity: capacity[0], reverse=True)


                # Returns whether cohort fit, and which capacity it fit in (if it did)
                fits, capacity = Cohorts.__check_if_fits__(capacities, group, programs, classroom_hours, lab_hours)
                if not fits:
                    if group[3] < 50:
                        raise NearLimit
                        # If the group cannot fit, raises the priority of the group so they get first choice of room
                    group[3] += 1

                    Cohorts.__student_assignment__(students, labs_by_size, class_by_size, programs, safety_net)
                    return  # Very important return statement do not remove else the computer will violently detonate
                else:
                    # If there is enouh room in the classes for this cohort, removes its hours from the class
                    # so futor cohorts do not stack
                    Cohorts.__remove_hours_from_room_core__(capacity, group, programs, classroom_hours, lab_hours)

    def create_cohorts(self, classrooms, programs, students):
        # Given an amount of classrooms in the classrooms object
        # programs from the programs object
        # students: a list of students in the format [("PROGRAM-NAME TERM", COUNT)]
        # Ex: [("PCOM 1", 54),("PCOM 2", 45), ("PCOM 3", 81), ("PC 2", 32)]

        # This is sorting the list of students from largest to smallest amount of students
        termed_students = self.__read_students__(students)
        # These are the sorted lists of classrooms by their size from largest to smallest
        classes_by_size, labs_by_size = Classrooms.rooms_by_size(classrooms)

        # Classes by most even?
        # Compare the minimal amount it is different from
        # Do all again with priority level 0-1-2
        try:
            self.__student_assignment__(termed_students, classes_by_size, labs_by_size, programs)
        except NearLimit:
            # If the class does not fit, removes the 10% safty to try to match room sizes
            self.__student_assignment__(termed_students, classes_by_size, labs_by_size, programs, 1.0)

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
