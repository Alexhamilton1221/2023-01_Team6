


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