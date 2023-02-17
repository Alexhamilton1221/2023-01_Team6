from unittest import TestCase
from Database.course import Course
from Database.lecture import Lecture
from Database.classroom import Classroom

class TestCourse(TestCase):

    def test_givenGoodLecture_addLecture_Addlecture(self):
        course = Course("CMPT101", 8, [])
        room = Classroom("11-101", 24)
        lecture1 = Lecture(8, 10)

        course.add_lecture(lecture1)

        assert lecture1 == course.lectures[0]

    def test_givenNotLabCoure_is_lab_returnFalse(self):
        course = Course("CMPT101", 8, [])

        output = course.is_lab()

        assert not output

    def test_givenLabCoure_is_lab_returnTrue(self):
        course = Course("CMPT102", 8, [], "Lab")

        output = course.is_lab()

        assert output

    def test_giventwodifferntOBject_is_equal_returnFalse(self):
        course = Course("CMPT102", 8, [], "Lab")
        v = 5

        answer = course.is_equal(v)

        assert answer == False

    def test_giventwodifferntPrereques_is_equal_returnFalse(self):
        course1 = Course("CMPT102", 8, [], "Lab")
        course2 = Course("CMPT102", 8, [course1], "Lab")


        answer = course1.is_equal(course2)

        assert answer == False

    def test_giventwoSameCourses_is_equal_returnTrue(self):
        course1 = Course("CMPT102", 8, [], "Lab")
        course2 = Course("CMPT102", 8, [course1], "Lab")
        course3 = Course("CMPT102", 8, [course1], "Lab")


        answer = course2.is_equal(course3)

        assert answer == True