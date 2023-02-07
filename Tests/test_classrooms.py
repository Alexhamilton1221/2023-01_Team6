from unittest import TestCase
from Database.classrooms import Classrooms
from Database.classroom import Classroom

class TestClassrooms(TestCase):
    def test_givenNewClassRoom_AddClassromm_HaveNewClassroom(self):
        room = Classroom("1101", 24)
        rooms = Classrooms()

        rooms.add_classroom(room)
        gottenRoom = rooms.classrooms[0]

        assert room == gottenRoom

    def test_givenRequestingASingleRoom_get_room_retriveRoom(self):
        test_room = Classroom("1103", 24)
        room_array = [Classroom("1101", 24), test_room]
        rooms = Classrooms(room_array)

        gottenRoom = rooms.get_room(lambda room: room.name == "1103")

        assert test_room == gottenRoom

    def test_givenRequestMultipleRooms_get_rooms_RetriveallRoomd(self):
        test_room = Classroom("1103", 24)
        room_array = [Classroom("1101", 24), test_room]
        rooms = Classrooms([Classroom("1101", 24), Classroom("1103", 24)])
        rooms.add_classroom(Classroom("1001", 30))

        gotten_rooms = rooms.get_rooms(lambda room: room.size == 24)

        for i in range(0, 2):
            assert room_array[0].is_equal(gotten_rooms[0])