import math

from Database.classrooms import Classrooms
from Database.cohort import Cohort
from Database.programs import Programs
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
            p_students.sort(key=lambda student: student[2], reverse=True)
            p_sorted_students.append(p_students)

        return p_sorted_students


    def __check_if_fits__(self, capacities, group, program, classroom_hours, lab_hours):
        not_core = int(not program.is_core())

        fits = False
        for capacity in capacities:
            # This stores the hours that are to be removed if the capacity is correct
            hours_removal = []
            room_num = 0
            # Hours per cohort is the amount of hours this cohort will need for the program
            # total hours is the total number of hours needed for all cohorts
            hours_per_cohort = program.get_hours(lambda course: course.delivery == "Class" and course.term == group[1])
            total_hours = hours_per_cohort * capacity[2]


            # Goes through every classroom
            while room_num < len(classroom_hours) and total_hours > 0:
                # Checks if room is not too small
                if classroom_hours[room_num][2 + not_core] >= hours_per_cohort:
                    # Removes all possibles hours from the classroom
                    total_hours -= hours_per_cohort * math.floor(classroom_hours[room_num][2 + not_core] / hours_per_cohort)
                else:
                    room_num += 1
                # If the classrooms was able to handle hours
            if room_num == len(classroom_hours):
                # This means that the current capacity cannot hold the students
                # Changes the way that the students are stored
                continue

            room_num = 0
            # Hours per cohort is the amount of hours this cohort will need for the program
            # total hours is the total number of hours needed for all cohorts
            hours_per_cohort = program.get_hours(lambda course: course.delivery == "Lab" and course.term == group[1])
            total_hours = hours_per_cohort * capacity[2]
            while room_num < len(lab_hours) and total_hours > 0:
                # Checks if the group is full stack
                if group[0] == "FS":
                    if lab_hours[room_num][4] >= hours_per_cohort:
                        total_hours -= math.floor(lab_hours[room_num][4] / hours_per_cohort)
                # Checks if room is not too small
                if lab_hours[room_num][2 + not_core] >= hours_per_cohort:
                    # Removes all possibles hours from the classroom
                    total_hours -= hours_per_cohort * math.floor(lab_hours[room_num][2 + not_core] / hours_per_cohort)
                else:
                    room_num += 1

            if room_num == len(lab_hours):
                # This means that the current capacity cannot hold the students
                # Changes the way that the students are stored
                continue

            return True, capacity
        return False, None

    def __create_unassigned_cohorts__(self, capacity, group, program):
        # Creates cohorts for a specific group of students (program term) and balances the amounts
        cohorts = []
        # CREATE COHORTS AND SET THEM DOWN THERE NOT DONE
        for i in range(capacity[2]):
            # TEMP
            cohorts.append(Cohort(program, group[1], i + 1, capacity[1],
                                  program.get_instance_courses()))
        extra_students = len(cohorts) * capacity[1] - group[2]
        c_num = 0
        while extra_students > 0:
            cohorts[c_num].count -= 1
            extra_students -= 1
            c_num += 1
            if c_num == len(cohorts):
                c_num = 0

        return cohorts

    def __set_rooms__(self, capacity, group, program, classroom_hours, lab_hours):
        # Adds a value for checking if a room is core or not and deducts the correct hours
        not_core = int(not program.is_core())

        assigned_class_index = 0
        assigned_lab_index = 0
        cohorts = self.__create_unassigned_cohorts__(capacity, group, program)

        room_num = 0
        # Hours per cohort is the amount of hours this cohort will need for the program
        # total hours is the total number of hours needed for all cohorts
        hours_per_cohort = program.get_hours(lambda course: course.delivery == "Class" and course.term == group[1])
        total_hours = hours_per_cohort * capacity[2]
        # Goes through every classroom
        while room_num < len(classroom_hours) and total_hours > 0:
            # Checks if room is not too small
            if classroom_hours[room_num][2 + not_core] >= hours_per_cohort:
                # Gets the amount of cohorts that fit in the room
                fitting_cohorts = math.floor(classroom_hours[room_num][2 + not_core] / hours_per_cohort)
                if fitting_cohorts > total_hours / hours_per_cohort:
                    fitting_cohorts = int(total_hours / hours_per_cohort)
                for i in range(fitting_cohorts):
                    cohorts[assigned_class_index + i].room = classroom_hours[room_num][0]
                assigned_class_index += fitting_cohorts
                # Removes all possibles hours from the classroom and removes them from the classroom
                total_hours -= hours_per_cohort * fitting_cohorts
                classroom_hours[room_num][2 + not_core] -= hours_per_cohort * fitting_cohorts
            else:
                room_num += 1

        room_num = 0
        # Hours per cohort is the amount of hours this cohort will need for the program
        # total hours is the total number of hours needed for all cohorts
        hours_per_cohort = program.get_hours(lambda course: course.delivery == "Lab" and course.term == group[1])
        total_hours = hours_per_cohort * capacity[2]
        while room_num < len(lab_hours) and total_hours > 0:
            # Goes through full stack hours first
            if group[0] == "FS":
                # DOES NOT WORK CURRENTLY - FIX
                if lab_hours[room_num][4] + lab_hours[room_num][2 + not_core] >= hours_per_cohort:
                    # Removes all possibles hours from the classroom
                    total_hours -= hours_per_cohort * lab_hours[room_num][4] / hours_per_cohort
                    lab_hours[room_num][4] -= hours_per_cohort * math.floor(lab_hours[room_num][4] / hours_per_cohort)

            # Checks if room is not too small
            if lab_hours[room_num][2 + not_core] >= hours_per_cohort:
                fitting_cohorts = math.floor(lab_hours[room_num][2 + not_core] / hours_per_cohort)
                if fitting_cohorts > total_hours / hours_per_cohort:
                    fitting_cohorts = int(total_hours / hours_per_cohort)

                for i in range(fitting_cohorts):
                    cohorts[assigned_lab_index + i].lab = lab_hours[room_num][0]
                assigned_lab_index += fitting_cohorts
                # Removes all possibles hours from the classroom
                total_hours -= hours_per_cohort * fitting_cohorts
                lab_hours[room_num][2 + not_core] -= hours_per_cohort * fitting_cohorts
            else:
                room_num += 1

        return cohorts


    def __student_assignment__(self, students, class_by_size, labs_by_size, programs, safety_net=1.1):

        # This holds the list of all cohorts created by the function, to be added at the end if they fit
        cohorts = []

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
        #classroom_hours.sort()

        # This creates a separate list containing the lab hours for core (left) and program (right), with extra hours
        # that full stack classes get on the far right.
        # As cohorts are assigned the amount of spare hours will be decreased
        for room in labs_by_size:
            # FORMAT [ROOM, ROOM SIZE,CORE HOURS, PROGRAM HOURS, FULL STACK ONLY HOURS]
            lab_hours.append([room, room.size, get_hours(), get_hours(), get_FullStack_hours()])
            if room.size not in class_sizes:
                lab_sizes.append(room.size)
        #lab_sizes.sort()

        # This pruduces a matrix with the outer array being the sorted priority
        sorted_priority_students = self.__students_by_priority__(students)

        for p_students in sorted_priority_students:
            # Go through all groups of students
            for group in p_students:
                # goes through all class sizes, and find the cohorts that leave around 10% extra room
                # capacities format is [Spare Space, cohort Size, cohort count]
                capacities = []
                # This gets the program of courese
                program = programs.get_program(lambda program: program.name == group[0])

                # This gets the capacity of ever class size with the possible cohort size
                for size in class_sizes:
                    # gets the size of the cohort with the safety net making the class bigger
                    cohort_count = math.ceil((group[2] * safety_net / size))
                    cohort_size = math.ceil((group[2] / cohort_count))
                    # Extra space is the size of the cohort times the size of the cohort minus the amount of student
                    extra_space = (cohort_count * size) - group[2]
                    capacities.append([extra_space, cohort_size, cohort_count])




                # Sorts the cohorts from the least amount of extra space (since the 10% extra is already accounted for)
                capacities.sort(key=lambda capacity: capacity[0])

                # Returns whether cohort fit, and which capacity it fit in (if it did)
                fits, capacity = self.__check_if_fits__(capacities, group, program, classroom_hours, lab_hours)
                if not fits:
                    if group[3] > 50:
                        raise NearLimit
                        # If the group cannot fit, raises the priority of the group so they get first choice of room
                    group[3] += 1

                    self.__student_assignment__(students, labs_by_size, class_by_size, programs, safety_net)
                    return  # Very important return statement do not remove else the computer will violently detonate
                else:
                    # If there is enouh room in the classes for this cohort, removes its hours from the class
                    # so futor cohorts do not stack
                    new_cohorts = self.__set_rooms__(capacity, group, program, classroom_hours, lab_hours)
                    for a_cohort in new_cohorts:
                        a_cohort.generate_name()
                        cohorts.append(a_cohort)

        # This adds the rooms to the classroom
        for cohort in cohorts:
            if cohort.room is not None:
                cohort.room.add_cohort(cohort)
            if cohort.lab is not None:
                cohort.lab.add_cohort(cohort)
        # Adds the cohort to the data class since they all fix
        self.cohorts = cohorts

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
