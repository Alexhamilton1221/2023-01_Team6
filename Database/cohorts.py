import math

from Database.classrooms import Classrooms
from Database.cohort import Cohort
from Database.programs import Programs
from calc_space import get_hours
from calc_space import get_FullStack_hours


class NearLimit(Exception):
    pass


class OverLimit(Exception):
    # def __init__(self):

    # "Raises if there are too many students for the program to handle
    pass


class Cohorts:

    def __init__(self, cohorts=[]):
        # The cohorts of the database (array of cohort)
        self.cohorts = cohorts

    def create_empty_lectures(self):
        for cohort in self.cohorts:
            cohort.create_empty_lectures()
    def create_schedules(self, term):
        self.create_empty_lectures()
        for cohort in self.cohorts:
            cohort.create_schedule(term)

    @staticmethod
    def __set_cohorts_rooms_from_list__(cohorts):
        # Goes through a list of cohorts, and adds the stored rooms within to classrooms
        # This adds the rooms to the classroom
        for cohort in cohorts:
            if cohort.room is not None:
                cohort.room.add_cohort(cohort)
            if cohort.lab is not None:
                cohort.lab.add_cohort(cohort)

    @staticmethod
    def __rooms_by_size_with_hours__(class_by_size, labs_by_size, cur_semester):
        # This returns lists of the classes_by_size and labs_by_size, with the hours for program and non-program

        class_sizes, lab_sizes, classroom_hours, lab_hours = [], [], [], []
        # This creates a separate list containing the classrooms hours for core (left) and program (right)
        # As cohorts are assigned the amount of spare hours will be decreased
        for room in class_by_size:
            # FORMAT [ROOM, ROOM SIZE, CORE HOURS, PROGRAM HOURS]
            classroom_hours.append([room, room.size, get_hours(True, cur_semester), get_hours(False, cur_semester)])
            if room.size not in class_sizes:
                class_sizes.append(room.size)
        classroom_hours.sort(key=lambda room: room[1])

        # This creates a separate list containing the lab hours for core (left) and program (right), with extra hours
        # that full stack classes get on the far right.
        # As cohorts are assigned the amount of spare hours will be decreased
        for room in labs_by_size:
            # FORMAT [ROOM, ROOM SIZE,CORE HOURS, PROGRAM HOURS, FULL STACK ONLY HOURS]
            lab_hours.append([room, room.size, get_hours(True, cur_semester), get_hours(False, cur_semester), get_FullStack_hours(cur_semester)])
            if room.size not in class_sizes:
                lab_sizes.append(room.size)
        lab_sizes.sort(key=lambda room: room[1])

        return class_sizes, lab_sizes, classroom_hours, lab_hours

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
        # This takes a list of students in the format [("PCOM 1", 54),("PCOM 2", 45), ("PCOM 3", 81), ("PC 2", 32)]
        priority_levels = []
        # goes through each group and adds it priority level to the group
        for group in students:
            if group[3] not in priority_levels:
                priority_levels.append(group[3])
        priority_levels.sort(reverse=True)

        p_sorted_students = []
        # Make
        for level in priority_levels:
            p_students = []
            for group in students:
                # Checks if the grous priority level is the same
                if group[3] == level:
                    p_students.append(group)
            p_students.sort(key=lambda student: student[2], reverse=True)
            p_sorted_students.append(p_students)

        return p_sorted_students

    def __check_if_fits__(self, capacities, group, program, classroom_hours, lab_hours, extra_time_mod):
        # Capcaites[extra space in group, the size of the cohort,the count of the cohort]
        #
        not_core = int(not program.is_core())
        total_hours = 0
        lab_failed = False
        for capacity in capacities:
            lab_failed = False
            # This stores the hours that are to be removed if the capacity is correct
            hours_removal = []
            room_num = 0
            # Hours per cohort is the amount of hours this cohort will need for the program
            # total hours is the total number of hours needed for all cohorts
            hours_per_cohort = math.ceil(program.get_hours(lambda course: course.delivery == "Class" and course.term == group[1]) * extra_time_mod)
            total_hours = hours_per_cohort * capacity[2]

            # Goes through every classroom
            while room_num < len(classroom_hours) and total_hours > 0:
                # Checks if the room is too small
                if classroom_hours[room_num][1] < capacity[1]:
                    room_num += 1
                    continue
                # Checks if room has enough hours
                if classroom_hours[room_num][2 + not_core] >= hours_per_cohort:
                    # Removes all possibles hours from the classroom
                    total_hours -= hours_per_cohort * math.floor(
                        classroom_hours[room_num][2 + not_core] / hours_per_cohort)

                room_num += 1
                # If the classrooms was able to handle hours
            if total_hours > 0:
                # This means that the current capacity cannot hold the students
                # Changes the way that the students are stored
                continue

            room_num = 0
            # Hours per cohort is the amount of hours this cohort will need for the program
            # total hours is the total number of hours needed for all cohorts
            hours_per_cohort = math.ceil(program.get_hours(lambda course: course.delivery == "Lab" and course.term == group[1]) * extra_time_mod)
            total_hours = hours_per_cohort * capacity[2]
            while room_num < len(lab_hours) and total_hours > 0:
                # Checks if the room is too small
                if lab_hours[room_num][1] < capacity[1]:
                    room_num += 1
                    continue
                # Checks if the group is full stack
                if group[0] == "FS":
                    if lab_hours[room_num][4] >= hours_per_cohort:
                        total_hours -= hours_per_cohort * math.floor(lab_hours[room_num][4] / hours_per_cohort)
                # Checks if room has enough hours remaining
                if lab_hours[room_num][2 + not_core] >= hours_per_cohort:
                    # Removes all possibles hours from the classroom
                    total_hours -= hours_per_cohort * math.floor(lab_hours[room_num][2 + not_core] / hours_per_cohort)

                room_num += 1

            if total_hours > 0:
                # This means that the current capacity cannot hold the students
                # Changes the way that the students are stored
                lab_failed = True
                continue

            return [0, None], capacity
        return [total_hours, lab_failed], None

    def __create_unassigned_cohorts__(self, capacity, group, program):
        # Creates cohorts for a specific group of students (program term) and balances the amounts
        cohorts = []
        # CREATE COHORTS AND SET THEM DOWN THERE NOT DONE
        for i in range(capacity[2]):
            cohorts.append(Cohort(program, group[1], i + 1, capacity[1],
                                  program.get_instance_courses(lambda course: course.term == group[1])))
        extra_students = len(cohorts) * capacity[1] - group[2]
        c_num = 0
        while extra_students > 0:
            cohorts[c_num].count -= 1
            extra_students -= 1
            c_num += 1
            if c_num == len(cohorts):
                c_num = 0

        return cohorts

    @staticmethod
    def __create_capacities__(class_sizes, group, safety_net):
        # Creates an array of capacities which are in the format [extra space in group, the size of the cohort,
        # the count of the cohort]
        capacities = []
        # This gets the capacity of ever class size with the possible cohort size
        for size in class_sizes:
            # gets the size of the cohort with the safety net making the class bigger
            cohort_count = math.ceil((group[2] * safety_net / size))
            cohort_size = math.ceil((group[2] / cohort_count))

            # Extra space is the size of the cohort times the size of the cohort minus the amount of student
            # Note: this line is extreemly important as it determenes what cohort sizes and amounts are priorities
            # To be made
            extra_space = math.floor(size * cohort_count - (group[2] * safety_net))

            capacities.append([extra_space, cohort_size, cohort_count])
        # Sorts the cohorts from the least amount of extra space (since the 10% extra is already accounted for)
        capacities.sort(key=lambda capacity: capacity[0])
        return capacities

    def __set_rooms__(self, capacity, group, program, classroom_hours, lab_hours, extra_time_mod):
        # Adds a value for checking if a room is core or not and deducts the correct hours
        not_core = int(not program.is_core())

        assigned_class_index = 0
        assigned_lab_index = 0
        cohorts = self.__create_unassigned_cohorts__(capacity, group, program)

        room_num = 0
        # Hours per cohort is the amount of hours this cohort will need for the program
        # total hours is the total number of hours needed for all cohorts
        hours_per_cohort = math.ceil(program.get_hours(lambda course: course.delivery == "Class" and course.term == group[1]) * extra_time_mod)
        total_hours = hours_per_cohort * capacity[2]
        # Goes through every classroom
        while room_num < len(classroom_hours) and total_hours > 0:
            # Checks if the room is too small
            if classroom_hours[room_num][1] < capacity[1]:
                room_num += 1
                continue
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

            room_num += 1

        room_num = 0
        # Hours per cohort is the amount of hours this cohort will need for the program
        # total hours is the total number of hours needed for all cohorts
        hours_per_cohort = math.ceil(program.get_hours(lambda course: course.delivery == "Lab" and course.term == group[1]) * extra_time_mod)
        total_hours = hours_per_cohort * capacity[2]
        while room_num < len(lab_hours) and total_hours > 0:
            # Checks if the room is too small
            if lab_hours[room_num][1] < capacity[1]:
                room_num += 1
                continue
            # Goes through full stack hours first
            if group[0] == "FS":

                # NOTE: THIS IS A STOP GAP, SOME TIME MAY BE WASTED FROM THE LACK OF CROSSOVER
                if lab_hours[room_num][4] + lab_hours[room_num][2 + not_core] >= hours_per_cohort:
                    fitting_cohorts = math.floor(lab_hours[room_num][4] / hours_per_cohort)
                    if fitting_cohorts > total_hours / hours_per_cohort:
                        fitting_cohorts = int(total_hours / hours_per_cohort)

                    for i in range(fitting_cohorts):
                        cohorts[assigned_lab_index + i].lab = lab_hours[room_num][0]
                    # Removes all possibles hours from the classroom
                    total_hours -= hours_per_cohort * fitting_cohorts
                    lab_hours[room_num][4] -= hours_per_cohort * fitting_cohorts


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

    def __student_assignment__(self, students, class_by_size, labs_by_size, programs, cur_semester, safety_net=1.1, extra_time_mod=1.0):
        # Returns: list of [success/failType, program , amount of extra hours, whether it was the labs that failed]
        # list[0]: 0 = success, 1 = nearly to capacity, 2 = over capacity

        # This holds the list of all cohorts created by the function, to be added at the end if they fit
        cohorts = []

        # These are lists of all the classrooms sizes by themselves, Ex [40, 36, 30, 24]
        # These are list all the classrooms by the hours stored within
        class_sizes, lab_sizes, classroom_hours, lab_hours = Cohorts.__rooms_by_size_with_hours__(class_by_size,
                                                                                        labs_by_size, cur_semester)

        # This pruduces a matrix with the outer array being the sorted priority
        sorted_priority_students = self.__students_by_priority__(students)

        for p_students in sorted_priority_students:
            # Go through all groups of students

            for group in p_students:
                # goes through all class sizes, and find the cohorts that leave around 10% extra room
                # capacities format is [Spare Space, cohort Size, cohort count]

                # This gets the program of courese
                program = programs.get_program(lambda program: program.name == group[0])
                capacities = Cohorts.__create_capacities__(class_sizes, group, safety_net)

                # Returns whether cohort fit, and which capacity it fit in (if it did)
                fail_check, capacity = self.__check_if_fits__(capacities, group, program, classroom_hours, lab_hours, extra_time_mod=extra_time_mod)
                if fail_check[0] > 0:
                    if group[3] > 50:
                        # Checks if the safty has been removed, if so there is no room for the safty to be removed

                        if safety_net == 1.0:
                            raise OverLimit
                        else:
                            raise NearLimit
                        # If the group cannot fit, raises the priority of the group so they get first choice of room
                    group[3] += 1

                    self.__student_assignment__(students, class_by_size, labs_by_size, programs, cur_semester, safety_net, extra_time_mod)
                    return  # This ends the recusive loop
                else:
                    # If there is enouh room in the classes for this cohort, removes its hours from the class
                    # so futor cohorts do not stack
                    new_cohorts = self.__set_rooms__(capacity, group, program, classroom_hours, lab_hours, extra_time_mod)
                    for a_cohort in new_cohorts:
                        a_cohort.generate_name()
                        cohorts.append(a_cohort)

        Cohorts.__set_cohorts_rooms_from_list__(cohorts)
        # Adds the cohort to the data class since they all fix
        self.cohorts = cohorts

    def create_cohorts(self, classrooms, programs, students, cur_semester, extra_time_mod=1.0):
        # Given an amount of classrooms in the classrooms object
        # programs from the programs object
        # students: a list of students in the format [("PROGRAM-NAME TERM", COUNT)]
        # Ex: [("PCOM 1", 54),("PCOM 2", 45), ("PCOM 3", 81), ("PC 2", 32)]

        # This is sorting the list of students from largest to smallest amount of students
        termed_students = self.__read_students__(students)
        # These are the sorted lists of classrooms by their size from largest to smallest
        classes_by_size, labs_by_size = Classrooms.rooms_by_size(classrooms)

        # Compare the minimal amount it is different from
        # Do all again with priority level 0-1-2
        try:

            self.__student_assignment__(termed_students, classes_by_size, labs_by_size, programs, cur_semester, 1.1, extra_time_mod)
        except NearLimit:

            # If the class does not fit, removes the 10% safty to try to match room sizes
            try:
                self.__student_assignment__(termed_students, classes_by_size, labs_by_size, programs, cur_semester, 1.0, extra_time_mod)

                # TEMP, PUT STUFF HERE TO INFOM THE USER ABOUT HOW IT FAILED
                fail_type = NearLimit
            except OverLimit:
                print("WARNING: TOO MANY STUDENTS. (ADD better error handeling here)")
                fail_type = OverLimit

        return None

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
            print(a_cohort.name, " - ", a_cohort.count, sep='')
