from unittest import TestCase
from Database.lecture import Lecture
from Database.classroom import Classroom


class TestLecture(TestCase):
    def test_givenStartOverlappingLecture_isWithin_ReturnTrue(self):
        classroom = Classroom("523", 24)
        Lec1 = Lecture(0, 8, 10)
        Lec2 = Lecture(0, 9, 11)

        # Test Should be assisciative
        assert True == Lec1.is_within(Lec2)
        assert True == Lec2.is_within(Lec1)


    def test_givenEndOverlappingLecture_isWithin_ReturnTrue(self):
        classroom = Classroom("523", 24)
        Lec1 = Lecture(0, 8, 10)
        Lec2 = Lecture(0, 7, 9)

        # Test Should be assisciative
        assert True ==  Lec1.is_within(Lec2)
        assert True ==  Lec2.is_within(Lec1)


    def test_givenCompleteOverlappingLecture_isWithin_ReturnTrue(self):
        classroom = Classroom("523", 24)
        Lec1 = Lecture(0, 8, 10)
        Lec2 = Lecture(0, 7, 11)

        # Test Should be assisciative
        assert True == Lec1.is_within(Lec2)
        assert True == Lec2.is_within(Lec1)

    def test_givenNonOVerLapping_isWithin_ReturnFalse(self):
        classroom = Classroom("523", 24)
        Lec1 = Lecture(0, 8, 9)
        Lec2 = Lecture(0, 9, 11)


        # Test Should be assisciative
        assert False == Lec1.is_within(Lec2)
        assert False == Lec2.is_within(Lec1)
