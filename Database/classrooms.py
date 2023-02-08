
class Classrooms:
    # A data storage class
    def __init__(self, classrooms = []):
        self.classrooms = classrooms

    def add_classroom(self, room):
        # Adds a new room to the classrooms
        self.classrooms.append(room)

    def get_room(self, specification):
        # Finds a room with the following specification
        for room in self.classrooms:
            if specification(room):
                return room
        return None

    def get_rooms(self, specification):
        # Finds rooms with the following specification
        rooms = []
        for room in self.classrooms:
            if specification(room):
                rooms.append(room)
        return rooms