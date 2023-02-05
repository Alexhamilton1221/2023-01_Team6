from unittest import TestCase
from Database.lecture import Lecture
from Database.classroom import Classroom


class TestLecture(TestCase):
    def test_givenOverlappingLecture_isWithin_ReturnTrue(self):
        classroom = Classroom("523", 24)
        Lec1 = Lecture(classroom, 8, 10)
        Lec2 = Lecture(Classroom, 9, 11)

        output = Lec1.is_within(Lec2)

        assert False == output
