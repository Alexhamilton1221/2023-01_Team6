import math

from Database.classrooms import Classrooms




class RoomsException(Exception):
    # "Raised if the rooms have run out, either too small or not enough in total"
    pass


def get_hours():
    # This is the amount of hours for coures per classroom (for either core or program, but not together)
    hours_per_day = 8
    days = 24
    return hours_per_day * days


def get_FullStack_hours():
    # This is the amount of hours for fullstack courestack
    hours_per_day = 3.5
    days = 24
    return hours_per_day * days  # NOTE GET NUMBER OF HOURS TO CHECK CLASSES, ONCE GOTTEN CHECK FOR OVER TO SEE CAPACITY


def calc_cohort_hours_class(classrooms, cohorts):
    # Cohorts, the cohort database class (not array)
    # Classrooms, the classrooms database class (not array)


    # Returns each classroom with space and

    # Array of tuples with program, open space, assuming only Term 1 has new applications

    c_num = 0
    r_num = 0
    cohorts_by_size = cohorts.get_cohorts(lambda x: x.program.is_core())
    cohorts_by_size.sort(key=lambda x: x.count, reverse=True)
    rooms_by_size = classrooms.get_rooms(lambda x: not x.is_lab)
    rooms_by_size.sort(key=lambda x: x.size, reverse=True)

    try:
        while r_num < len(rooms_by_size):
            # This checks if the room is big enough for the cohort. If the room is not big enough, since both cohorts
            # are going from largest to smallest, this means that the rooms available are not large enough for the
            # cohorts
            if cohorts_by_size[c_num].count > rooms_by_size[r_num].size:
                print("Warning: Core Courses are over capacity, not enough classrooms of sufficient size")
                raise RoomsException
            hours_left = get_hours()

            while cohorts_by_size[c_num].get_hours(lambda x: x.delivery == "Class") < hours_left:
                hours_left -= cohorts_by_size[c_num].get_hours(lambda x: x.delivery == "Class")
                c_num += 1
                # if all courses are full, should return the amount of spare hours for classrooms

                if c_num == len(cohorts_by_size):

                    # Checks if the amount of hours left is greater or equal to 59, which is the minimal amount needed
                    # For a core classroom
                    if hours_left >= 59:
                        rooms_with_space = [(rooms_by_size[r_num], hours_left)]
                    else:
                        rooms_with_space = []
                    r_num += 1
                    while r_num < len(rooms_by_size):
                        rooms_with_space.append((rooms_by_size[r_num], get_hours()))
                        r_num += 1

                    return rooms_with_space
            r_num += 1

        # This checks after all rooms hours have been checked, if there are any cohorts that have not been
        if c_num != len(cohorts_by_size):
            print("Warning: Core Courses are over capacity, not enough rooms for the class hours needed")
            raise RoomsException

    # If there are not enough rooms, calculates the number of hours that the class needs
    except RoomsException:
        remainingHours = 0
        while c_num < len(cohorts_by_size):
            remainingHours += cohorts_by_size[c_num].size







def calc_extra_students(spare_hours, length, room_size):
    # space_hours - how many extra hours exist
    # length - the amount of hours of the program
    # rooms size - the size of the room
    number_of_classes = math.floor(spare_hours / length)
    return room_size * number_of_classes
