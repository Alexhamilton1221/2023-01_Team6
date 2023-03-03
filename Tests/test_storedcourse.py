from unittest import TestCase

from Database.storedcourse import StoredCourse
from Database.course import Course
class TestStoredCourse(TestCase):
    def test_givenNoPrerequsits_generateCourse_createCorrectCourse(self):
        StoredCourse1 = StoredCourse("C1", 10, 1, [])
        Course1 = Course("C1", 10, [])
        genCourse = StoredCourse1.generate_course()

        answer = Course1.is_equal(genCourse)

        assert answer == True

    def test_lecture_length(self):
        StoredCourse2 = StoredCourse("21", 21, 1, [],"Class","H=1.5h")
        answer = 1.5

        assert answer == StoredCourse2.lecture_length()


    def test_return_lecture_total(self):
        #testing to see correct number of lectures returned
        #Stored course has 21 hours total and 3 hour lectures, answer should be 7
        StoredCourse3 = StoredCourse("21", 21, 1, [],"Class","H=3h")

        answer = 7
        assert answer == StoredCourse3.number_of_lectures()

