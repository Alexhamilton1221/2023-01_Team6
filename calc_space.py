import math

from Database.classrooms import Classrooms


class RoomsTooSmallException(Exception):
    # def __init__(self):

    # "Raised if the rooms have run out, either too small or not enough in total"
    pass


class NotEnoughRoomsException(Exception):
    # def __init__(self, cohorts):

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


def calc_cohort_hours(classrooms, cohorts, core, lab):
    # Cohorts, the cohort database class (not array)
    # Classrooms, the classrooms database class (not array)

    # Returns each classroom with space and

    # Array of tuples with program, open space, assuming only Term 1 has new applications

    # Current Issues:
    # Can skip over some class use if two cohorts are of a similar size but take a different time make

    c_num = 0
    r_num = 0
    cohorts_by_size = cohorts.get_cohorts(lambda x: x.program.is_core() == core)
    cohorts_by_size.sort(key=lambda x: x.count, reverse=True)
    rooms_by_size = classrooms.get_rooms(lambda x: x.is_lab == lab)
    rooms_by_size.sort(key=lambda x: x.size, reverse=True)

    try:
        while r_num < len(rooms_by_size):
            # This checks if the room is big enough for the cohort. If the room is not big enough, since both cohorts
            # are going from largest to smallest, this means that the rooms available are not large enough for the
            # cohorts
            if cohorts_by_size[c_num].count > rooms_by_size[r_num].size:
                print("Warning: Core Courses are over capacity, not enough classrooms of sufficient size")
                raise RoomsTooSmallException
            hours_left = get_hours()

            while cohorts_by_size[c_num].get_hours(lambda x: x.is_lab() == lab) < hours_left:
                if cohorts_by_size[c_num].program.name == "FS":
                    hours_left += get_FullStack_hours
                hours_left -= cohorts_by_size[c_num].get_hours(lambda x: x.is_lab() == lab)
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
            raise NotEnoughRoomsException

    # If there are not enough rooms, calculates the number of hours that the class needs
    except RoomsTooSmallException:
        print("TEMP")
        # remainingHours = 0
        # while c_num < len(cohorts_by_size):
        #     remainingHours += cohorts_by_size[c_num].size


def calc_cohort_capacity(classrooms, cohorts):
    # This calculates the number of extra students each cohort can take, assumging that only cohorts of the
    # First term can get new students

    classes_by_size = classrooms.get_rooms(lambda x: x.is_lab == False)
    labs_by_size = classrooms.get_rooms(lambda x: x.is_lab == True)

    classes_by_size.sort(key=lambda x: x.size, reverse=True)
    labs_by_size.sort(key=lambda x: x.size, reverse=True)

    cohorts_with_spare_rooms = []

    for core in [True, False]:
        # Resets the search for core programs and non-core, since thay can use the rooms twice, since they are on differn't days
        cohorts_by_size = cohorts.get_cohorts(lambda x: x.program.is_core() == core)
        cohorts_by_size.sort(key=lambda x: x.count, reverse=True)
        c_num = 0
        cl_num = 0
        lab_num = 0
        class_hours_left = get_hours()
        lab_hours_left = get_hours()

        # Loops for every cohort available
        while c_num < len(cohorts_by_size):

            # For each lab while finding one, (this should only be one)
            while lab_num < len(labs_by_size):
                if cohorts_by_size[c_num].program.name == "FS":
                    lab_hours_left += get_FullStack_hours()

                # Removes the hours if it has enough, else, goes to the next lab
                if cohorts_by_size[c_num].get_hours(lambda x: x.is_lab() == True) < lab_hours_left:
                    lab_hours_left -= cohorts_by_size[c_num].get_hours(lambda x: x.is_lab() == True)
                    break
                else:
                    lab_num += 1
                    lab_hours_left = get_hours()

            # For each class while finding one, (this should only be one)
            while cl_num < len(classes_by_size):

                # Removes the hours if it has enough, else, goes to the next lab
                if cohorts_by_size[c_num].get_hours(lambda x: x.is_lab() == False) < class_hours_left:
                    class_hours_left -= cohorts_by_size[c_num].get_hours(lambda x: x.is_lab() == False)
                    break
                else:
                    cl_num += 1
                    class_hours_left = get_hours()

            # Only adds if it is the first term, as you can't add new students to old cohorts ()
            if cohorts_by_size[c_num].term == 1:
                size_lab = labs_by_size[lab_num].size - cohorts_by_size[c_num].count
                size_class = classes_by_size[cl_num].size - cohorts_by_size[c_num].count
                if size_class < size_lab:
                    if size_class != 0:
                        cohorts_with_spare_rooms.append((cohorts_by_size[c_num], size_class))
                else:
                    if size_lab != 0:
                        cohorts_with_spare_rooms.append((cohorts_by_size[c_num], size_lab))

            c_num += 1
                # if all courses are full, should return the amount of spare hours for classrooms


    return cohorts_with_spare_rooms

    # If there are not enough rooms, calculates the number of hours that the class needs



def calc_extra_students(spare_hours, length, room_size):
    # space_hours - how many extra hours exist
    # length - the amount of hours of the program
    # rooms size - the size of the room
    number_of_classes = math.floor(spare_hours / length)
    return room_size * number_of_classes
