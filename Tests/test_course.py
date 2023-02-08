from unittest import TestCase
from Database.course import Course
from Database.lecture import Lecture
from Database.classroom import Classroom

class TestCourse(TestCase):

    def test_givenGoodLecture_addLecture_Addlecture(self):
        course = Course("CMPT101", 8, [])
        room = Classroom("11-101", 24)
        lecture1 = Lecture(room, 8, 10)

        course.add_lecture(lecture1)

        assert lecture1 == course.lectures[0]

    def test_givenNotLabCoure_is_lab_returnFalse(self):
        course = Course("CMPT101", 8, [])

        output = course.is_lab()

        return not output

    def test_givenLabCoure_is_lab_returnTrue(self):
        course = Course("CMPT102", 8, [], "Lab")

        output = course.is_lab()

        return output