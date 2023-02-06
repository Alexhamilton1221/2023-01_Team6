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
