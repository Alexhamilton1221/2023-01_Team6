from calc_space import get_hours, get_FullStack_hours


class Classrooms:
    # A data storage class
    def __init__(self, classrooms = []):
        # An array of classrooms
        self.classrooms = classrooms

    @staticmethod
    def rooms_by_size(classrooms,separate=True):
        # Returns one or two lists depending on if the user wants a list that seperates the labs from the classrooms
        # based on the size of the rooms
        if separate:
            classes_by_size = classrooms.get_rooms(lambda x: x.is_lab == False)
            labs_by_size = classrooms.get_rooms(lambda x: x.is_lab == True)
            classes_by_size.sort(key=lambda x: x.size, reverse=True)
            labs_by_size.sort(key=lambda x: x.size, reverse=True)
            return classes_by_size, labs_by_size
        else:
            sized = classrooms.get_rooms()
            sized.sort(key=lambda x: x.size, reverse=True)
            return sized

    @staticmethod
    def rooms_by_size_with_hours(class_by_size, labs_by_size):
        # This returns lists of the classes_by_size and labs_by_size, with the hours for program and non-program

        class_sizes, lab_sizes, classroom_hours, lab_hours = [], [], [], []
        # This creates a separate list containing the classrooms hours for core (left) and program (right)
        # As cohorts are assigned the amount of spare hours will be decreased
        for room in class_by_size:
            # FORMAT [ROOM, ROOM SIZE, CORE HOURS, PROGRAM HOURS]
            classroom_hours.append([room, room.size, get_hours(), get_hours()])
            if room.size not in class_sizes:
                class_sizes.append(room.size)
        classroom_hours.sort(key=lambda room: room[1])

        # This creates a separate list containing the lab hours for core (left) and program (right), with extra hours
        # that full stack classes get on the far right.
        # As cohorts are assigned the amount of spare hours will be decreased
        for room in labs_by_size:
            # FORMAT [ROOM, ROOM SIZE,CORE HOURS, PROGRAM HOURS, FULL STACK ONLY HOURS]
            lab_hours.append([room, room.size, get_hours(), get_hours(), get_FullStack_hours()])
            if room.size not in class_sizes:
                lab_sizes.append(room.size)
        lab_sizes.sort(key=lambda room: room[1])

        return class_sizes, lab_sizes, classroom_hours, lab_hours

    def add_classroom(self, room):
        # Adds a new room to the classrooms
        self.classrooms.append(room)

    def get_room(self, specification):
        # Finds a room with the following specification
        for room in self.classrooms:
            if specification(room):
                return room
        return None

    def get_rooms(self, specification=lambda x: True):
        # Finds rooms with the following specification
        rooms = []
        for room in self.classrooms:
            if specification(room):
                rooms.append(room)
        return rooms